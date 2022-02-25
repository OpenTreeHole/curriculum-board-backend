from sanic import Sanic

from blueprints import bp_curriculum_board

app = Sanic("JIARAN")

if __name__ == "__main__":
    app.blueprint(bp_curriculum_board)
    app.run(host="0.0.0.0", port=8000)
