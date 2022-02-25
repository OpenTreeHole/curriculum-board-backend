from sanic import Blueprint

bp_curriculum_board: Blueprint = Blueprint('api_v1')
from .curriculum_board import api
from .auth import api
