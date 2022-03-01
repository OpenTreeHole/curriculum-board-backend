user_verification_address = "https://api.fduhole.com/users"
model_modules: list[str] = ['models']
database_config = {
    'connections': {
        # Dict format for connection
        # 'default': {
        #     'engine': 'tortoise.backends.asyncpg',
        #     'credentials': {
        #         'host': 'localhost',
        #         'port': '5432',
        #         'user': 'tortoise',
        #         'password': 'qwerty123',
        #         'database': 'test',
        #     }
        # },
        # Using a DB_URL string
        'default': 'sqlite://test.sqlite3'
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
