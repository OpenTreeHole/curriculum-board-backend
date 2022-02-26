from functools import wraps

import requests
from sanic import Request
from sanic.exceptions import Unauthorized
from sanic_ext.extensions.openapi import openapi

import config


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            authorization = "token 3290a52217bf7c775db5ac10242ea91cc21b7342"
            if authorization is not None:
                response: requests.Response = \
                    requests.get(config.user_verification_address, headers={'Authorization': authorization})
                if response.status_code == 401:
                    raise Unauthorized("Authorization Failed.")
                elif 400 <= response.status_code < 600:
                    raise Unauthorized("Internal Error: Cannot validate authorization information.")
                try:
                    user_id: int = response.json().get('user_id')
                except Exception:
                    raise Unauthorized("Internal Error: Cannot validate authorization information.")
                request.ctx.user_id = user_id
                return await f(request, *args, **kwargs)
            raise Unauthorized("Authorization Information Needed.")

        openapi.parameter("Authorization", str, "header")(decorated_function)
        return decorated_function

    return decorator
