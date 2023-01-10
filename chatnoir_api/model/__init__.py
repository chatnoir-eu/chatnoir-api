from base64 import urlsafe_b64decode
from enum import Enum
from uuid import UUID

from chatnoir_api.types import Literal


class Index(Enum):
    ClueWeb09 = "cw09"
    ClueWeb12 = "cw12"
    ClueWeb22 = "cw22"
    CommonCrawl1511 = "cc1511"
    CommonCrawl1704 = "cc1704"

    @property
    def prefix(self) -> str:
        if self is Index.ClueWeb09:
            return "clueweb09"
        elif self is Index.ClueWeb12:
            return "clueweb12"
        elif self is Index.ClueWeb22:
            return "clueweb22"
        elif self is Index.CommonCrawl1511:
            return "commoncrawl"
        elif self is Index.CommonCrawl1704:
            return "commoncrawl"
        else:
            raise ValueError(f"Unknown Index enum: {self}")


Slop = Literal[0, 1, 2]


class ShortUUID(UUID):
    def __init__(self, short_uuid: str):
        super().__init__(bytes=urlsafe_b64decode(f"{short_uuid}=="))


def decode_uuid(uuid_or_short_uuid: str) -> UUID:
    if "-" in uuid_or_short_uuid and len(uuid_or_short_uuid) >= 36:
        return UUID(uuid_or_short_uuid)
    else:
        return ShortUUID(uuid_or_short_uuid)
