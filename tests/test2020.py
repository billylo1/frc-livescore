import sys

from testCommon import processYear

error = processYear(2020)
if error:
    sys.exit(1)
