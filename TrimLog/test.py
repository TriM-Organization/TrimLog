import TrimLog
from TrimLog import object_constants
from TrimLog import log__init__, logger

# import test1
# from loggerT.TriMOLogger import *

osc = object_constants.ObjectStateConstant()
osc.isLoggingUsing = False
osc.project_name = "Test Project"
osc.version = "v0.1.2334"

pm = TrimLog.PipManage(True, True, 40)
# pm.detecting_setting(requirements_path="requirements.txt")
osc.dp("dp" + str(pm.pip_detect()))

osc.get_console(logger.console)
osc.dp("dp: 666")

logger.show_position = True
logger.include_release_info = True  # Release 模式
# logger.include_headline = False
log__init__(osc, pm)

logger.suffix = ".abc"

logger.baseinfo_shower()

logger.info("nothing")

osc.isLoggingUsing = True

pm.is_install_pip = False
pm.is_detect_pip = False
log__init__(osc, pm)

logger.include_headline = False
logger.info("a")
logger.license_shower(
    "libA", "GPL3.0", "Copyright 2023 xxx", "v0.0.1", "This lib is xxx."
)
logger.include_release_info = True
logger.baseinfo_shower()

logger.set_print_level = TrimLog.CRITICAL
logger.info("b")
logger.critical("c")

logger.set_print_level = TrimLog.INFO
logger.info(logger.default_value_return())

logger.tips_list = [{"position": "test.py:58 in <module>",
                     "error_text": "ZeroDivisionError: division by zero",
                     "tips": "除数为0了，你可以：1.  xxxx; 2.xxxx"}]

print(5 / 0)
