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

py_version: str = platform.version()
__version__: str = "v0.3.5"
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

    def __new__(cls) -> Logger:
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
            line_length: int = None,

    ) -> None:
        self.log_text: str = ""

        # 总开关，根据OSC
        self.isLogging = isLogging
        Logger.isLogging_ = isLogging

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

        # 设置一行长度，默认为15
        self.line_length_set = line_length

        # 初始化展示headline
        self.headline_shower()

    def log(self,
            info: T,
            level: L) -> T:
        if self.isLogging:
            style: Optional[str]
            style_len: Optional[int]
            style, style_len = getattr(_Level, level, (None, None))
            if style is None or style_len is None:
                raise TypeError(
                    f"等级应为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 或 'CRITICAL' 中的一种，而非 '{level}'"
                )

            level_weight = WEIGHT_ORDER.get(level)

            if self.isWrite:
                if level_weight >= self.write_default_weight:
                    self.log_text += f"{time.strftime('[%H:%M:%S]')} [{level}] {info}\n"

            length = 12 + style_len
            if self.line_length_set is not None:
                length = self.line_length_set

            if self.isPrint:
                if level_weight >= self.print_default_weight:
                    self.console.log(f"{style:<{length}}{info!s:<10}")

        return info

    def get_length(self, level: Literal["DEBUG",
                                        "INFO",
                                        "WARNING",
                                        "ERROR",
                                        "CRITICAL"]) -> int:
        length: int
        if self.line_length_set is not None:
            length = self.line_length_set
        else:
            style: Optional[str]
            style_len: Optional[int]
            style, style_len = getattr(_Level, level, (None, None))
            if style is None or style_len is None:
                raise TypeError(
                    f"等级应为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 或 'CRITICAL' 中的一种，而非 '{level}'"
                )
            length = 12 + style_len
        return length

    def set_default_weight(self):
        self.print_default_weight = WEIGHT_ORDER.get(self.printLevel)
        self.write_default_weight = WEIGHT_ORDER.get(self.writeLevel)

    def debug(self, debug: T) -> T:
        return self.log(debug, "DEBUG")

    def info(self, info: T) -> T:
        return self.log(info, "INFO")

    def warning(self, warning: T) -> T:
        return self.log(warning, "WARNING")

    def error(self, error: T) -> T:
        return self.log(error, "ERROR")

    def critical(self, critical: T) -> T:
        return self.log(critical, "CRITICAL")

    def write(self, text: str) -> None:
        if self.isLogging:
            self.log_text += text

    def headline_shower(self):
        global __version__
        if self.isHeadline:
            self.log(HEADLINE_INSTRUCTION.format(__version__)
                     .replace("——==", "——" * (self.get_length(self.headlineLevel) - 1)), self.headlineLevel)

    def license_shower(self, lib_name: str,
                       license_name: str,
                       license_line: str,
                       lib_version: str,
                       addition: str = "",
                       isStartLine: bool = False):
        if self.isLicenseLine:
            license_thing = LICENSE_INSTRUCTION.format(lib_name, license_name, license_line, lib_version, addition)
            license_thing = license_thing.replace("——==", "——" * (self.get_length(self.licenseLevel) - 1))
            if isStartLine:
                license_thing = "——" * (self.get_length(self.licenseLevel) - 1) + license_thing  # 统一长度
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

                if len(list_of_files) >= 10:
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


def log__init__(osc_in: ObjectStateConstant) -> None:
    global osc_, logger
    osc_ = osc_in
    logger.isLogging = osc_.isLoggingUsing


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
