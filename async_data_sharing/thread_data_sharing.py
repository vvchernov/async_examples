from threading import Thread, Event
from time import sleep


def var_in_thread_arg():
  event = Event()

  my_var = [1., 2., 3.]

  def test_thread(var):
    while True:
      for i in range(len(var)):
        var[i] += 1
      if event.is_set():
        break
      sleep(.5)
    print('Stop printing:', var)


  t = Thread(target=test_thread, args=(my_var, ))
  t.start()
  while True:
    try:
      print(my_var)
      for i in range(len(my_var)):
        my_var[i] += 0.5
      sleep(1)
    except KeyboardInterrupt:
      event.set()
      break
  t.join()
  print(my_var)


def global_var_in_thread():
    event = Event()

    my_var = [1., 2., 3.]

    def test_thread():
        while True:
            for i in range(len(my_var)):
                my_var[i] += 1
            if event.is_set():
                break
            sleep(.5)
        print('Stop printing:', my_var)


    t = Thread(target=test_thread)
    t.start()
    while True:
      try:
        print(my_var)
        for i in range(len(my_var)):
          my_var[i] += 0.5
        sleep(1)
      except KeyboardInterrupt:
        event.set()
        break
    t.join()
    print(my_var)


def reinit_var():
  event = Event()

  my_var = [1., 2., 3.]

  def test_thread(var):
    while True:
      for i in range(len(var)):
        var[i] += 1
      if event.is_set():
        break
      sleep(.5)
    print('Stop printing:', var)


  t = Thread(target=test_thread, args=(my_var, ))
  t.start()
  while True:
    try:
      print(my_var)
      a = [0.37, 1.37, 2.37]
      my_var = a
      sleep(1)
    except KeyboardInterrupt:
      event.set()
      break
  t.join()
  print(my_var)


def main():
#  var_in_thread_arg()
#  global_var_in_thread()
  reinit_var()


if __name__ == '__main__':
  main()
