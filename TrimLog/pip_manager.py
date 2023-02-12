# -*- coding: utf-8 -*-
"""日志消息处理 Pip管理模块

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

pip管理类开发者：bgArray
"""

import pkg_resources
import os

from typing import Union, Tuple, List, Dict

from .exceptions import *


# Pip method
class PipManage:
    """
    管理Pip的类，一个Project一个即可
    write by bgArray
    """

    __version__ = "v0.2.7"

    def __init__(
        self,
        is_detect_pip: bool = False,
        is_install_pip: bool = False,
        max_printing_lib_count: int = 20,
    ):
        """
        实例化对象
        :param is_detect_pip: logger库 是否启用检测pip安装情况
        :param is_install_pip: logger库 是否自动安装pip
        :param max_printing_lib_count: logger库 最大print多少个Lib的阈值
        """
        self.working_set = pkg_resources.WorkingSet()
        self.lst: list = [d for d in self.working_set]  # 本环境下已有内容

        self.is_detect_pip: bool = is_detect_pip  # 是否自动检测
        self.is_install_pip: bool = is_install_pip  # 是否自动安装

        self.max_printing_lib_count: int = max_printing_lib_count  # 打印阈值

        self.set_lst = []  # 需要目标
        self.detect_report = []  # 报告

    def count(self) -> int:
        """
        返回环境下pip lib count
        :return: pip lib count
        """
        return self.lst.__len__()

    def return_lib(self) -> Tuple[str, str, list]:
        """
        以yield方式返回环境下的 包名和版本 , 所依赖的其他包
        :return:
        """
        for item in self.lst:
            yield str(item.project_name), str(item.version), list(
                item.requires()
            )  # 包名和版本 , 所依赖的其他包

    def pip_detect(self) -> Union[bool, List[Dict[str, str]], List[Dict[str, None]]]:
        """
        先执行detecting_setting()
        :return: 不缺库的时候返回True;缺库时返回一个列表，里面会以{"need": xxx, "have": yyy}形式说明，若版本冲突，则yyy为str；
        若缺少库，则yyy为None
        """
        return_list = []
        for item in self.lst:
            for i in self.set_lst:
                if str(i) == str(item.project_name) + "==" + str(item.version):
                    self.set_lst.remove(i)
                    break
                elif str(item.project_name) in str(i):
                    if str(i).count("==") == 0:
                        if str(i)[: str(i).find("==")] == str(item.project_name):
                            self.set_lst.remove(i)
                            break
                    else:
                        if str(item.project_name) == str(i)[: str(i).find("==")]:
                            return_list.append(
                                {
                                    "need": str(i),
                                    "have": str(item.project_name)
                                    + "=="
                                    + str(item.version),
                                }
                            )
                            self.set_lst.remove(i)
                            break
                elif str(i) in (str(item.project_name) + "==" + str(item.version)):
                    if str(i).count("==") == 0:
                        self.set_lst.remove(i)
                        break
                elif str(i).lower() in (
                    str(item.project_name).lower() + "==" + str(item.version)
                ):
                    self.set_lst.remove(i)
                    break
                elif str(i).upper() in (
                    str(item.project_name).upper() + "==" + str(item.version)
                ):
                    self.set_lst.remove(i)
                    break

        if self.set_lst.__len__() == 0 and return_list.__len__() == 0:  # 无版本不匹配及库缺失
            self.set_lst = []
            self.detect_report = []
            return True
        else:
            for i in self.set_lst:
                if "@ file:" in i:
                    continue
                return_list.append({"need": str(i), "have": None})
            self.detect_report = return_list
            return return_list

    def detecting_setting(
        self,
        requirements_list: List[pkg_resources.Requirement.parse] = None,
        requirements_path: str = None,
    ) -> None:
        """
        设置要检测的对象，注意两个参数填一个且只有一个就好，建议使用path
        :param requirements_list: 传入[Requirement.parse('matplotlib'), Requirement.parse('mido')]这样的列表
        :param requirements_path: 传入requirements.txt的路径即可
        :return: None
        """
        if requirements_list is None and requirements_path is None:
            raise NoSettings
        elif requirements_list is not None and requirements_path is not None:
            raise OverSettings
        elif requirements_list is not None:
            self.set_lst = requirements_list
        elif requirements_path is not None:
            requirements_string: str = self.open_req(requirements_path)
            REs = []
            for i in range(requirements_string.count("\n")):
                if (
                    requirements_string != ""
                    and requirements_string != "\n"
                    and requirements_string != " "
                    and requirements_string[:1] != "\n"
                ):
                    Re = pkg_resources.Requirement.parse(
                        requirements_string[: requirements_string.find("\n")]
                    )
                    REs.append(Re)
                    requirements_string = requirements_string.replace(
                        requirements_string[: requirements_string.find("\n")] + "\n", ""
                    )
                else:
                    requirements_string = requirements_string.replace(
                        "\n", "", 1
                    ).replace(" ", "")
            requirements_string = requirements_string.replace("\n", "").replace(" ", "")
            if requirements_string != "":
                REs.append(pkg_resources.Requirement.parse(requirements_string))
            self.set_lst = REs

    @staticmethod
    def open_req(path: str) -> str:
        """
        打开requirements.txt
        :param path: requirements.txt path
        :return: str: thing
        """
        try:
            f = open(path, mode="r", encoding="utf-16")
            return f.read(-1)
        except UnicodeError as e:
            f.close()
            if str(e) == "UTF-16 stream does not start with BOM":
                f = open(path, mode="r", encoding="utf-8")
                return f.read(-1)
        finally:
            f.close()

    def pip_install(self) -> bool:
        """
        根据self.detect_report安装库
        :return: True/False 表示是否全部安装正确
        """
        if self.is_install_pip:
            if self.detect_report.__len__() == 0:
                return True
            for i in self.detect_report:
                if i["have"] is None:
                    command = "pip install " + str(i["need"])
                    os.system(command)
            if self.pip_detect():
                return True
            else:
                return False
