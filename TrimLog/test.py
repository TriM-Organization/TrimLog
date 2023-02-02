# -*- coding: utf-8 -*-
"""日志消息处理 示例模块

本日志功能拷贝并修改自 万花（我的世界指令IDE）

引用协议：
版权所有© 全体 万花 作者

   Copyright 2022 all the developers of Kaleido

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
继承协议：
版权所有© 全体 万花项目 和 睿穆组织 作者

   Copyright 2022-2023 all the developers of Kaleido and Trim Organization

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
"""

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
