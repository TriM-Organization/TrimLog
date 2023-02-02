# -*- coding: utf-8 -*-
"""日志消息处理 日志常数模块

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
from sys import version_info
from typing import Tuple

from .exceptions import *

# Traceback exception definitions
WIDTH: int = 100
EXTRA_LINES: int = 3
THEME = None
WORD_WRAP: bool = False
SHOW_LOCALS: bool = True
INDENT_GUIDES: bool = True
SUPPRESS = ()
MAX_FRAMES: int = 100

# Headline definitions
# {0}{1}:使用程序名称及版本号，由oc管理
# {2}:logger版本号
HEADLINE_STRUCTURE: str = """ 
{0} {1}
Using TrimLog Library by Apache2.0 License.
Copyright 2022-2023 all the developers of Kaleido and Trim Organization.(FedDragon1, Eilles Wan, bgArray)
Library Version: {2}
"""

# License template
# {0} lib_name; {1} license_name; {2} license_line; {3} lib_version; {4} addition(optional)
LICENSE_STRUCTURE: str = """
Using {0} Library by {1} License.
{2}
Library Version: {3}
{4}
"""

# Weight order
WEIGHT_ORDER = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

# Release template
RELEASE_STRUCTURE = """
running platform: {0}
Python version: {1}
Python cmd version: {2}
Python version info: {3}
program location: {4}
default encoding: {5}
file system encoding: {6}
pip list: {7}
pip check: {8}
"""


# levels_setting
class _Level:
    if version_info[0] != 3:
        raise PythonVersionError
    else:
        DEBUG: Tuple[str, int] = "[bright_cyan][DEBUG][/bright_cyan]", 27
        INFO: Tuple[str, int] = "[green][INFO][/green]", 15
        WARNING: Tuple[str, int] = "[gold3][WARNING][/gold3]", 15
        ERROR: Tuple[str, int] = "[dark_orange3][ERROR][/dark_orange3]", 29
        CRITICAL: Tuple[str, int] = "[red][CRITICAL][/red]", 11
