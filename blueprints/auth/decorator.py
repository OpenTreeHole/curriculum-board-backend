from functools import wraps

import requests
from sanic import Request
from sanic.exceptions import Unauthorized
from sanic_ext.extensions.openapi import openapi

import config


def authorized():
    def decorator(f):
        @openapi.secured("Token")
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            authorization = request.headers.get("Authorization")
            if authorization is not None:
                response: requests.Response = \
                    requests.get(config.user_verification_address, headers={'Authorization': authorization})
                if response.status_code == 401:
                    raise Unauthorized("Authorization Failed.")
                elif 400 <= response.status_code < 600:
                    raise Unauthorized("Internal Error: Cannot validate authorization information.")
                try:
                    user_id: int = response.json().get('user_id')
                    is_admin: bool = response.json().get('is_admin')
                except Exception:
                    raise Unauthorized("Internal Error: Cannot validate authorization information.")
                request.ctx.user_id = user_id
                request.ctx.is_admin = is_admin
                return await f(request, *args, **kwargs)
            raise Unauthorized("Authorization Information Needed.")

        return decorated_function

    return decorator
