import timeit
import torch

from typing import List, Optional

from .init_test import init_list_of_tensors, init_list_of_lists


def torch_stack(length: int = 10, batch: int = 10):
  torch_list = init_list_of_tensors(length, batch)
  a = torch.stack(torch_list)


def torch_from_list_of_lists(length: int = 10, batch: int = 10):
  list_of_lists = init_list_of_lists(length, batch)
  a = torch.tensor(list_of_lists)


def torch_stack_ready(torch_list: List[torch.Tensor]):
  a = torch.stack(torch_list)


def torch_from_ready_list_of_lists(list_of_lists: List[List[float]]):
  a = torch.tensor(list_of_lists)


def time_it(pass_str: str, setup_str: str = "", num_loop=1000000):
    time_sec = timeit.timeit(
        pass_str,
        setup=setup_str,
        number=num_loop,
        globals=globals(),
    )
    print(1e9 * time_sec / num_loop, "ns")


def base_stack_test():
  num_loop = {
    10: 100000,
    100: 10000,
    1000: 1000,
    32000: 100,
  }
  for length in [10, 100, 1000, 32000]:
    print(f"TORCH STACK BATCH 10 LENGTH {length}")
    time_it(f"torch_stack(length={length})", num_loop=num_loop[length])
    print(f"TORCH FROM LIST OF LISTS BATCH 10 LENGTH {length}")
    time_it(f"torch_from_list_of_lists(length={length})", num_loop=num_loop[length])

    print()


def stack_ready_test():
  num_loop = {
    10: 100000,
    100: 10000,
    1000: 1000,
    32000: 100,
  }
  for length in [10, 100, 1000, 32000]:
    print(f"TORCH STACK READY BATCH 10 LENGTH {length}")
    time_it(
      "torch_stack_ready(a)",
      f"a = init_list_of_tensors(length={length})",
      num_loop=num_loop[length],
    )
    print(f"TORCH FROM READY LIST OF LISTS BATCH 10 LENGTH {length}")
    time_it(
      "torch_from_ready_list_of_lists(a)",
      f"a = init_list_of_lists(length={length})",
      num_loop=num_loop[length],
    )

    print()


def stack_batch_test():
  for batch in [10, 25, 50, 100]:
    print(f"TORCH STACK BATCH {batch} LENGTH 10")
    time_it(f"torch_stack(batch={batch})", num_loop=100000)
    print(f"TORCH FROM LIST OF LISTS BATCH {batch} LENGTH 10")
    time_it(f"torch_from_list_of_lists(batch={batch})", num_loop=100000)

    print()


def stack_test(op_type: Optional[str] = None):
  if op_type == "batch":
    stack_batch_test()
  elif op_type == "ready":
    stack_ready_test()
  else:  # None
    base_stack_test()
