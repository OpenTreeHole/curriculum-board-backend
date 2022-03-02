from functools import wraps

from sanic import Request, Sanic
from sanic.exceptions import Unauthorized
from sanic.log import error_logger
from sanic_ext.extensions.openapi import openapi

import config


async def __get_or_fetch_user(authorization_header: str) -> dict:
    """
    带缓存地获取用户 JSON。
    :param authorization_header: 带 APIKEY 的 Header，如 'token abcd1234'
    """
    cached_json = await config.global_json_cache.get(authorization_header)
    if cached_json is not None:
        return cached_json
    async with Sanic.get_app("CurriculumBoard").ctx.global_session.get(
            config.user_verification_address,
            headers={
                'Authorization': authorization_header}) as response:
        if response.status == 401:
            raise Unauthorized("Authorization Failed.")
        elif 400 <= response.status < 600:
            raise Unauthorized("Internal Error: Cannot validate authorization information.")
        try:
            new_json = await response.json()
            await config.global_json_cache.set(authorization_header, new_json)
            return new_json
        except Exception:
            error_logger.error('Failed to fetch token for ' + authorization_header, exc_info=True)
            raise Unauthorized("Internal Error: Cannot validate authorization information.")


def authorized():
    def decorator(f):
        @openapi.secured("Token")
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            authorization = request.headers.get("Authorization")
            if authorization is not None:
                user_json = await __get_or_fetch_user(authorization)
                try:
                    user_id: int = user_json.get('user_id')
                    is_admin: bool = user_json.get('is_admin')
                except Exception:
                    error_logger.error('Failed to fetch token for ' + authorization, exc_info=True)
                    raise Unauthorized("Internal Error: Cannot validate authorization information.")
                request.ctx.user_id = user_id
                request.ctx.is_admin = is_admin
                return await f(request, *args, **kwargs)
            raise Unauthorized("Authorization Information Needed.")

        return decorated_function

    return decorator
