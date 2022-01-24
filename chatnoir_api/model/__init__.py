from enum import Enum

from chatnoir_api.types import Literal


class Index(Enum):
    ClueWeb09 = "cw09"
    ClueWeb12 = "cw12"
    CommonCrawl1511 = "cc1511"
    CommonCrawl1704 = "cc1704"

    @property
    def prefix(self) -> str:
        if self is Index.ClueWeb09:
            return "clueweb09"
        elif self is Index.ClueWeb12:
            return "clueweb12"
        elif self is Index.CommonCrawl1511:
            return "commoncrawl"
        elif self is Index.CommonCrawl1704:
            return "commoncrawl"
        else:
            raise ValueError(f"Unknown Index enum: {self}")


Slop = Literal[0, 1, 2]
