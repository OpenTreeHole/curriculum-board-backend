from sanic_ext.extensions.openapi import openapi

from blueprints import bp_curriculum_board
from sanic.response import json
from sanic import Request

from blueprints.auth.decorator import authorized
from models import Review


@bp_curriculum_board.post("/reviews")
@openapi.body({"application/json": Review})
@authorized()
def add_review(request: Request):
    request.json().get()
    return json({'res': 1})
