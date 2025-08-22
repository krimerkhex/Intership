import requests
from aiohttp import ClientSession
import time
import threading
from multiprocessing import Process
import asyncio

# url = "http://www.skuad-dev.nots-fns.ru/api/info"
url = "http://ya.ru"
REQUEST_COUNT = 10
SEQUENCE = range(REQUEST_COUNT)


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} execution time: {elapsed:.2f} seconds")
        return elapsed

    return wrapper


def a_timer_decorator(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} execution time: {elapsed:.2f} seconds")
        return elapsed

    return wrapper


def execution_factory(method: str):
    """
    methods: 'sync', 'async', 'multiprocess', 'multithread'
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            match method:
                case 'async':
                    return asyncio.run(async_execution(func, *args, **kwargs))
                case 'multiprocess':
                    return multiprocess_execution(func, *args, **kwargs)
                case 'multithread':
                    return multithread_execution(func, *args, **kwargs)
                case _:
                    return sync_execution(func, *args, **kwargs)

        return wrapper

    return decorator


@timer_decorator
def sync_execution(func, *args, **kwargs):
    for _ in range(REQUEST_COUNT):
        func(*args, **kwargs)


@a_timer_decorator
async def async_execution(func, *args, **kwargs):
    async with ClientSession() as session:
        tasks = [func(session) for _ in SEQUENCE]
        await asyncio.gather(*tasks)


@timer_decorator
def multiprocess_execution(func, *args, **kwargs):
    processes = [Process(target=func) for _ in SEQUENCE]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


@timer_decorator
def multithread_execution(func, *args, **kwargs):
    threads = [threading.Thread(target=func) for _ in SEQUENCE]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def ping_skuad_dev():
    response = requests.post(url=url)
    return response.status_code


async def a_ping_skuad_dev(session: ClientSession):
    async with session.post(url=url) as response:
        return response.status


if __name__ == "__main__":
    sync_runner = execution_factory('sync')(ping_skuad_dev)
    async_runner = execution_factory('async')(a_ping_skuad_dev)
    mp_runner = execution_factory('multiprocess')(ping_skuad_dev)
    mt_runner = execution_factory('multithread')(ping_skuad_dev)

    sync_runner()
    async_runner()
    mp_runner()
    mt_runner()
