from others.str_format_test import str_format_test

other_types_list = ["str_format"]


def other_perf_test(type: str):
  assert type in other_types_list,  f"{type} is not in the list: {other_types_list}"

  if type == "str_format":
    str_format_test()
