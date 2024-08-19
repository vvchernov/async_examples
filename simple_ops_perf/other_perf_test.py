from others.str_format_test import str_format_test

other_types_list = ["str_format"]


def other_perf_test(type: str):
  if type == "str_format":
    str_format_test()
  else:
    raise RuntimeError(
      f"Other test of type {type} is not supported. "
      f"{other_types_list} types are evailable"
    )
