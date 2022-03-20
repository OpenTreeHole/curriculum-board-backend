import multiprocessing

import aiohttp
from sanic import Sanic
from sanic_ext import Extend
from sanic_ext.extensions.openapi.constants import SecuritySchemeAuthorization
from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise

app: Sanic = Sanic("CurriculumBoard")
Extend(app)
from config import model_modules, database_config

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
        workers=multiprocessing.cpu_count(),
        port=8000
    )


if __name__ == "__main__":
    main()
