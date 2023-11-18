# -*- coding: utf-8 -*-
"""日志消息处理 附属功能性组件模块

版权所有© 全体 睿乐组织 作者

   Copyright 2022-2023 all the developers of Trim Organization

   Licensed under the Apache License, Version 2.0 (the 'License');
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0
"""

from typing import Iterable


def string_version_2_tuple_version(string_version_code: str = "0.0.1"):
    return tuple(
        [
            int(i) if i.isnumeric() else int("".join([j for j in i if j.isnumeric()]))
            for i in string_version_code.split(".")
        ]
    )


def tuple_version_2_string_version(tuple_version_code: Iterable[int] = (0, 0, 1)):
    return ".".join([str(i) for i in tuple_version_code])
