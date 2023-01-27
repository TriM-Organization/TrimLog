import loggerT
from loggerT import objectConstant
from loggerT import log__init__, logger
# import test1
# from loggerT.TriMOLogger import *

osc_ = objectConstant.ObjectStateConstant()
osc_.isLoggingUsing = False

pm = loggerT.PipManage(True, 40)
pm.detecting_setting(requirements_path="requirements.txt")
# print(pm.pip_detect())
log__init__(osc_, pm)
logger.include_release_info = True
logger.baseinfo_shower()

logger.info("nothing")

osc_.isLoggingUsing = True

log__init__(osc_, pm)

logger.info("a")
logger.license_shower("libA", "GPL3.0", "Copyright 2023 xxx", "v0.0.1", "This lib is xxx.", True)
logger.include_release_info = True
logger.baseinfo_shower()

logger.print_level = loggerT.CRITICAL
logger.set_default_weight()
logger.info("b")
logger.critical("c")
