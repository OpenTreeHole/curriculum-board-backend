from typing import Type, Union, Optional

from sanic import json, HTTPResponse
from sanic_ext.extensions.openapi.definitions import Response
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel


async def jsonify(cls: Type[PydanticModel], obj: Model) -> str:
    try:
        # 优先使用 from_orm，因为它不会覆写我们手动添加的额外字段，例如 is_me。
        # 当然，这个方法不会做 prefetch 的工作，所以如果你自己没调用 fetch_related，可能会报错。
        return cls.from_orm(obj).json()
    except:
        pass
    return (await cls.from_tortoise_orm(obj)).json()


async def jsonify_list(cls: Type[PydanticModel], obj: list[Model]) -> str:
    json_elements: list[str] = [await jsonify(cls, r) for r in obj]
    return '[' + ','.join(json_elements) + ']'


async def jsonify_list_response(cls: Type[PydanticModel], obj: list[Model]) -> HTTPResponse:
    return json(await jsonify_list(cls, obj), dumps=lambda x: x)


async def jsonify_response(cls: Type[PydanticModel], obj: Model) -> HTTPResponse:
    return json(await jsonify(cls, obj), dumps=lambda x: x)


class Struct(object):
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value


def objectify(original_dict: dict) -> Struct:
    return Struct(original_dict)


def standardize(obj: Union[str, object], status=200):
    if obj is str:
        return {
            "status_code": status,
            "description": "Success",
            "message": obj
        }
    else:
        return {
            "status_code": status,
            "description": "Success",
            "data": obj
        }


def standard_openapi_response(obj: Union[str, object], status=200, description: Optional[str] = None):
    return Response(
        {
            "application/json": standardize(obj)
        },
        description=description,
        status=status
    )
