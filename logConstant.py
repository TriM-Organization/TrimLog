# Traceback exception definitions
width: int = 100
extra_lines: int = 3
theme = None
word_wrap: bool = False
show_locals: bool = True
indent_guides: bool = True
suppress = ()
max_frames: int = 100


# Headline definitions
# {}:版本号
HEADLINE_INSTRUCTION: str = """ 
——==
Using TrimLog Library by Apache2.0 License.
Copyright 2022-2023 all the developers of Kaleido and Trim Organization.(FedDragon1, Eilles Wan, bgArray)
Library Version: {}
——==
"""


# License template
# {0} lib_name; {1} license_name; {2} license_line; {3} lib_version; {4} addition(optional)
LICENSE_INSTRUCTION: str = """
Using {0} Library by {1} License.
{2}
Library Version: {3}
{4}
——==
"""


# Weight order
WEIGHT_ORDER = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
