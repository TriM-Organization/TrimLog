# -*- coding: utf-8 -*-

# Exceptions
class NoSettings(BaseException):  # PIP管理设置参数为空
    pass


class OverSettings(BaseException):  # PIP管理设置参数过多
    pass


class PythonVersionError(BaseException):  # python版本不为3
    pass
