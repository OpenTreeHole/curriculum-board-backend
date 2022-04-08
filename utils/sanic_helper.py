from typing import Type, Union, Optional

from sanic import json, HTTPResponse
from sanic_ext.extensions.openapi.definitions import Response
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel


async def jsonify(cls: Type[PydanticModel], obj: Model) -> str:
    return (await cls.from_tortoise_orm(obj)).json()


async def jsonify_list(cls: Type[PydanticModel], obj: list[Model]) -> str:
    json_elements: list[str] = [await jsonify(cls, r) for r in obj]
    return '[' + ','.join(json_elements) + ']'


async def jsonify_list_response(cls: Type[PydanticModel], obj: list[Model]) -> HTTPResponse:
    return json(await jsonify_list(cls, obj), dumps=lambda x: x)


async def jsonify_response(cls: Type[PydanticModel], obj: Model) -> HTTPResponse:
    return json(await jsonify(cls, obj), dumps=lambda x: x)


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
