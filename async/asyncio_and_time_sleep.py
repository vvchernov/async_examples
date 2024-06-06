import asyncio
import argparse
import time


async def cpu_coro_asyncio_sleep(coro_id: int, duration: float = 1.0):
    print(f'>task {coro_id} executing')
    await asyncio.sleep(duration)


async def cpu_coro_time_sleep(coro_id: int, duration: float = 1.0):
    print(f'>task {coro_id} executing')
    time.sleep(duration)


coro_map = {
    "asyncio": cpu_coro_asyncio_sleep,
    "time": cpu_coro_time_sleep,
}


async def test_infer(coro_type: str, number: int = 10, duration: float = 1.0):
    runner = coro_map[coro_type]
    # create many coroutines
    coros = [runner(i, duration) for i in range(number)]
    # run the tasks
    await asyncio.gather(*coros)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int, default=10,
                        help="Number of coroutines to async")
    parser.add_argument("-d", "--duration", type=float, default=1.0,
                        help="Sleep duration in seconds")

    return parser.parse_args()


def main():
    args = parse_args()

    print(f"PURE TIME OF ONE COROUTINE: {args.duration} s")
    print(f"PURE TIME OF LOOP WITH {args.number} COROUTINES {args.number * args.duration} s")

    print("\n----------------------------------------------------\n")

    print("ASYNCIO SLEEP")
    start = time.perf_counter()
    asyncio.run(test_infer("asyncio", args.number))
    end = time.perf_counter()
    print("FULL TIME:", end - start, "s")
    print("TIME PER COROUTINE:", (end - start)/args.number, "s")

    print("\n----------------------------------------------------\n")

    print("TIME SLEEP")
    start = time.perf_counter()
    asyncio.run(test_infer("time", args.number))
    end = time.perf_counter()
    print("FULL TIME:", end - start, "s")
    print("TIME PER COROUTINE:", (end - start)/args.number, "s")


if __name__ == "__main__":
    main()
