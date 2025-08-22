from math import factorial
import time
import threading
from multiprocessing import Pool, cpu_count

SEQUENCE = range(1, 1001)


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} execution time: {elapsed:.2f} seconds")
        return elapsed

    return wrapper


@timer_decorator
def sync_launch():
    for i in SEQUENCE:
        factorial(i)


@timer_decorator
def launch_multiprocess():
    with Pool(cpu_count()) as pool:
        pool.map(factorial, SEQUENCE)


@timer_decorator
def launch_multithreading():
    threads = [threading.Thread(target=factorial, args=[i]) for i in SEQUENCE]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    print("Sync launch: ", sync_launch())
    print("Multiprocess launch: ", launch_multiprocess())
    print("Multithreading launch: ", launch_multithreading())
