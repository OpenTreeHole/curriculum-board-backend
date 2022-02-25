from sanic import Blueprint

bp_curriculum_board: Blueprint = Blueprint('curriculum_board')
auth: Blueprint = Blueprint('auth')
from .curriculum_board import api
from .auth import api
