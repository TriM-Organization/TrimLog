import TrimLog
from TrimLog import object_constants
from TrimLog import log__init__, logger

# import test1
# from loggerT.TriMOLogger import *

osc = object_constants.ObjectStateConstant()
osc.isLoggingUsing = False

pm = TrimLog.PipManage(True, True, 40)
pm.detecting_setting(requirements_path="requirements.txt")
osc.dp("dp" + str(pm.pip_detect()))

osc.get_console(logger.console)
osc.dp("dp: 666")

log__init__(osc, pm)
logger.show_position = True
logger.include_release_info = True
logger.baseinfo_shower()

logger.info("nothing")

osc.isLoggingUsing = True

pm.is_install_pip = False
pm.is_detect_pip = False
log__init__(osc, pm)

logger.info("a")
logger.license_shower(
    "libA", "GPL3.0", "Copyright 2023 xxx", "v0.0.1", "This lib is xxx.", True
)
logger.include_release_info = True
logger.baseinfo_shower()

logger.print_level = TrimLog.CRITICAL
logger.set_default_weight()
logger.info("b")
logger.critical("c")

logger.print_level = TrimLog.INFO
logger.set_default_weight()
logger.info(logger.default_value_return())
