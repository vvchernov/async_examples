import timeit

from random import randint


def str_format(input):
  foo = f"{input}"


def time_it(pass_str: str, setup_str: str = "", num_loop=1000000):
    time_sec = timeit.timeit(
        pass_str,
        setup=setup_str,
        number=num_loop,
        globals=globals(),
    )
    print(1e9 * time_sec / num_loop, "ns")


def str_format_test():
  print("FORMAT STRING WITH STRING")
  time_it("str_format('Dummy string')")

  print()

  print("FORMAT STRING WITH INTEGER")
  time_it("str_format(137)")

  for n in [1, 5, 10, 100, 1000]:
    print()
    print(f"FORMAT STRING WITH LIST OF {n} INTEGERS")
    ints = [randint(0, 1000) in range(n)]
    time_it(f"str_format({ints})")
