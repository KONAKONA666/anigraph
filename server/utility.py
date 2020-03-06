import aioredis
import yaml
import asyncio
import pathlib

from concurrent.futures import ProcessPoolExecutor

import trafaret as t
from aiohttp import web


from warm import warm, clean

PROJECT_ROOT = pathlib.Path(__file__).parent

def load_config(file_path):
    with open(file_path, 'rt') as f:
        data = yaml.load(f)
    return data


async def init_redis(conf, loop):
    pool = await aioredis.create_redis_pool(
        conf['host'],
        loop=loop
    )
    return pool


async def init_workers(app, conf):
    n = conf['max_workers']
    executor = ProcessPoolExecutor(max_workers=n)
    model_path = str(PROJECT_ROOT / conf['model_file'])
    loop = asyncio.get_event_loop()
    fs = [loop.run_in_executor(executor, warm, model_path) for _  in range(n)]
    await asyncio.gather(*fs)

    async def close_executor(app: web.Application) -> None:
        fs = [loop.run_in_executor(executor, clean) for _ in range(n)]
        await asyncio.shield(asyncio.gather(*fs))
        executor.shutdown(wait=True)

    app.on_cleanup.append(close_executor)
    return executor

