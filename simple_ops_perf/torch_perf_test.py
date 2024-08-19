from typing import Optional

from torch_tests.init_test import init_test
from torch_tests.stack import stack_test
from torch_tests.softmax import softmax_test

torch_types_list = ["init", "stack", "softmax"]


def torch_perf_test(type: str, op_type: Optional[str] = None, device: str = "cpu"):
  if type == "init":
    init_test()
  elif type == "stack":
    stack_test(op_type)
  elif type == "softmax":
    softmax_test(op_type, device)
  else:
    raise RuntimeError(
      f"Torch test of type {type} is not supported."
      f"{torch_types_list} types are evailable"
    )
