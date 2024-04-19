from hunter import trace, Q
from xunter import CallPrinterProfile, StackPrinterProfile

# action=CallPrinterProfile
action = StackPrinterProfile

filters = (
    Q(depth_lt=3),
)

trace(
    *filters,
    stdlib=False,
    action=action
)


if __name__ == '__main__':
    print('start')
    from aaa.bbb import b
    b(2)
    print('done')