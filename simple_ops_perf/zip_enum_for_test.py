import argparse
import timeit

from numpy import random
from typing import List 


setup_str="""\
n = 100
a = gen_int_list(n)
b = gen_int_list(n)
c = gen_int_list(n)
"""


# ---------------------------------------------------------------
def gen_int_list(n: int = 10):
   return [random.randint(10000) for _ in range(n)]


def zip_test(a: List[int], b: List[int], c: List[int]):
  for a_unit, b_unit, c_unit in zip(a, b, c):
     d = a_unit + b_unit + c_unit


def for_test(a: List[int], b: List[int], c: List[int], n: int = 10):
  for i in range(n):
     d = a[i] + b[i] + c[i]


def enum_test(a: List[int], b: List[int], c: List[int]):
  for i, (a_unit, b_unit,) in enumerate(zip(a, b)):
     d = a_unit + b_unit + c[i]

# ----------------------------------------------------------------


def time_it(pass_str: str, setup_str: str = "", num_loop=1000000):
    time_sec = timeit.timeit(
        pass_str,
        setup=setup_str,
        number=num_loop,
        globals=globals(),
    )
    print(1e9 * time_sec / num_loop, "ns")


def zip_enum_for_test(num_loop=1000000):
  print("ZIP TEST:")
  time_it("zip_test(a, b, c)", setup_str, num_loop)

  print("ENUM TEST:")
  time_it("enum_test(a, b, c)", setup_str, num_loop)

  print("FOR TEST:")
  time_it("for_test(a, b, c, n)", setup_str, num_loop)


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--number", type=int, default=1000000,
                      help="Number of loop iterations")

  return parser.parse_args()


def main():
  args = parse_args()

  zip_enum_for_test(args.number)


if __name__ == '__main__':
  main()
