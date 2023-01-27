# -*- coding: utf-8 -*-
"""日志消息处理

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

from __future__ import annotations

from rich.traceback import Traceback
from rich.console import Console
import rich.traceback
from typing import Literal, Optional, Type, TypeVar
from types import TracebackType
import time
import sys
import os
import atexit
import platform
from .logConstant import *
from .objectConstant import *

__version__: str = "v0.4.5"
T = TypeVar("T")
L = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class _Level:
    DEBUG: tuple[str, int] = "[bright_cyan][DEBUG][/bright_cyan]", 27
    INFO: tuple[str, int] = "[green][INFO][/green]", 15
    WARNING: tuple[str, int] = "[gold3][WARNING][/gold3]", 15
    ERROR: tuple[str, int] = "[dark_orange3][ERROR][/dark_orange3]", 29
    CRITICAL: tuple[str, int] = "[red][CRITICAL][/red]", 11


class Logger:
    instance: Logger = None
    str_start_time: str = time.strftime("%Y-%m-%d %H_%M_%S")
    console: Console = Console()
    __suffix = "dsl"
    isLogging_ = True
    MaxLogCount: int = 20

    def __new__(cls,
                isLogging: bool = True,
                isPrint: bool = True,
                isWrite: bool = True,
                printLevel: L = "DEBUG",
                writeLevel: L = "INFO",
                isHeadline: bool = True,
                isLicenseLine: bool = True,
                headlineLevel: L = "WARNING",
                licenseLevel: L = "WARNING",
                maxLogCount: int = 20,
                isRelease: bool = False,
                isShowPosition: bool = True,
                ) -> Logger:
        if cls.instance is not None:
            return cls.instance
        cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
            self,
            isLogging: bool = True,
            isPrint: bool = True,
            isWrite: bool = True,
            printLevel: L = "DEBUG",
            writeLevel: L = "INFO",
            isHeadline: bool = True,
            isLicenseLine: bool = True,
            headlineLevel: L = "WARNING",
            licenseLevel: L = "WARNING",
            maxLogCount: int = 20,
            isRelease: bool = False,
            isShowPosition: bool = True,
    ) -> None:
        self.log_text: str = ""

        # 总开关，根据OSC
        self.isLogging = isLogging
        Logger.isLogging_ = isLogging

        # 是否需要输出一些开发时不需要输出的内容；但是用户使用时需要输出的内容
        # 也就是Release版本到不同平台不同版本Python下需要增加的一些信息
        self.isRelease = isRelease

        # 是否需要console.log(end="....")
        self.isShowPosition: bool = isShowPosition

        # 头声明；协议声明
        self.isHeadline: bool = isHeadline
        self.isLicenseLine: bool = isLicenseLine
        self.headlineLevel: L = headlineLevel
        self.licenseLevel: L = licenseLevel

        # 打印到屏幕设置；写入到文件设置
        self.isPrint: bool = isPrint
        self.isWrite: bool = isWrite
        self.printLevel: L = printLevel
        self.writeLevel: L = writeLevel
        self.print_default_weight = WEIGHT_ORDER.get(self.printLevel)
        self.write_default_weight = WEIGHT_ORDER.get(self.writeLevel)

        # 文件最多保存多少个后开始删除
        self.maxLogCount: int = maxLogCount
        Logger.MaxLogCount = self.maxLogCount

        # 初始化展示headline
        self.headline_shower()

    def log(self,
            info: T,
            level: L,
            upLine: int = None,
            upFunction: str = None,
            upModel: str = None) -> T:
        if self.isLogging:
            style: Optional[str]
            style_len: Optional[int]
            style, style_len = getattr(_Level, level, (None, None))
            if style is None or style_len is None:
                raise TypeError(
                    f"等级应为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 或 'CRITICAL' 中的一种，而非 '{level}'"
                )

            level_weight = WEIGHT_ORDER.get(level)

            if upLine is None and upFunction is None and upModel is None:
                back_frame = sys._getframe().f_back
                upModel: str = os.path.basename(back_frame.f_code.co_filename)
                upFunction: str = back_frame.f_code.co_name
                upLine: int = back_frame.f_lineno

            if self.isShowPosition:
                end_with = "{0}-{1}: {2}\n".format(upModel, upFunction, str(upLine))

            if self.isWrite:
                if level_weight >= self.write_default_weight:
                    if self.isShowPosition:
                        e_w = end_with.replace("\n", "")
                        self.log_text += f"{time.strftime('[%H:%M:%S]')} [{level}] [{e_w}] {info}\n"
                    else:
                        self.log_text += f"{time.strftime('[%H:%M:%S]')} [{level}] {info}\n"

            length = 12 + style_len

            if self.isPrint:
                if level_weight >= self.print_default_weight:
                    if self.isShowPosition:
                        e_w = " <" + end_with.replace("\n", "") + "> "
                        add = style + e_w
                        self.console.log(f"{add:<{length}}{info!s:<10}")
                    else:
                        self.console.log(f"{style:<{length}}{info!s:<10}")

        return info

    def set_default_weight(self):
        self.print_default_weight = WEIGHT_ORDER.get(self.printLevel)
        self.write_default_weight = WEIGHT_ORDER.get(self.writeLevel)

    def debug(self, debug: T) -> T:
        back_frame = sys._getframe().f_back
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        return self.log(debug, "DEBUG", back_line_number, back_func_name, back_file_name)

    def info(self, info: T) -> T:
        back_frame = sys._getframe().f_back
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        return self.log(info, "INFO", back_line_number, back_func_name, back_file_name)

    def warning(self, warning: T) -> T:
        back_frame = sys._getframe().f_back
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        print(back_func_name)
        print(back_line_number)
        return self.log(warning, "WARNING", back_line_number, back_func_name, back_file_name)

    def error(self, error: T) -> T:
        back_frame = sys._getframe().f_back
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        return self.log(error, "ERROR", back_line_number, back_func_name, back_file_name)

    def critical(self, critical: T) -> T:
        back_frame = sys._getframe().f_back
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        return self.log(critical, "CRITICAL", back_line_number, back_func_name, back_file_name)

    def write(self, text: str) -> None:
        if self.isLogging:
            self.log_text += text

    def headline_shower(self):
        global __version__
        if self.isHeadline:
            self.console.rule("[bold red]Headline")
            self.log(HEADLINE_STRUCTURE.format(__version__), self.headlineLevel)

    def baseInfo_shower(self):
        global py_version, py_sys_version, py_sys_version_info, pip_list, \
            pip_check, default_encoding, running_path, file_system_encoding, py_platform
        if self.isRelease and self.isLogging:
            self.console.rule("[bold red]BaseInfo")
            self.log(RELEASE_STRUCTURE.format(py_platform,
                                              py_version,
                                              py_sys_version,
                                              py_sys_version_info,
                                              running_path,
                                              default_encoding,
                                              file_system_encoding,
                                              pip_list,
                                              pip_check), self.headlineLevel)

    def license_shower(self, lib_name: str,
                       license_name: str,
                       license_line: str,
                       lib_version: str,
                       addition: str = "",
                       isStartLine: bool = True):
        if self.isLicenseLine and self.isLogging:
            license_thing = LICENSE_STRUCTURE.format(lib_name, license_name, license_line, lib_version, addition)
            if isStartLine:
                self.console.rule("[bold red]License for " + lib_name)
            self.log(license_thing, self.licenseLevel)

    @staticmethod
    @atexit.register
    def save() -> None:
        if Logger.isLogging_:
            try:
                list_of_files = os.listdir("logs")
            except FileNotFoundError:
                os.makedirs("logs")
            else:
                full_path = ["logs/{0}".format(x) for x in list_of_files]

                if len(list_of_files) >= Logger.MaxLogCount:
                    oldest_file = min(full_path, key=os.path.getctime)
                    logger.log(f"移除最早的日志：{oldest_file!r}", INFO)
                    os.remove(oldest_file)

            try:
                path = os.path.abspath("./logs/")
                if not os.path.exists(path):
                    os.makedirs("./logs/")

                if not Logger.instance.log_text:
                    Logger.instance.log(f"日志未保存：空日志文件", "WARNING")
                    return

                if Logger.instance.log_text == "":
                    Logger.instance.log(f"日志未保存：空日志文件", "INFO")
                    return

                with open(
                        "./logs/" + (name := (Logger.str_start_time + f".{Logger.__suffix}.log")),
                        "w",
                        encoding="UTF-8",
                ) as f:
                    f.write(Logger.instance.log_text)

                Logger.instance.log(f"日志保存至 '{path}\\{name}'", "INFO")

            except IOError as e:
                Logger.instance.log(f'日志保存失败："{e}"', "ERROR")

    @staticmethod
    def register_traceback() -> None:
        if Logger.isLogging_:
            traceback_console = Console(file=sys.stderr, width=100)

            def excepthook(
                    type_: Type[BaseException],
                    value: BaseException,
                    traceback: Optional[TracebackType],
            ) -> None:

                exception = Traceback.from_exception(
                    type_,
                    value,
                    traceback,
                    width=width,
                    extra_lines=extra_lines,
                    theme=theme,
                    word_wrap=word_wrap,
                    show_locals=show_locals,
                    indent_guides=indent_guides,
                    suppress=suppress,
                    max_frames=max_frames,
                )

                path = os.path.abspath("./logs/")
                logger.log(
                    f"出现严重错误，程序崩溃！详情请看 '{path + Logger.str_start_time}.{Logger.__suffix}.log'",
                    CRITICAL,
                )

                exception_no_local = Traceback.from_exception(
                    type_,
                    value,
                    traceback,
                    width=width,
                    extra_lines=extra_lines,
                    theme=theme,
                    word_wrap=word_wrap,
                    show_locals=show_locals,
                    indent_guides=indent_guides,
                    suppress=suppress,
                    max_frames=max_frames,
                )

                traceback_console.print(exception_no_local)
                for exc in exception.__rich_console__(
                        traceback_console, traceback_console.options
                ):
                    if isinstance(exc, rich.traceback.Constrain):
                        panel = exc.renderable

                        for thing in panel.__rich_console__(
                                traceback_console, traceback_console.options
                        ):
                            logger.write(thing.text)

                    elif isinstance(exc, rich.traceback.Text):
                        logger.write(str(exc.copy()) + "\n")

            sys.excepthook = excepthook


py_version: str = platform.version()
py_sys_version: str = sys.version
py_sys_version_info: str = sys.version_info
py_platform: str = sys.platform
default_encoding: str = sys.getdefaultencoding()  # 获取系统当前编码
file_system_encoding: str = sys.getfilesystemencoding()  # 获取文件系统使用编码方式，Windows下返回'mbcs'，mac下返回'utf-8'
running_path: str = os.path.abspath("./")  # logger程序目录环境
pip_list: str = ""
pip_check: str


def log__init__(osc_in: ObjectStateConstant, pip_in: PipManage) -> None:
    global osc_, logger, pip_list, pip_check
    osc_ = osc_in
    logger.isLogging = osc_.isLoggingUsing

    pip_manage: PipManage = pip_in

    if pip_manage.count() <= pip_manage.maxPrintLibCount:
        for i in pip_manage.return_lib():
            pip_list += str(i)
    else:
        pip_list = "Amount is bigger than default, so there's no output."

    if pip_manage.isPipDetect:
        if pip_manage.pip_detect() is True:
            pip_check = "All lib is already done."
        else:
            pip_check = pip_manage.pip_detect()
    else:
        pip_check = "Don't use pip check."


logger = Logger()
logger.register_traceback()

DEBUG: Literal["DEBUG"] = "DEBUG"  # ”罗嗦的“，不会在日志文件中记录的
INFO: Literal["INFO"] = "INFO"  # 非开发者能看的懂的信息
WARNING: Literal["WARNING"] = "WARNING"  # 对程序本身没有影响的异常
ERROR: Literal["ERROR"] = "ERROR"  # 异常，但是会被捕捉
CRITICAL: Literal["CRITICAL"] = "CRITICAL"  # 致命异常，将终止程序

__all__ = [
    "logger",
    "osc_",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "py_version",
    "__version__",
    "log__init__"]

osc_: ObjectStateConstant = ObjectStateConstant()
