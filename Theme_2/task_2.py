from math import factorial
import requests
from aiohttp import ClientSession
import time
import threading
from multiprocessing import Process, Pool, cpu_count
import asyncio


def sync_launch() -> float:
    start = time.time()
    for i in range(1, 1001):
        factorial(i)
    return time.time() - start


def launch_multiprocess() -> float:
    start = time.time()
    with Pool(cpu_count()) as pool:
        pool.map(factorial, range(1, 1001))
    return time.time() - start


def launch_multithreading() -> float:
    threads = [threading.Thread(target=factorial, args=[i]) for i in range(1, 1001)]
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return time.time() - start


if __name__ == "__main__":
    print("Sync launch: ", sync_launch())
    print("Multiprocess launch: ", launch_multiprocess())
    print("Multithreading launch: ", launch_multithreading())
