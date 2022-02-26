from sanic import Sanic
from sanic_ext import Extend
from tortoise import Tortoise

from blueprints import bp_curriculum_board, bp_auth

app: Sanic = Sanic("CurriculumBoard")
Extend(app)


@app.listener("before_server_start")
async def init_orm(_, __):
    await Tortoise.init(
        db_url='sqlite://test.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


@app.listener("after_server_stop")
async def close_orm(_, __):
    await Tortoise.close_connections()


if __name__ == "__main__":
    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.blueprint(bp_curriculum_board)
    app.blueprint(bp_auth)
    app.run(host="0.0.0.0", port=8000)
