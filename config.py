from aiocache import Cache
from aiocache.serializers import JsonSerializer
from sanic import Sanic
from sanic_ext import Extend

app: Sanic = Sanic("CurriculumBoard")
Extend(app)

app = Sanic.get_app()

user_verification_address = "https://api.fduhole.com/users"

model_modules: list[str] = ['models', "aerich.models"]
database_config = {
    'connections': {
        'default': app.config.get('DB_URL', 'mysql://username:password@mysql:3306/cb')
    },
    'apps': {
        'models': {
            'models': model_modules,
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'UTC'
}

global_json_cache = Cache(serializer=JsonSerializer())
