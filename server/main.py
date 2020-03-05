import asyncio
import logging
import pathlib
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from utility import init_redis, load_config, init_workers
from views import MainPageHandler
from routes import setup_routes
from db import init_sqlite

TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'
PROJECT_ROOT = pathlib.Path(__file__).parent
STATIC_ROOT = pathlib.Path(__file__).parent.parent / 'static'


async def setup_sqlite(app: web.Application, conf, loop):
    connection = await init_sqlite(conf['sqlite'], loop)

    async def close_sqlite(app):
        await connection.close()

    app.on_cleanup.append(close_sqlite)
    app['sqlite_connection'] = connection
    return connection


async def setup_redis(app: web.Application, conf, loop):
    pool = await init_redis(conf['redis'], loop)

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


def setup_jinja(app: web.Application):

    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
    return jinja_env





async def init(loop):
    conf = load_config(PROJECT_ROOT/'config.yaml')

    port = int(os.environ.get('PORT', conf['port']))
    conf['port'] = port

    app = web.Application(loop=loop)
    #redis_pool = await setup_redis(app, conf, loop)
    sqlite_connection = await setup_sqlite(app, conf, loop)
    setup_jinja(app)
    executor = await init_workers(app, conf)
    redis_pool = None
    handler = MainPageHandler(redis_pool, conf, executor, sqlite_connection)
    setup_routes(app, handler, STATIC_ROOT)


    return app, conf['host'], conf['port']


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    #loop.set_debug(True)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()