from aiocache import Cache
from aiocache.serializers import JsonSerializer
from sanic import Sanic
from sanic_ext import Extend
from sanic_gzip import Compress

compress = Compress()
app: Sanic = Sanic("CurriculumBoard")
Extend(app)

app = Sanic.get_app()

# SANIC_AUTH_API_URL
user_verification_address = app.config.get("AUTH_API_URL", "https://testauth.fduhole.com/api/users/me")

model_modules: list[str] = ['models', "aerich.models"]
database_config = {
    'connections': {
        'default': app.config.get('DB_URL', 'mysql://root:root@127.0.0.1:3306/board')
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
