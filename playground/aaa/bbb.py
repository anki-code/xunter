"""Some code to play with."""

myint = 1

class PlayWithMe:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello {self.name}")

def c():
    import time
    time.sleep(3)

def b(cnt):
    import time
    time.sleep(cnt)
    c()