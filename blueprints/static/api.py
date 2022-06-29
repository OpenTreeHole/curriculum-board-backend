from sanic import response

from blueprints import bp_static
from config import compress


@bp_static.get("/static/cedict_ts.u8")
@compress.compress()
async def cedict(request):
    return await response.file(
        location="static/cedict_ts.u8",  headers={'charset': 'utf-8'})
