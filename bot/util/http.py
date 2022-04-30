import aiohttp
import asyncio

from functools import wraps


def cache(maxsize=128):
    cache = {}

    def decorator(func):
        @wraps(func)
        def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                return func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache:
                return cache[key]

            res = func(*args, **kwargs)

            if len(cache) > maxsize:
                del cache[list(cache.keys())[0]]
                cache[key] = res

            return res

        return inner

    return decorator


def async_cache(maxsize=128):
    cache = {}

    def decorator(func):
        @wraps(func)
        async def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                return await func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache:
                return cache[key]

            res = await func(*args, **kwargs)

            if len(cache) > maxsize:
                del cache[list(cache.keys())[0]]
                cache[key] = res

            return res

        return inner

    return decorator


_loop = asyncio.get_event_loop()


class _Session:
    def __init__(self):
        self.session = _loop.run_until_complete(self._get_session())

    async def _get_session(self):
        return aiohttp.ClientSession()

    def __del__(self):
        if not self.session.closed:
            _loop.run_until_complete(self.session.close())


_session_instance = _Session()
http = _session_instance.session


@async_cache()
async def query(url, method="get", res_method="text", *args, **kwargs):
    async with getattr(session, method.lower())(url, *args, **kwargs) as res:
        return await getattr(res, res_method)()


async def get(url, *args, **kwargs):
    return await query(url, "get", *args, **kwargs)


async def post(url, *args, **kwargs):
    return await query(url, "post", *args, **kwargs)
