from sanic import Blueprint

bp_curriculum_board: Blueprint = Blueprint('curriculum_board')
bp_auth: Blueprint = Blueprint('auth')
bp_static: Blueprint = Blueprint('static')
from .curriculum_board import api
from .auth import api
from .static import api