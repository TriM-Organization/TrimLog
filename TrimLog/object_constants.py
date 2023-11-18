# -*- coding: utf-8 -*-
"""日志消息处理 OSC项目常数模块

本日志功能拷贝并修改自 万花（我的世界指令IDE）

引用协议：
版权所有© 全体 万花 作者

   Copyright 2022 all the developers of Kaleido

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
继承协议：
版权所有© 全体 万花项目 和 睿乐组织 作者

   Copyright 2022-2023 all the developers of Kaleido and Trim Organization

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
"""

import builtins
from typing import Union, Iterable, Optional,Callable
import rich.console

from .utils import tuple_version_2_string_version, string_version_2_tuple_version


class ObjectStateConstant(builtins.object):
    def __init__(
        self,
        is_debugging: bool = True,
        logging_project_name: str = "",
        logging_project_version: Union[str, Iterable] = (0, 0, 1),
        is_logging: bool = True,
        is_this_a_release: bool = False,
        logging_exit_exec:Callable = lambda x:None,
        console_width:int = 64,
    ):
        """
        __init__() function. change values after you initialize.
        """
        self.debugging: bool = is_debugging
        self.project_name: str = logging_project_name
        self.version: str = (
            logging_project_version
            if isinstance(logging_project_version, str)
            else tuple_version_2_string_version(logging_project_version)
        )
        self.version_tuple: tuple = (
            tuple(logging_project_version)
            if isinstance(logging_project_version, Iterable)
            else string_version_2_tuple_version(logging_project_version)
        )
        self.ParameterSelection: str = "default=self"

        self.is_logging_using: bool = is_logging

        self.is_release: bool = is_this_a_release

        self.console: Optional[rich.console.Console] = None

        self.exit_execution: Callable = logging_exit_exec

        self.console_width:int = console_width

    def set_console(self, in_console: rich.console.Console) -> None:
        """
        give a logger console object.
        :param in_console: logger console object.
        """
        self.console: Optional[rich.console.Console] = in_console

    def get_is_debug(self) -> bool:
        return self.debugging

    def get_versions(self) -> list:
        return [self.version, self.version_tuple]

    def debugging_print(self, anything) -> None:
        if self.debugging:
            if self.console is not None:
                self.console.print(anything)
            else:
                print(anything)

    def dp(self, anything) -> None:
        if self.debugging:
            if self.console is not None:
                self.console.print(anything)
            else:
                print(anything)
