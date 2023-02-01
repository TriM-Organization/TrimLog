# Exceptions
class NoSettings(BaseException):  # PIP管理设置参数为空
    pass


class OverSettings(BaseException):  # PIP管理设置参数过多
    pass
