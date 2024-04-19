"""
This is tracing code playground to understand how it works.
"""

from hunter import trace, Q
from xunter import CallPrinterProfile, StackPrinterProfile

# action = CallPrinterProfile
action = StackPrinterProfile

filters = (
    Q(filename_endswith="bbb.py"),
    Q(depth_lt=10),
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

    from aaa.bbb import PlayWithMe
    pw = PlayWithMe('Bar')
    pw.say_hello()

    pw.new_func = lambda: "Catch me if you can ;)"
    print(pw.new_func())

    print('done')