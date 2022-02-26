from sanic import Sanic
from sanic_ext import Extend
from tortoise import Tortoise, run_async
from tortoise.contrib.sanic import register_tortoise

from config import model_modules

app: Sanic = Sanic("CurriculumBoard")
Extend(app)

register_tortoise(app, db_url='sqlite://test.sqlite3',
                  modules={'models': model_modules}, generate_schemas=True)


def main():
    Tortoise.init_models(model_modules, "models")
    from blueprints import bp_curriculum_board, bp_auth
    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.blueprint(bp_curriculum_board)
    app.blueprint(bp_auth)
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
