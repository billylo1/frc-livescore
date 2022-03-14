import sys

from testCommon import processYear

error = processYear(2021)
if error:
    sys.exit(1)
