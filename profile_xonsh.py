import os
from hunter import trace
from xunter import CallPrinterProfile, StackPrinterProfile

printers = ['stack', 'call']
printer = os.environ.get('XUNTER_PRINTER', 'stack')
if printer == 'call':
    printer = CallPrinterProfile
elif printer == 'stack':
    printer = StackPrinterProfile
else:
    raise Exception('Unknown printer')

trace(
    action=printer,
    depth_lt=int(os.environ.get('XUNTER_DEPTH_LT', 5)),
    stdlib=False,
)

# This is the result from `cat @$(which xonsh)`:
import re
import sys
from xonsh.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

