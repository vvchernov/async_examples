import asyncio
import argparse
import concurrent.futures
import time

from math_samples import math_sample_sync


async def test_infer_loop_in_pool(pool, number: int = 10):
    loop = asyncio.get_running_loop()

    for i in range(number):
        print(f'>task {i} executing')
        await loop.run_in_executor(pool, math_sample_sync)

async def pool_with_one_task(pool, task_id: int):
    print(f'>task {task_id} executing')
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, math_sample_sync)


async def test_infer_pool_in_loop(pool, number: int = 10):
    coros = [pool_with_one_task(pool, i) for i in range(number)]
    await asyncio.gather(*coros)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10,
                        help="Number of coroutines to async")

    return parser.parse_args()


def main():
    args = parse_args()

    start = time.perf_counter()
    math_sample_sync()
    end = time.perf_counter()
    print("PURE TIME OF ONE COROUTINE:", end - start, "s")

    start = time.perf_counter()
    for i in range(args.number):
        math_sample_sync(i)
    end = time.perf_counter()
    print(f"PURE TIME OF LOOP WITH {args.number} COROUTINES:", end - start, "s")

    pool_map = {
        "THREAD": concurrent.futures.ThreadPoolExecutor,
        "PROCESS": concurrent.futures.ProcessPoolExecutor,
    }

    for pool_type in ["PROCESS", "THREAD"]:
        print("\n----------------------------------------------------\n")
        pool = pool_map[pool_type]()

        print(f"ASYNCIO GATHER WITH {pool_type} POOL")
        start = time.perf_counter()
        asyncio.run(test_infer_pool_in_loop(pool, args.number))
        end = time.perf_counter()
        print("FULL TIME:", end - start, "s")
        print("TIME PER COROUTINE:", (end - start)/args.number, "s")

        print("\n----------------------------------------------------\n")

        print(f"ASYNCIO RUN IN EXECUTOR IN {pool_type} POOL")
        start = time.perf_counter()
        asyncio.run(test_infer_loop_in_pool(pool, args.number))
        end = time.perf_counter()
        print("FULL TIME:", end - start, "s")
        print("TIME PER COROUTINE:", (end - start)/args.number, "s")


if __name__ == "__main__":
    main()
