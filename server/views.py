import asyncio
import logging
import json

import aiohttp_jinja2
from aiohttp import web


from warm import get_closest, calc_analogy
from db import get_autocomplete, get_points, get_region_neighbours


class MainPageHandler:

    def __init__(self, redis, conf, executor, con):
        self._redis = redis
        self._conf = conf
        self._executor = executor
        self._loop = asyncio.get_event_loop()
        self._connection_sqlite = con
        self.logger = logging.getLogger('aiohttp.server')

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    async def get_closest_anime(self, request: web.Request):
        title = request.match_info['title']
        top = request.match_info['top']
        anime_list = await self._loop.run_in_executor(self._executor, get_closest, title, int(top))
        return web.json_response({"response": anime_list})

    async def autocomplete(self, request: web.Request):
        prefix = request.match_info['prefix']
        is_cahced = await self._redis.exists('autocomplete:{}'.format(prefix))
        if is_cahced:
            res = await self._redis.lrange('autocomplete:{}'.format(prefix), 0, -1)
            res = [a.decode('utf-8') for a in res]
        else:
            res = await get_autocomplete(self._connection_sqlite, prefix)
            res = [a[0] for a in res]
            await self._redis.rpush('autocomplete:{}'.format(prefix), *res)
            await self._redis.expire('autocomplete:{}'.format(prefix), 60*60)
        return web.json_response(res)

    async def get_all_points(self, request: web.Request):
        res = await get_points(self._connection_sqlite)
        return web.json_response(res)

    async def get_neighbours(self, request: web.Request):
        title, margin = request.match_info['title'], request.match_info['margin']
        is_cached = await self._redis.exists('neighbours:{}'.format(title))
        if is_cached:
            res = await self._redis.lrange('neighbours:{}'.format(title), 0, -1)
            res = [a.decode('utf-8') for a in res]
        else:
            res = await get_region_neighbours(self._connection_sqlite, title, margin)
            await self._redis.lpush('neighbours:{}'.format(title), *res)
            await self._redis.expire('neighbours:{}'.format(title), 60*60)
        return web.json_response(res)

    async def get_analogy(self, request: web.Request):
        base_title, rel_title, req_title = request.match_info['base_title'], request.match_info['rel_title'], request.match_info['req_title']
        res = await self._loop.run_in_executor(self._executor, calc_analogy, base_title, rel_title, req_title)
        return web.json_response(res)


