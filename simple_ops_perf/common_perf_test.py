import argparse

#from data_container_perf_test import data_container_perf_test
from other_perf_test import other_perf_test
from torch_perf_test import torch_perf_test


def parse_args():
  parser = argparse.ArgumentParser(description="Different tests to check performance on micro level")
  # parser.add_argument(
  #   "-d", "--data", action="store_true", default=False,
  #   help="Switch on data container tests"
  # )
  parser.add_argument(
    "-to", "--torch", action="store_true", default=False,
    help="Switch on torch tests"
  )
  parser.add_argument(
    "-o", "--others", action="store_true", default=False,
    help="Switch on others tests"
  )
  parser.add_argument(
    "-t", "--test_type", type=str, default="simple",
    help="Subtype of set of tests"
  )
  parser.add_argument(
    "-op", "--op_type", type=str, default=None,
    help="Operation type. It is described specific conditions for specified tested operation"
         "Currently it is used by torch test only"
  )
  parser.add_argument(
    "-dev", "--device", type=str, default="cpu",
    help="Device for torch tensors"
  )

  return parser.parse_args()


def main():
  args = parse_args()
  # if args.data:
  #   data_container_perf_test(args.test_type)
  if args.torch:
    torch_perf_test(args.test_type, args.op_type, args.device)
  if args.others:
    other_perf_test(args.test_type)


if __name__ == '__main__':
  main()
