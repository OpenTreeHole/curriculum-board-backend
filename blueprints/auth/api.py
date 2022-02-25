from sanic import Request, json

from blueprints import auth
from blueprints.auth.decorator import authorized


@auth.get("/login")
@authorized()
async def login(request: Request):
    return json({"user_id": request.ctx.user_id})