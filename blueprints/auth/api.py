from sanic import Request, json

from blueprints import bp_auth
from blueprints.auth.decorator import authorized


@bp_auth.get("/login")
@authorized()
async def login(request: Request):
    return json({"user_id": request.ctx.user_id})