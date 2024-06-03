import asyncio
import argparse
import time

from math_samples import math_sample_sync, math_sample_async


async def cpu_coro_async(coro_id: int):
    print(f'>task {coro_id} executing')
    await math_sample_async()


async def cpu_coro_sync(coro_id: int):
    print(f'>task {coro_id} executing')
    math_sample_sync()


async def cpu_coro_embed(coro_id: int):
    print(f'>task {coro_id} executing')
    sum(i * i for i in range(10**7))


coro_map = {
    "async": cpu_coro_async,
    "sync": cpu_coro_sync,
    "embed": cpu_coro_embed,
}


async def test_infer(coro_type: str, number = 10):
    runner = coro_map[coro_type]
    # create many coroutines
    coros = [runner(i) for i in range(number)]
    # run the tasks
    await asyncio.gather(*coros)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10,
                        help="Number of coroutines to async",)

    return parser.parse_args()


def main():
    args = parse_args()

    start = time.perf_counter()
    math_sample_sync()
    end = time.perf_counter()
    print("PURE TIME:", end - start)\

    print("ASYNCIO GATHER WITH ASYNC MATHS")
    start = time.perf_counter()
    asyncio.run(test_infer("async", args.number))
    end = time.perf_counter()
    print("FULL TIME:", end - start, "s")
    print("TIME PER COROUTINE:", (end - start)/args.number, "s")

    print("ASYNCIO GATHER WITH SYNC MATHS")
    start = time.perf_counter()
    asyncio.run(test_infer("sync", args.number))
    end = time.perf_counter()
    print("FULL TIME:", end - start, "s")
    print("TIME PER COROUTINE:", (end - start)/args.number, "s")

    print("ASYNCIO GATHER WITH EMBED MATHS")
    start = time.perf_counter()
    asyncio.run(test_infer("embed", args.number))
    end = time.perf_counter()
    print("FULL TIME:", end - start, "s")
    print("TIME PER COROUTINE:", (end - start)/args.number, "s")


if __name__ == "__main__":
    main()
