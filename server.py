from sanic import Sanic
from sanic_ext import Extend

from blueprints import bp_curriculum_board

app = Sanic("CurriculumBoard")
Extend(app)

if __name__ == "__main__":
    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.blueprint(bp_curriculum_board)
    app.run(host="0.0.0.0", port=8000)
