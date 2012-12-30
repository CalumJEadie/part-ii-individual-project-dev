"""
Executes `script` in the parent directory of this script.
"""

import sys
from show import show

if len(sys.argv) < 2:
    sys.exit("Usage: %s script" % sys.argv[0])

script = sys.argv[1]

print "before"

show(script)
print open(script).read()

execfile(script)

print "after"