from blueprints import bp_curriculum_board
from sanic.response import json
from sanic import Request

from blueprints.curriculum_board.models.course import Course


@bp_curriculum_board.route("/")
def select(request: Request):
    return json({'res': 1})
