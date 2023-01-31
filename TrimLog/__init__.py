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

import atexit
import platform
import sys
import time
from types import TracebackType
from typing import Literal, Optional, Type, TypeVar

import rich.traceback
from rich.console import Console
from rich.traceback import Traceback

from .logger_constants import *
from .object_constants import *

__version__: str = "v0.6.4"
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
    is_logging = True

    is_tips = False
    tips_dict: list = []

    max_log_count: int = 20

    def __new__(
            cls,
            is_logging: bool = True,
            printing: bool = True,
            writing: bool = True,
            print_level: L = "DEBUG",
            write_level: L = "INFO",
            include_headline: bool = True,
            include_license: bool = True,
            headline_level: L = "WARNING",
            license_level: L = "WARNING",
            max_log_count: int = 20,
            include_release_info: bool = False,
            show_position: bool = True,
            is_auto_headline: bool = False,
            is_tips: bool = True,
    ) -> Logger:
        """
        __new__() method. Don't change it unless you need.
        :param is_logging: use logger or not. Notice that this is the main switch of Logger class.
        :param printing: print on the screen or not.
        :param writing: write into file or not.
        :param print_level: a level that's used to limit the print.
        :param write_level: a level that's used to limit the output files.
        :param include_headline: allow to use the function headline_shower() or not.
        :param include_license: allow to use the function license_shower() or not.
        :param headline_level: choose which level to output the headline.
        :param license_level: choose which level to output the license.
        :param max_log_count: a number that's used to set the maximum number of log files.
        :param include_release_info: allow to use the function baseinfo_shower() or not.
        :param show_position: allow to show the running codes position or not.
        :param is_auto_headline: allow to print headline when the logger is initializing or not.
        The best choice is false.
        :param is_tips: allow to show some tips when the program have errors or not.
        """
        if cls.instance is not None:
            return cls.instance
        cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
            self,
            is_logging: bool = True,
            printing: bool = True,
            writing: bool = True,
            print_level: L = "DEBUG",
            write_level: L = "INFO",
            include_headline: bool = True,
            include_license: bool = True,
            headline_level: L = "WARNING",
            license_level: L = "WARNING",
            max_log_count: int = 20,
            include_release_info: bool = False,
            show_position: bool = False,
            is_auto_headline: bool = False,
            is_tips: bool = True,
    ) -> None:
        """
        __init__() method. Don't change it unless you need.
        :param is_logging: use logger or not. Notice that this is the main switch of Logger class.
        :param printing: print on the screen or not.
        :param writing: write into file or not.
        :param print_level: a level that's used to limit the print.
        :param write_level: a level that's used to limit the output files.
        :param include_headline: allow to use the function headline_shower() or not.
        :param include_license: allow to use the function license_shower() or not.
        :param headline_level: choose which level to output the headline.
        :param license_level: choose which level to output the license.
        :param max_log_count: a number that's used to set the maximum number of log files.
        :param include_release_info: allow to use the function baseinfo_shower() or not.
        :param show_position: allow to show the running codes position or not.
        :param is_auto_headline: allow to print headline when the logger is initializing or not.
        The best choice is false.
        :param is_tips: allow to show some tips when the program have errors or not.
        """
        # 写入文件的内容
        self.log_text: str = ""

        # 总开关，根据OSC
        self.is_logging = is_logging
        Logger.is_logging = is_logging

        # 报错是否给出提示帮助
        self.is_tips = is_tips
        Logger.is_tips = is_tips
        self.tips_dict = []

        # 是否需要输出一些开发时不需要输出的内容；但是用户使用时需要输出的内容
        # 也就是Release版本到不同平台不同版本Python下需要增加的一些信息
        self.include_release_info: bool = include_release_info

        # 是否需要console.log(end="....")
        self.show_position: bool = show_position

        # 头声明；协议声明
        self.include_headline: bool = include_headline
        self.include_license: bool = include_license
        self.headline_level: L = headline_level
        self.license_level: L = license_level

        # 打印到屏幕设置；写入到文件设置
        self.printing: bool = printing
        self.writing: bool = writing
        self.print_level: L = print_level
        self.write_level: L = write_level
        self.print_default_weight = WEIGHT_ORDER.get(self.print_level)
        self.write_default_weight = WEIGHT_ORDER.get(self.write_level)

        # 文件最多保存多少个后开始删除
        self.max_log_count: int = max_log_count
        Logger.max_log_count = self.max_log_count

        # headline理论上只展示一次
        self.headline_count = 0

        # 初始化展示headline
        if is_auto_headline:
            self.headline_shower()

    def log(
            self,
            info: T,
            level: L,
            mandatory_use: bool = False,
            frame_file: str = None,
            frame_name: str = None,
            frame_lineno: int = None,
    ) -> T:
        """
        log output base function.
        :param info: things you want to output.
        :param level: the log output level.
            :param mandatory_use: allow to use this function while "self.is_logging" is False.
        :param frame_file: initiation program's file name.
        :param frame_name: initiation program's function name.
        :param frame_lineno: initiation program's line number.
        :return: things you input.
        """
        if self.is_logging or mandatory_use:
            style: Optional[str]
            style_len: Optional[int]
            style, style_len = getattr(_Level, level, (None, None))
            if style is None or style_len is None:
                raise TypeError(
                    f"等级应为 'DEBUG', 'INFO', 'WARNING', 'ERROR', 或 'CRITICAL' 中的一种，而非 '{level}'"
                )

            level_weight = WEIGHT_ORDER.get(level)

            if frame_lineno is None and frame_name is None and frame_file is None:
                back_frame = sys._getframe().f_back
                frame_file: str = os.path.basename(back_frame.f_code.co_filename)
                frame_name: str = back_frame.f_code.co_name
                frame_lineno: int = back_frame.f_lineno

            if self.show_position:
                end_with = "{0}-{1}: {2}\n".format(
                    frame_file, frame_name, str(frame_lineno)
                )

            if self.writing:
                if level_weight >= self.write_default_weight:
                    if self.show_position:
                        e_w = end_with.replace("\n", "")
                        self.log_text += (
                            f"{time.strftime('[%H:%M:%S]')} [{level}] [{e_w}] {info}\n"
                        )
                    else:
                        self.log_text += (
                            f"{time.strftime('[%H:%M:%S]')} [{level}] {info}\n"
                        )

            length = 12 + style_len

            if self.printing:
                if level_weight >= self.print_default_weight:
                    if self.show_position:
                        e_w = " <" + end_with.replace("\n", "") + "> "
                        add = style + e_w
                        self.console.log(f"{add:<{length}}{info!s:<10}")
                    else:
                        self.console.log(f"{style:<{length}}{info!s:<10}")

        return info

    def set_default_weight(self) -> None:
        """
        refresh weight datas.
        """
        # TODO: 把这里改为@name
        self.print_default_weight = WEIGHT_ORDER.get(self.print_level)
        self.write_default_weight = WEIGHT_ORDER.get(self.write_level)

    @staticmethod
    def get_detail_info() -> tuple[str, str, int]:
        """
        get initiation program datas.
        :return: initiation program's file name, initiation program's function name, initiation program's line number.
        """
        back_frame = sys._getframe().f_back.f_back  # 上一帧=debug/info/..., 上上帧=目标函数
        back_file_name: str = os.path.basename(back_frame.f_code.co_filename)
        back_func_name: str = back_frame.f_code.co_name
        back_line_number: int = back_frame.f_lineno
        return back_file_name, back_func_name, back_line_number

    def debug(self, debug: T) -> T:
        """
        output log that's "debug" level.
        :param debug: things you want to output.
        :return:things you want to output.
        """
        return self.log(debug, "DEBUG", *self.get_detail_info())

    def info(self, info: T) -> T:
        """
        output log that's "info" level.
        :param info: things you want to output.
        :return: things you want to output.
        """
        return self.log(info, "INFO", *self.get_detail_info())

    def warning(self, warning: T) -> T:
        """
        output log that's "warning" level.
        :param warning: things you want to output.
        :return: things you want to output.
        """
        return self.log(warning, "WARNING", *self.get_detail_info())

    def error(self, error: T) -> T:
        """
        output log that's "error" level.
        :param error: things you want to output.
        :return: things you want to output.
        """
        return self.log(error, "ERROR", *self.get_detail_info())

    def critical(self, critical: T) -> T:
        """
        output log that's "critical" level.
        :param critical: things you want to output.
        :return: things you want to output.
        """
        return self.log(critical, "CRITICAL", *self.get_detail_info())

    def write(self, text: str) -> None:
        """
        write things into self.log_text.
        :param text: things
        """
        if self.is_logging:
            self.log_text += text

    def headline_shower(self, mandatory_use: bool = False) -> None:
        """
        show this library's headline.
        :param mandatory_use: mandatory use, which means not subject to self.include_headline and self.headline_count
        control
        """
        global __version__, pip_manage_, osc_
        if (
                self.include_headline is True and self.headline_count < 1
        ) or mandatory_use is True:
            self.console.rule("[bold red]Headline")
            self.log(
                HEADLINE_STRUCTURE.format(osc_.project_name, osc_.version, __version__),
                self.headline_level,
                mandatory_use=True,
            )

            license_thing = LICENSE_STRUCTURE.format(
                "Pip manage Lib",
                "Apache 2.0",
                "Copyright 2022-2023 all the developers of Trim Organization.(FedDragon1, Eilles Wan, bgArray)",
                str(pip_manage_.__version__),
                "",
            )
            self.console.rule("[bold red]License for " + "Pip manage Lib")
            self.log(license_thing, self.license_level, mandatory_use=True)

            self.headline_count += 1

    def baseinfo_shower(self) -> None:
        """
        show:running platform, Python version, Python cmd version, Python version info, program location,
        default encoding, file system encoding, pip list, pip check.
        """
        global py_version, py_sys_version, py_sys_version_info, pip_list, pip_check, \
            default_encoding, running_path, file_system_encoding, py_platform
        if self.include_release_info and self.is_logging:
            self.console.rule("[bold red]BaseInfo")
            self.log(
                RELEASE_STRUCTURE.format(
                    py_platform,
                    py_version,
                    py_sys_version,
                    py_sys_version_info,
                    running_path,
                    default_encoding,
                    file_system_encoding,
                    pip_list,
                    pip_check,
                ),
                self.headline_level,
            )

    def license_shower(
            self,
            lib_name: str,
            license_name: str,
            license_line: str,
            lib_version: str,
            addition: str = "",
            include_startline: bool = True,
    ) -> None:
        """
        show a specified license
        :param lib_name: what's your importing lib's name?
        :param license_name: what's your importing lib's license?
        :param license_line: copy your importing lib's license show information. Be like:
        Copyright 2022-2023 all the developers of Trim Organization.(FedDragon1, Eilles Wan, bgArray)
        :param lib_version: what's your importing lib's version?
        :param addition: if there's something you want to add, fill in this blank. (if not, please keep "")
        :param include_startline: to show a line before the main text or not.
        """
        if self.include_license and self.is_logging:
            license_thing = LICENSE_STRUCTURE.format(
                lib_name, license_name, license_line, lib_version, addition
            )
            if include_startline:
                self.console.rule("[bold red]License for " + lib_name)
            self.log(license_thing, self.license_level)

    def tips_set(self, in_dict: list) -> None:
        """
        set tips dict.
        :param in_dict: input your tips formatting dict.
        """
        # TODO: 把这里改为@name
        self.tips_dict = in_dict
        Logger.tips_dict = self.tips_dict

    @staticmethod
    def default_value_return() -> list:
        """
        to return our library default values.
        :return: a list.
        """
        return_list = [
            {
                "WIDTH": WIDTH,
                "EXTRA_LINES": EXTRA_LINES,
                "THEME": THEME,
                "WORD_WRAP": WORD_WRAP,
                "SHOW_LOCALS": SHOW_LOCALS,
                "INDENT_GUIDES": INDENT_GUIDES,
                "SUPPRESS": SUPPRESS,
                "MAX_FRAMES": MAX_FRAMES,
            },
            {
                "HEADLINE_STRUCTURE": HEADLINE_STRUCTURE,
                "LICENSE_STRUCTURE": LICENSE_STRUCTURE,
                "RELEASE_STRUCTURE": RELEASE_STRUCTURE,
            },
            {"WEIGHT_ORDER": WEIGHT_ORDER},
            {"NoSettings": NoSettings, "OverSettings": OverSettings},
            {"PipManage": PipManage, "PipManage.__version__": PipManage.__version__},
        ]
        return return_list

    @staticmethod
    @atexit.register
    def save() -> None:
        """
        to save log's function.
        """
        if Logger.is_logging:
            try:
                list_of_files = os.listdir("logs")
            except FileNotFoundError:
                os.makedirs("logs")
            else:
                full_path = ["logs/{0}".format(x) for x in list_of_files]

                if len(list_of_files) >= Logger.max_log_count:
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
                        "./logs/"
                        + (name := (Logger.str_start_time + f".{Logger.__suffix}.log")),
                        "w",
                        encoding="UTF-8",
                ) as f:
                    f.write(Logger.instance.log_text)

                Logger.instance.log(f"日志保存至 '{path}\\{name}'", "INFO")

            except IOError as e:
                Logger.instance.log(f'日志保存失败："{e}"', "ERROR")

    @staticmethod
    @atexit.register
    def tips() -> None:
        """
        add tips' function.
        """
        global osc_
        if (Logger.is_logging and osc_.isRelease) or Logger.is_tips:
            log_t = Logger.instance.log_text
            tips_d = Logger.tips_dict
            del_t = (
                    "┌" + "─" * 31 + " Traceback (most recent call last) " + "─" * 32 + "┐"
            )
            end_t = "└" + "─" * 98 + "┘"

            clean_t = (
                log_t[log_t.find(del_t) + 100:].replace("│ │", "").replace("│", "")
            )

            end_error_text = log_t[log_t.find(end_t) + 100:].replace("\n", "")
            error_position = (
                clean_t[: clean_t.find("\n", 2)].replace("\n", "")[1:].replace("  ", "")
            )
            error_position = error_position[error_position.rfind("\\") + 1:]

            if tips_d is not []:
                for i in tips_d:
                    # noinspection PyBroadException
                    try:
                        if (
                                error_position == i["position"]
                                and end_error_text == i["error_text"]
                        ):
                            print(i["tips"])
                            Logger.instance.log_text += i["tips"] + "\n"
                    except BaseException:
                        pass

    @staticmethod
    def register_traceback() -> None:
        """
        register traceback function.
        """
        if Logger.is_logging:
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
                    width=WIDTH,
                    extra_lines=EXTRA_LINES,
                    theme=THEME,
                    word_wrap=WORD_WRAP,
                    show_locals=SHOW_LOCALS,
                    indent_guides=INDENT_GUIDES,
                    suppress=SUPPRESS,
                    max_frames=MAX_FRAMES,
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
                    width=WIDTH,
                    extra_lines=EXTRA_LINES,
                    theme=THEME,
                    word_wrap=WORD_WRAP,
                    show_locals=SHOW_LOCALS,
                    indent_guides=INDENT_GUIDES,
                    suppress=SUPPRESS,
                    max_frames=MAX_FRAMES,
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
file_system_encoding: str = (
    sys.getfilesystemencoding()
)  # 获取文件系统使用编码方式，Windows下返回'mbcs'，mac下返回'utf-8'
running_path: str = os.path.abspath("./")  # logger程序目录环境
pip_list: str = ""
pip_check: str


def log__init__(osc_in: ObjectStateConstant, pip_in: PipManage) -> None:
    """
    to initialize logger.
    :param osc_in: need a OSC class.
    :param pip_in: need a PM class.
    """
    global osc_, logger, pip_list, pip_check
    osc_ = osc_in
    logger.is_logging = osc_.isLoggingUsing
    if osc_.isRelease:
        logger.include_release_info = True
        logger.headline_shower(mandatory_use=True)
    else:
        logger.include_release_info = False
        logger.headline_shower()

    pip_manage: PipManage = pip_in

    if pip_manage.count() <= pip_manage.max_printing_lib_count:
        for i in pip_manage.return_lib():
            pip_list += str(i)
    else:
        pip_list = "Amount is bigger than default, so there's no output."

    if pip_manage.is_detect_pip:
        if pip_manage.pip_detect() is True:
            pip_check = "All lib is already done."
        else:
            pip_check = pip_manage.pip_detect()
    else:
        pip_check = "Don't use pip check."

    if pip_manage.is_install_pip:
        if pip_manage.pip_install() is True and pip_manage.pip_detect() is not True:
            logger.info(
                "Pip manage Class has already downloaded the requirements’ packages and libraries."
            )


osc_: ObjectStateConstant = ObjectStateConstant()
pip_manage_: PipManage = PipManage()

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
    "pip_manage_",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "py_version",
    "__version__",
    "log__init__",
]
