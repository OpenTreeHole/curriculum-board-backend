import requests
from sanic import Request, json, text
from sanic.exceptions import Unauthorized

import config
from blueprints import bp_curriculum_board


@bp_curriculum_board.get("/login")
async def login(request: Request):
    request.headers.items()
    authorization = request.headers.get("Authorization")
    if authorization is not None:
        response: requests.Response = requests.get(config.user_verification_address, headers=request.headers.items())
        return json(response.json())
    raise Unauthorized("Authorization Failed.")
