# TrimLog 使用指南

（2023/4/8 版本）

本仓库使用 Apache2.0 协议开源

## Part1 简介

TriMO 组织的 python 项目 log 和项目管理框架库。

包含 Logger、Pip Manage(PM)和 ObjectConstant(OSC)两部分。

Logger 负责日志主体，OSC 负责控制项目整体变量，例如是否启用日志，是否启用 debug 模式等，也可以管理版本号等基础信息。

PM 负责 pip 简单管理，例如检查 pip，执行 pip install。

在`test.py`中有基础的代码示例，可以参考！

## Part2 Logger 部分

### 2.1 logger 基础

首先感谢**乐观的辣条(FedDragon1)** 手写本项目的 logger 框架，太强了，万分感谢！

logger 使用起来非常简单，第一步，导入。

以下两种导入都可以：

> `import TrimLog`
>
> `from TrimLog import object_constants`
>
> `from TrimLog import log__init__, logger`

**警告: TrimLog 使用的是单例模式，并且包内已经实例化过了，所以请不要再在您程序中
使用`TrimLog.Logger()`实例化主类。**

提示：因为 logger 已经被实例化了，此时所以的 logger 的所有函数都可以使用了。
但是这时所有的参数都是内置的，如果需要自己设置参数请往下看。

### 2.2 logger**init**()方法

如果你希望设置自动 logger 的部分参数，而且管理项目更方便，我更推荐使用`logger__init__()`方法后再使用。

```text
def log__init__(osc_in: ObjectStateConstant, pip_in: PipManage, is_regenerate: bool = False) -> None:
    """
    to initialize logger.
    :param osc_in: need an OSC class.
    :param pip_in: need a PM class.
    :param is_regenerate: if regenerate the log class, set True.
    """
```

`logger__init__()`方法默认需要三个实参：一个 OSC 实例化对象，一个 PM 实例化对象，最后一个是是否重新生成 logger 实例的布尔值。

所以，在使用`logger__init__()`之前，您应该需要先实例化这两个对象，具体实例化请看后文。

这个方法的主要功能是：

1. 利用 OSC 的内置参数配置全局是否启动 log
2. 利用 OSC 的内置参数配置全局是否启动 release 发布模式
3. 利用 PM 直接对 pip 管理
4. 自动 headline
5. 重新启动 logger 示例（单例刷新）

当然，以上操作都可以手动完成，但更推荐这样做（尤其你的程序需要发布时）。

提示：如果你的项目有许多模块，建议你只在运行程序也就是类似于 main.py 中使用 logger**init**()。
其他模块正常 import 即可。

多模块示例：
in `main.py`

```text
from TrimLog import *
from TrimLog.object_constants import ObjectStateConstant
from TrimLog.pip_manager import PipManage
from call_ import *

osc = ObjectStateConstant()
pm = PipManage()

log__init__(osc, pm)
logger.info("a")

osc.isLoggingUsing = False

log__init__(osc, pm)
calling()
```

in `call_.py`

```text
from TrimLog import *

logger.info("start")


def calling():
    print("is calling me")
    logger.info("calling")
    print(logger.is_logging)
```

output:

```text
[15:38:30] [INFO]      start                                 logger_main.py:267
────────────────────────────────── Headline ───────────────────────────────────
           [WARNING]                                         logger_main.py:267
            v0.0.1
           Using TrimLog Library by Apache2.0 License.
           Copyright 2022-2023 all the developers of Kaleido
           and Trim Organization.(FedDragon1, Eilles Wan,
           bgArray)
           Library Version: v0.6.8

───────────────────────── License for Pip manage Lib ──────────────────────────
           [WARNING]                                         logger_main.py:267
           Using Pip manage Lib Library by Apache 2.0
           License.
           Copyright 2022-2023 all the developers of Trim
           Organization.(FedDragon1, Eilles Wan, bgArray)
           Library Version: v0.2.7


           [WARNING]   log__init__ done.                     logger_main.py:267
           [INFO]      a                                     logger_main.py:267
is calling me
False
```

### 2.3 logger 内置属性

这是整体的属性预览，下面有分段讲解。

```text
    def __new__(
            cls,
            is_logging: bool = True,
            is_auto_headline: bool = False,
            is_tips: bool = True,
            printing: bool = True,
            writing: bool = True,
            include_headline: bool = True,
            include_license: bool = True,
            include_release_info: bool = False,
            print_level: L = "DEBUG",
            write_level: L = "INFO",
            headline_level: L = "WARNING",
            license_level: L = "WARNING",
            max_log_count: int = 20,
            show_position: bool = False,
            in_suffix: str = ".dsl",

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
        :param in_suffix: allow to set a suffix of file name. Be like: ".dsl" or "".
        """
```

#### 2.3.1 logger.is_logging

`is_logging: bool = True`

可以用来随时控制 logger 是否启用，默认启用。

影响主要是是否输出和写入。False 状态所有函数调用后无反应(含 return 的正常继续 return)

#### 2.3.2 logger.is_auto_headline

`is_auto_headline: bool = False`

几乎没什么用，保持 False 即可。

用处就是在内置 logger 实例化的时候是否自动输出 headline。
使用`logger.is_auto_headline = True`后依然无效果。

只有修改源码才有效果。

你可能想看的是：`logger.include_headline`

#### 2.3.3 logger.is_tips

`is_tips: bool = True`

是否在出错时使用 tips 功能，详见 tips 章节。

tips 输出规则：

```text
if (Logger.instance.is_logging and osc_.isRelease) or Logger.instance.is_tips:
```

如果 logger.is_tips 为 True 的话就无论如何都会 tips。

#### 2.3.4 logger.printing

`printing: bool = True`

控制是否输出到屏幕上，默认 True。

提示：这里为 False 也可以输出到屏幕上，详见方法说明——强制启用。

#### 2.3.5 logger.writing

`writing: bool = True`

控制是否写入文本，默认 True。

提示：这里为 False 也可以写入文本，详见方法——强制启用。

#### 2.3.6 logger.include_headline

include_headline: bool = True

是否允许使用 headline_shower()，默认 True。

headline 输出规则：

```text
if (self.include_headline is True and self.headline_count < 1) or \
                mandatory_use is True:  # 启动两种条件：允许自动包含打印且次数为0；强制打印
```

详见 `logger.headline_shower()`

#### 2.3.7 logger.include_license

`include_license: bool = True`

是否允许使用 license_shower()，默认 True。

license 输出规则：

```text
 # 启用条件：使用log且启用license输出
if self.include_license and self.is_logging:
```

详见 `logger.license_shower()`

#### 2.3.8 logger.include_release_info

`include_release_info: bool = False`

是否允许使用基本信息：baseinfo_shower()，默认 False。

baseinfo 输出规则：

```text
# 启用条件：使用log且启用release模式
if self.include_release_info and self.is_logging:
```

详见 `logger.baseinfo_shower()`

#### 2.3.9 logger.print_level

`print_level: L = "DEBUG"`

屏幕输出限制等级，如 DEBUG 则为所有都输出，INFO 为 DEBUG 不输出，默认 DEBUG。

不建议使用这个参数来修改等级，详见：`2.4.7 set_print_level`

详见输出等级。

#### 2.3.10 logger.write_level

`write_level: L = "INFO"`

写入限制等级，如 DEBUG 则为所有都输出，INFO 为 DEBUG 不输出，默认 INFO。

不建议使用这个参数来修改等级，详见：`2.4.8 set_write_level`

详见输出等级。

#### 2.3.11 logger.headline_level

`headline_level: L = "WARNING"`

headline 输出和写入等级，默认 WARNING。

详见输出等级。

#### 2.3.12 logger.license_level

`license_level: L = "WARNING"`

headline 输出和写入等级，默认 WARNING。

详见输出等级。

#### 2.3.13 logger.max_log_count

`max_log_count: int = 20`

最多存储多少个文件就开始从最早的文件删去，默认 20.

#### 2.3.14 logger.show_position

`show_position: bool = False`

是否显示调用 logger 的位置，默认 False。

输出效果如下：

```text
[INFO] <test.py-<module>: 62> a                   logger_main.py:265
```

#### 2.3.15 logger.in_suffix

`in_suffix: str = ".dsl"`

保存的日志后缀，默认为.dsl.log 文件。

### 2.4 logger 方法

接下来是方法合集。

#### 2.4.1 logger.log()

```text
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
```

这是最原始的输出函数，调用他意味着既输出到屏幕又输出到文本。

你需要填入：info：你想要输出的信息；level：你想要的等级；
mandatory_use：是否无视 self.is_logging/self.printing/self.print_level 的限制输出。

例子：`logger.log("things", "INFO")`

剩余的参数请不要动。

#### 2.4.2-2.4.6 logger.debug()/info()/warning()/error()/critical()

以 logger.debug()举例子：

```text
    def debug(self, debug: T, mandatory_use: bool = False,) -> T:
        """
        output log that's "debug" level.
        :param debug: things you want to output.
        :param mandatory_use: allow to use this function while "self.is_logging" is False.
        :return:things you want to output.
        """
```

使用这些简化输出函数，同样意味着既输出到屏幕又输出到文本。

你需要填入：info：你想要输出的信息；
mandatory_use：是否无视 self.is_logging/self.printing/self.print_level 的限制输出。

提示：建议使用这几种函数。

#### 2.4.7-2.4.8 logger.set_print_level/set_write_level

以 logger.set_print_level 举例子：

```text
     @set_print_level.setter
     def set_print_level(self, in_level: L) -> None:
            """
            set print level and refresh weight
            :param in_level: print level
            """
```

在你想改变输出等级时，请最好使用这个 property 方法。

你需要填入：in_level：变动后的输出等级。

例子：`logger.set_print_level = "INFO"`

#### 2.4.9 logger.write()

```text
    def write(self, text: str, mandatory_use: bool = False,) -> None:
        """
        write things into self.log_text.
        :param text: things
        :param mandatory_use: allow to use this function while "self.is_logging" is False.
        """
```

如果你就是只想写入，请你使用这个函数。

你需要填入：test：你想要写入的文本；
mandatory_use：是否无视 self.is_logging/self.writing 的限制写入。

#### 2.4.10 logger.headline_shower()

```text
    def headline_shower(self, mandatory_use: bool = False) -> None:
        """
        show this library's headline.
        :param mandatory_use: allow to use this function while "self.is_logging" is False and self.headline_count >= 1.
        control
        """
```

用于输出 headline 的函数。

你需要填入：mandatory_use：是否无视 self.include_headline 和 self.headline_count 输出。

输出条件：

```text
if (self.include_headline is True and self.headline_count < 1) or \
                mandatory_use is True:  # 启动两种条件：允许自动包含打印且次数为0；强制打印
```

默认输出示例：

```text
────────────────────────────────── Headline ───────────────────────────────────
[14:27:31] [WARNING] <logger_main.py-headline_shower: 389>   logger_main.py:266
           Test Project v0.1.2334
           Using TrimLog Library by Apache2.0 License.
           Copyright 2022-2023 all the developers of Kaleido
           and Trim Organization.(FedDragon1, Eilles Wan,
           bgArray)
           Library Version: v0.6.8

───────────────────────── License for Pip manage Lib ──────────────────────────
           [WARNING] <logger_main.py-headline_shower: 404>   logger_main.py:266
           Using Pip manage Lib Library by Apache 2.0
           License.
           Copyright 2022-2023 all the developers of Trim
           Organization.(FedDragon1, Eilles Wan, bgArray)
           Library Version: v0.2.7

```

默认模板：

```text
# {0}{1}:使用程序名称及版本号，由osc管理
# {2}:logger版本号
{0} {1}
Using TrimLog Library by Apache2.0 License.
Copyright 2022-2023 all the developers of Kaleido and Trim Organization.(FedDragon1, Eilles Wan, bgArray)
Library Version: {2}
```

#### 2.4.11 logger.baseinfo_shower()

```text
    def baseinfo_shower(self) -> None:
        """
        show:running platform, Python version, Python cmd version, Python version info, program location,
        default encoding, file system encoding, pip list, pip check.
        """
```

用于输出程序运行环境信息。

无实参。

输出条件：

```text
        # 启用条件：使用log且启用release模式
        if self.include_release_info and self.is_logging:
```

默认输出示例：

```text
────────────────────────────────── BaseInfo ───────────────────────────────────
           [WARNING] <logger_main.py-baseinfo_shower: 420>   logger_main.py:266
           running platform: win32
           Python version: 10.0.19045
           Python cmd version: 3.9.13 (main, Aug 25 2022,
           23:51:50) [MSC v.1916 64 bit (AMD64)]
           Python version info: sys.version_info(major=3,
           minor=9, micro=13, releaselevel='final',
           serial=0)
           program location:
           L:\logger更新\TrimLog\v0.6.5\TrimLog\TrimLog
           default encoding: utf-8
           file system encoding: utf-8
           pip list: Amount is bigger than default, so
           there's no output.
           pip check: Don't use pip check.
```

默认模板：

```text
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
```

#### 2.4.12 logger.license_shower()

```text
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
```

用于打印许可证或者协议信息。

你需要填入：lib_name：引用库的名称；license_name：许可证名称（如 Apache2.0）；
license_line：一行许可证引用复制证明的话（如：Copyright 2022-2023 all the developers of Trim Organization.
(FedDragon1, Eilles Wan, bgArray)）；
lib_version：引用库版本；addition：附加内容；include_startline 是否开始打印一条分割线。

输出条件：

```text
        # 启用条件：使用log且启用license输出
        if self.include_license and self.is_logging:
```

默认输出示例：

```text
────────────────────────────── License for libA ───────────────────────────────
           [WARNING] <logger_main.py-license_shower: 462>    logger_main.py:266
           Using libA Library by GPL3.0 License.
           Copyright 2023 xxx
           Library Version: v0.0.1
           This lib is xxx.
```

默认模板：

```text
# {0} lib_name; {1} license_name; {2} license_line; {3} lib_version; {4} addition(optional)
LICENSE_STRUCTURE: str = """
Using {0} Library by {1} License.
{2}
Library Version: {3}
{4}
"""
```

#### 2.4.13 logger.default_value_return()

```text
    @staticmethod
    def default_value_return() -> list:
        """
        to return our library default values.
        :return: a list.
        """
```

返回默认参数，无实参。

模板：

```text
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
```

#### 2.4.14-2.4.16 logger.save()/tips()/register_traceback()

不建议使用，主要为内部方法，暂时不设教程。

## Part3 Pip Manage 部分

```text
# Pip method
class PipManage:
    """
    管理Pip的类，一个Project一个即可
    write by bgArray
    """

    __version__ = "v0.2.7"
```

因为这个部分比较简单，我就按照教程写了，不按上面的文档格式。

#### 3.1 pm 初始化

```text
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
```

如上面，正常实例化即可。

#### 3.2 pm.count()

返回当前环境下有多少个 pip 包

#### 3.3 pm.return_lib()

```text
    def return_lib(self) -> tuple[str, str, list]:
        """
        以yield方式返回环境下的 包名和版本 , 所依赖的其他包
        :return:
        """
```

#### 3.4 pm.detecting_setting()

```text
    def detecting_setting(
        self,
        requirements_list: list[pkg_resources.Requirement.parse] = None,
        requirements_path: str = None,
    ) -> None:
        """
        设置要检测的对象，注意两个参数填一个且只有一个就好，建议使用path
        :param requirements_list: 传入[Requirement.parse('matplotlib'), Requirement.parse('mido')]这样的列表
        :param requirements_path: 传入requirements.txt的路径即可
        :return: None
```

在 pip 安装及检测前必须做的设置，建议用路径 requirements.txt 输入。

#### 3.5 pm.pip_detect()

在执行完上面的函数后可执行这个：

```text
    def pip_detect(self) -> Union[bool, list[dict[str, str]], list[dict[str, None]]]:
        """
        先执行detecting_setting()
        :return: 不缺库的时候返回True;缺库时返回一个列表，里面会以{"need": xxx, "have": yyy}形式说明，若版本冲突，则yyy为str；
        若缺少库，则yyy为None
        """
```

#### 3.6 pm.pip_install()

执行完上面两个函数方可执行这个：

```text
    def pip_install(self) -> bool:
        """
        根据self.detect_report安装库
        :return: True/False 表示是否全部安装正确
        """
```

#### 3.7 PM 搭配 logger 使用示例

```python
import TrimLog
from TrimLog import object_constants
from TrimLog import log__init__, logger

osc = object_constants.ObjectStateConstant()

pm = TrimLog.PipManage(True, True, 40)
pm.detecting_setting(requirements_path="requirements.txt")
osc.dp("dp" + str(pm.pip_detect()))

osc.set_console(logger.console)
osc.dp("dp: 666")

logger.show_position = True
logger.include_release_info = True  # Release 模式
# logger.include_headline = False
log__init__(osc, pm)
```

## Part4 ObjectStateConstant 部分

这个没啥可说的，就是项目常量记录：

```python
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

```

唯一值得一提的是，这里面的 dp 函数可用使用 rich 模块的 print。
可以使用 set_console 来启用这个功能。

下面就是示例代码：

```python
import TrimLog
from TrimLog import object_constants
from TrimLog import log__init__, logger

osc = object_constants.ObjectStateConstant()
osc.isLoggingUsing = False
osc.project_name = "Test Project"
osc.version = "v0.1.2334"

pm = TrimLog.PipManage(True, True, 40)
# pm.detecting_setting(requirements_path="requirements.txt")
osc.dp("dp" + str(pm.pip_detect()))

osc.set_console(logger.console)
osc.dp("dp: 666")

logger.show_position = True
logger.include_release_info = True  # Release 模式
# logger.include_headline = False
log__init__(osc, pm)
```

## Part5 tips 功能补充说明

最后补充一个 logger 功能，没有放在 logger 章节里。

```text
logger.tips_list = [{"position": "test.py:80 in <module>",
                     "error_text": "ZeroDivisionError: division by zero",
                     "tips": "除数为0了，你可以：1.  xxxx; 2.xxxx"}]
```

你可以在你的代码中无限扩展这个 list，但每个项目中的 key 都应该保持和这个一样。

position 是相对路径，必须保持这个格式。

error_test 是报错最后一行内容。

tips 就是当你的程序出现这个错误后，你会给你的用户一个什么样的提示。

使用示例：

```text
logger.tips_list = [{"position": "test.py:91 in <module>",
                     "error_text": "ZeroDivisionError: division by zero",
                     "tips": "除数为0了，你可以：1.  xxxx; 2.xxxx"}]

print(5 / 0)  # 这是test.py的第91行
```

输出示例：

```text
           [CRITICAL]  出现严重错误，程序崩溃！详情请看      logger_main.py:268
           'L:\logger更新\TrimLog\v0.6.5\TrimLog\TrimLog\log
           2023-04-08 22_45_39.abc.log'
┌─────────────────────────────── Traceback (most recent call last) ────────────────────────────────┐
│ L:\logger更新\TrimLog\v0.6.5\TrimLog\TrimLog\test.py:91 in <module>                              │
│                                                                                                  │
│   88 │   │   │   │   │    "error_text": "ZeroDivisionError: division by zero",                   │
│   89 │   │   │   │   │    "tips": "除数为0了，你可以：1.  xxxx; 2.xxxx"}]                        │
│   90                                                                                             │
│ > 91 print(5 / 0)  # 91行抛错                                                                    │
│   92                                                                                             │
│                                                                                                  │
│ ┌─────────────────────────────────────────── locals ───────────────────────────────────────────┐ │
│ │      log__init__ = <function log__init__ at 0x000001F7C2235430>                              │ │
│ │           logger = <TrimLog.logger_main.Logger object at 0x000001F7C3DC0100>                 │ │
│ │ object_constants = <module 'TrimLog.object_constants' from                                   │ │
│ │                    'L:\\logger更新\\TrimLog\\v0.6.5\\TrimLog\\TrimLog\\object_constants.py'> │ │
│ │              osc = <TrimLog.object_constants.ObjectStateConstant object at                   │ │
│ │                    0x000001F7C1691FA0>                                                       │ │
│ │               pm = <TrimLog.pip_manager.PipManage object at 0x000001F7C1691F70>              │ │
│ │          TrimLog = <module 'TrimLog' from                                                    │ │
│ │                    'L:\\logger更新\\TrimLog\\v0.6.5\\TrimLog\\TrimLog\\__init__.py'>         │ │
│ └──────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
ZeroDivisionError: division by zero
除数为0了，你可以：1.  xxxx; 2.xxxx
           [INFO]      移除最早的日志：'logs/2023-02-01      logger_main.py:268
           12_54_15.abc.log'
           [INFO]      日志保存至                            logger_main.py:268
           'L:\logger更新\TrimLog\v0.6.5\TrimLog\TrimLog\log
           \2023-04-08 22_45_39.abc.log'
```

## Part6 后记

预祝各位 TrimLog 使用愉快。

不要忘了 star！
