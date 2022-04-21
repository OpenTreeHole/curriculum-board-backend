import asyncio
import multiprocessing

import aiohttp
from sanic_ext.extensions.openapi.constants import SecuritySchemeAuthorization
from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise

from config import model_modules, database_config, app

register_tortoise(app, config=database_config, generate_schemas=True)


@app.listener("before_server_start")
async def init_aiohttp(_, __):
    app.ctx.global_session = aiohttp.ClientSession()


@app.listener("after_server_stop")
async def close_aiohttp(_, __):
    await app.ctx.global_session.close()


def main():
    Tortoise.init_models(model_modules, "models")
    app.ext.openapi.add_security_scheme("Token", "apiKey", scheme=SecuritySchemeAuthorization.OAUTH)
    from blueprints import bp_curriculum_board, bp_auth
    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.config.OAS_UI_DEFAULT = "swagger"
    app.blueprint(bp_curriculum_board)
    app.blueprint(bp_auth)
    app.run(
        host="0.0.0.0",
        fast=True,
        port=8000
    )


async def migrate_database():
    from aerich import Command
    command = Command(tortoise_config=database_config)
    await command.init()
    try:
        await command.init_db(safe=True)
    except:
        pass
    try:
        await command.migrate()
    except:
        pass
    await command.upgrade()


if __name__ == "__main__":
    # 创建事件循环，运行数据库迁移
    loop = asyncio.get_event_loop()
    loop.run_until_complete(migrate_database())
    main()
