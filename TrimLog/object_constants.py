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
版权所有© 全体 万花项目 和 睿穆组织 作者

   Copyright 2022-2023 all the developers of Kaleido and Trim Organization

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
"""

import builtins
import rich.console


class ObjectStateConstant(builtins.object):
    def __init__(self):
        """
        __init__() function. change values after you initialize.
        """
        self.debugging = True
        self.project_name = ""
        self.version = "v0.0.1"
        self.version_tuple = (0, 0, 1)
        self.ParameterSelection = "default=self"

        self.isLoggingUsing = True

        self.isRelease = False

        self.console = None

    def set_console(self, in_console: rich.console.Console) -> None:
        """
        give a logger console object.
        :param in_console: logger console object.
        """
        self.console: rich.console.Console = in_console

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
