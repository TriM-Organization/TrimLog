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

# 实战第一步：import
import TrimLog
from TrimLog import object_constants
from TrimLog import log__init__, logger

# 实战第二步：OSC实例化
osc = object_constants.ObjectStateConstant()
osc.isLoggingUsing = False  # 设置osc的logging控制（相当于整个项目初始状态）
osc.project_name = "Test Project"  # 你这个项目叫什么
osc.version = "v0.1.2334"  # 你这个项目的版本

# 实战第三步：PM实例化
pm = TrimLog.PipManage(True, True, 40)  # 自动检测，自动安装，最多40个库输出到logger

# 设置目标依赖库用于检测
# pm.detecting_setting(requirements_path="requirements.txt")
osc.dp("dp" + str(pm.pip_detect()))  # dp示例（现在是print函数输出）

osc.set_console(logger.console)  # dp示例（传入console）
osc.dp("dp: 666")  # dp示例（现在是rich的print函数输出）

# 实战第四步：logger__init__()前设置参数（这一步放在logger__init__()后面也可以）
logger.show_position = True  # 显示申请代码的位置
logger.include_release_info = True  # Release 模式
# logger.include_headline = False

# 实战第五步：logger__init__()
log__init__(osc, pm)

logger.suffix = ".abc"  # 设置文件后缀

logger.baseinfo_shower()  # 如果上面Release为True，这里就会输出运行平台信息

logger.info("nothing")  # 这一条信息不会输出，因为OSC设置了Logging为False，并且被传入参数了

osc.isLoggingUsing = True  # 重新设置OSC

pm.is_install_pip = False  # 重新设置PM
pm.is_detect_pip = False
log__init__(osc, pm)  # 重新调整参数实例化（这几个步骤不需要，而且如果你想在程序运行过程中某一行关闭logger，那你可以用:
# logger.is_logging = False

logger.include_headline = False  # 没啥用，但你可以在logger__init__()前面使用这个来尝试关闭headline。
logger.info("a")  # 正常输出，因为上面logger__init__()把带了新参数的OSC送进去了。
logger.license_shower(
    "libA", "GPL3.0", "Copyright 2023 xxx", "v0.0.1", "This lib is xxx."
)  # 正常输出
logger.include_release_info = True  # 没用，因为上面已经设过一遍了
logger.baseinfo_shower()  # 正常输出

logger.set_print_level = TrimLog.CRITICAL  # 设置print等级
logger.info("b")  # 不输出
logger.critical("c")  # 输出

logger.set_print_level = TrimLog.INFO  # 设回来
logger.info(logger.default_value_return())  # 正常输出

# 实战第六步：设置tips_list

logger.tips_list = [{"position": "test.py:91 in <module>",  # 传入参数
                     "error_text": "ZeroDivisionError: division by zero",
                     "tips": "除数为0了，你可以：1.  xxxx; 2.xxxx"}]

print(5 / 0)  # 91行抛错
