from typing import Type, List

from sanic import json, HTTPResponse
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
