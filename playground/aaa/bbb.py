"""Some code to play with."""

myint = 1

class PlayWithMe:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello {self.name}")

def wait3():
    import time
    print('Wait 3')
    time.sleep(3)

def wait(cnt):
    import time
    print(f'Wait {cnt}')
    time.sleep(cnt)
    wait3()