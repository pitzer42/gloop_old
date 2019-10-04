import asyncio

from unittest.mock import Mock

_loop = None


def sync(coroutine):

    def wrapper(*args, **kwargs):
        global _loop

        if _loop is None:
            _loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop)

        try:
            future = coroutine(*args, **kwargs)
            _loop.run_until_complete(future)
        except RuntimeError:
            future = coroutine(*args, **kwargs)
            asyncio.run_coroutine_threadsafe(future, _loop)

    return wrapper


def make_async_mock(mock: Mock):
    future = asyncio.Future()
    future.set_result(Mock())
    mock.return_value = future
