import os
from hunter import trace, StackPrinter
from xunter import CallPrinterProfile, StackPrinterProfile
trace(
    depth_lt=int(os.environ.get('XUNTER_DEPTH_LT', 20)),
    stdlib=False,
    #action=CallPrinterProfile
    action=StackPrinterProfile
)


a = 1

def c():
    import time
    time.sleep(3)

def b(cnt):
    import time
    time.sleep(cnt)
    c()

b(2)
