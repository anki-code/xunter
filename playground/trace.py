import os
from hunter import trace
from xunter import CallPrinterProfile, StackPrinterProfile

trace(
    depth_lt=int(os.environ.get('XUNTER_DEPTH_LT', 20)),
    stdlib=False,
    #action=CallPrinterProfile
    action=StackPrinterProfile
)



if __name__ == '__main__':
    from aaa.bbb import b
    b(2)
