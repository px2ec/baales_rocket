
from time import *

import brocketd

print "hello"

_brdc = brocketd.bRocketD()

_brdc.scanDevices()

_brdc.start()

sleep(30)

_brdc.terminate()
