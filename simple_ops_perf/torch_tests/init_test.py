import timeit
import torch
import numpy as np

from typing import List
from random import randint


def data_list(length: int = 10):
  return [0.1] * length


def init_list_of_lists(length: int = 10, batch: int = 10):
  res_list = []
  for _ in range(batch):
    res_list.append(data_list(length))

  return res_list


def init_list_of_tensors(length: int = 10, batch: int = 10):
  res_list = []
  for _ in range(batch):
    res_list.append(torch.tensor(data_list(length)))

  return res_list


def get_prompt(plen: int = 10, length: int = 10):
  prompt = []
  for _ in range(plen):
    prompt.append(randint(0, length - 1))

  return prompt


def init_from_prompt(prompt: List[int], length: int = 10):
  tokens=torch.tensor(prompt, dtype=torch.long)
  bin_counts = torch.zeros((length + 1,),
                            dtype=torch.long,
                            device=tokens.device)
  bin_counts.scatter_add_(0, tokens, torch.ones_like(tokens))
  bin_counts = bin_counts[:length]
  prompt_mask = bin_counts > 0

  return prompt_mask


def init_list_of_tensors_from_prompts(prompt: List[int], length: int = 10, batch: int = 10):
  res_list = []
  for _ in range(batch):
    res_list.append(init_from_prompt(prompt, length))

  return res_list


def init_from_numpy(prompt: List[int], length: int = 10):
  tokens = np.array(prompt, dtype=np.int64)
  prompt_mask = np.zeros((length + 1,), dtype=bool)
  prompt_mask[tokens] = True
  prompt_mask = list(prompt_mask[:length])

  return prompt_mask


def init_list_of_lists_from_numpy(prompt: List[int], length: int = 10, batch: int = 10):
  res_list = []
  for _ in range(batch):
    res_list.append(init_from_numpy(prompt, length))

  return res_list


def time_it(pass_str: str, setup_str: str = "", num_loop=1000000):
    time_sec = timeit.timeit(
        pass_str,
        setup=setup_str,
        number=num_loop,
        globals=globals(),
    )
    print(1e9 * time_sec / num_loop, "ns")


def init_test():
  num_loop = {
    10: 100000,
    100: 10000,
    1000: 1000,
    32000: 100,
  }
  for length in [10, 100, 1000, 32000]:
    print(f"LIST OF LISTS INIT BATCH 10 LENGTH {length}")
    time_it(f"init_list_of_lists(length={length})", num_loop=num_loop[length])
    print(f"LIST OF TENSORS INIT BATCH 10 LENGTH {length}")
    time_it(f"init_list_of_tensors(length={length})", num_loop=num_loop[length])
    print(f"LIST FROM PROMPT INIT PROMPT 10 BATCH 10 LENGTH {length}")
    time_it(
      f"init_list_of_tensors_from_prompts(prompt = p, length={length})",
      f"p = get_prompt(10, {length})",
      num_loop=num_loop[length],
    )
    print(f"LIST FROM NUMPY INIT PROMPT 10 BATCH 10 LENGTH {length}")
    time_it(
      f"init_list_of_lists_from_numpy(prompt = p, length={length})",
      f"p = get_prompt(10, {length})",
      num_loop=num_loop[length],
    )

    print()

  print()

  for plen in [10, 50, 100, 500]:
    print(f"LIST FROM PROMPT INIT PROMPT {plen} BATCH 10 LENGTH 32000")
    time_it(
      f"init_list_of_tensors_from_prompts(prompt = p, length = 32000)",
      f"p = get_prompt({plen}, length = 32000)",
      num_loop=num_loop[length],
    )
    print(f"LIST FROM NUMPY INIT PROMPT {plen} BATCH 10 LENGTH 32000")
    time_it(
      f"init_list_of_lists_from_numpy(prompt = p, length = 32000)",
      f"p = get_prompt({plen}, length = 32000)",
      num_loop=num_loop[length],
    )

    print()
