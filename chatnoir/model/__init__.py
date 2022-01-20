from enum import Enum

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Index(Enum):
    ClueWeb09 = "cw09"
    ClueWeb12 = "cw12"
    CommonCrawl1511 = "cc1511"


Slop = Literal[0, 1, 2]
