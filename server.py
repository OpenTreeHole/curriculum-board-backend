from sanic import Sanic
from sanic_ext import Extend
from tortoise import Tortoise
from tortoise.contrib.sanic import register_tortoise

from blueprints import bp_curriculum_board, bp_auth

app: Sanic = Sanic("CurriculumBoard")
Extend(app)

register_tortoise(app, db_url='sqlite://:memory:',
                  modules={'models': ['models']}, generate_schemas=True)

if __name__ == "__main__":
    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.blueprint(bp_curriculum_board)
    app.blueprint(bp_auth)
    app.run(host="0.0.0.0", port=8000)
