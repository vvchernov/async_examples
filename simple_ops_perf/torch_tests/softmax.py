import timeit
import torch

from typing import Optional


def init_torch_tensor(batch_size: int = 10, length: int = 10, device: str = "cpu"):
  return torch.rand((batch_size, length,), device=device)


def torch_softmax(ttensor: torch.Tensor):
  a = torch.softmax(ttensor)


def time_it(pass_str: str, setup_str: str = "", num_loop=1000000):
    time_sec = timeit.timeit(
        pass_str,
        setup=setup_str,
        number=num_loop,
        globals=globals(),
    )
    print(1e9 * time_sec / num_loop, "ns")


def base_softmax_test(op_type: Optional[str] = None, device: str = "cpu"):
  if op_type is None:
    lengths = [10, 100, 1000, 100000]
    num_loop = {
      10: 1000000,
      100: 100000,
      1000: 10000,
      100000: 100,
    }
  else:
    length = int(op_type)
    lengths = [length]
    num_loop = {
      length: 1000,
    }

  for length in lengths:
    print(f"TORCH SOFTMAX, BATCH 10, LENGTH {length}")
    time_it(
      f"torch_softmax(a)",
      f"a = init_torch_tensor(length={length}, device={device})",
      num_loop=num_loop[length]
    )

    print()


def softmax_test(op_type: Optional[str] = None, device: str = "cpu"):
  assert op_type is None or op_type.isdigit(), "Length of tensor or None is expected for softmax test"

  base_softmax_test(op_type, device)
