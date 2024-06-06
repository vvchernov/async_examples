import concurrent.futures
import argparse
import time

from math_samples import math_sample_sync


def cpu_coro_sync(coro_id: int, result: int):
    print(f'>task {coro_id} executing')
    result = math_sample_sync()


def cpu_coro_embed(coro_id: int, result: int):
    print(f'>task {coro_id} executing')
    result = sum(i * i for i in range(10**7))


coro_map = {
    "sync": cpu_coro_sync,
    "embed": cpu_coro_embed,
}


def test_infer(executor, coro_type: str, number: int = 10):
    runner = coro_map[coro_type]
    futures = []
    parallel_results = {}
    # run the tasks
    for id in range(number):
        parallel_results[id] = []
        futures.append(executor.submit(
            runner,
            id,
            parallel_results[id]
        ))
    # finish tasks
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            print(f"Error parallel generating predictions: {exc}")


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
    for _ in range(args.number):
        math_sample_sync()
    end = time.perf_counter()
    print(f"PURE TIME OF LOOP WITH {args.number} COROUTINES:", end - start, "s")

    executor_map = {
        "THREAD": concurrent.futures.ThreadPoolExecutor,
        "PROCESS": concurrent.futures.ProcessPoolExecutor,
    }

    for pool_type in ["PROCESS", "THREAD"]:
        print("\n----------------------------------------------------\n")
        executor = executor_map[pool_type](args.number)

        print(f"FUTURES {pool_type} POOL WITH SYNC MATHS")
        start = time.perf_counter()
        test_infer(executor, "sync", args.number)
        end = time.perf_counter()
        print("FULL TIME:", end - start, "s")
        print("TIME PER COROUTINE:", (end - start)/args.number, "s")

        print("\n----------------------------------------------------\n")

        print(f"FUTURES {pool_type} POOL WITH EMBED MATHS")
        start = time.perf_counter()
        test_infer(executor, "embed", args.number)
        end = time.perf_counter()
        print("FULL TIME:", end - start, "s")
        print("TIME PER COROUTINE:", (end - start)/args.number, "s")


if __name__ == "__main__":
    main()
