# Traceback exception definitions
WIDTH: int = 100
EXTRA_LINES: int = 3
THEME = None
WORD_WRAP: bool = False
SHOW_LOCALS: bool = True
INDENT_GUIDES: bool = True
SUPPRESS = ()
MAX_FRAMES: int = 100

# Headline definitions
# {0}{1}:使用程序名称及版本号，由oc管理
# {2}:logger版本号
HEADLINE_STRUCTURE: str = """ 
{0} {1}
Using TrimLog Library by Apache2.0 License.
Copyright 2022-2023 all the developers of Kaleido and Trim Organization.(FedDragon1, Eilles Wan, bgArray)
Library Version: {2}
"""

# License template
# {0} lib_name; {1} license_name; {2} license_line; {3} lib_version; {4} addition(optional)
LICENSE_STRUCTURE: str = """
Using {0} Library by {1} License.
{2}
Library Version: {3}
{4}
"""

# Weight order
WEIGHT_ORDER = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

# Release template
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
"""


# levels_setting
class _Level:
    DEBUG: tuple[str, int] = "[bright_cyan][DEBUG][/bright_cyan]", 27
    INFO: tuple[str, int] = "[green][INFO][/green]", 15
    WARNING: tuple[str, int] = "[gold3][WARNING][/gold3]", 15
    ERROR: tuple[str, int] = "[dark_orange3][ERROR][/dark_orange3]", 29
    CRITICAL: tuple[str, int] = "[red][CRITICAL][/red]", 11
