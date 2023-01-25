import loggerT
from loggerT import objectConstant
from loggerT import log__init__, logger
# import test1
# from loggerT.TriMOLogger import *

osc_ = objectConstant.ObjectStateConstant()
osc_.isLoggingUsing = False

log__init__(osc_)

logger.info("a")

osc_.isLoggingUsing = True

log__init__(osc_)

logger.info("a")
logger.license_shower("libA", "GPL3.0", "Copyright 2023 xxx", "v0.0.1", "This lib is xxx.", True)

logger.printLevel = loggerT.CRITICAL
logger.set_default_weight()
logger.info("b")
logger.critical("c")
