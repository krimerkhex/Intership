import requests
from aiohttp import ClientSession
import time
import threading
from multiprocessing import Process
import asyncio

url = "http://www.skuad-dev.nots-fns.ru/api/info"
REQUEST_COUNT = 10


def ping_skuad_dev():
    response = requests.post(url=url)
    return response.status_code


async def a_ping_skuad_dev(session: ClientSession):
    async with session.post(url=url) as response:
        return response.status


def sync_launch() -> float:
    start = time.time()
    for _ in range(REQUEST_COUNT):
        ping_skuad_dev()
    return time.time() - start


async def async_launch() -> float:
    async with ClientSession() as session:
        tasks = [a_ping_skuad_dev(session) for _ in range(REQUEST_COUNT)]
        start = time.time()
        await asyncio.gather(*tasks)
    return time.time() - start


def launch_multiprocess() -> float:
    processes = [Process(target=ping_skuad_dev) for _ in range(REQUEST_COUNT)]
    start = time.time()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    return time.time() - start


def launch_multithreading() -> float:
    threads = [threading.Thread(target=ping_skuad_dev) for _ in range(REQUEST_COUNT)]
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return time.time() - start


if __name__ == "__main__":
    print("Sync launch: ", sync_launch())
    print("Async launch: ", asyncio.run(async_launch()))
    print("Multiprocess launch: ", launch_multiprocess())
    print("Multithreading launch: ", launch_multithreading())
