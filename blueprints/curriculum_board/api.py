from blueprints import bp_curriculum_board
from sanic.response import json
from sanic import Request

from blueprints.auth.decorator import authorized


@bp_curriculum_board.route("/")
@authorized()
def select(request: Request):
    return json({'res': 1})
