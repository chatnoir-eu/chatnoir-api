from base64 import urlsafe_b64decode
from typing import Literal
from typing_extensions import TypeAlias # type: ignore
from uuid import UUID


Index: TypeAlias = Literal[
    "clueweb09",
    "clueweb12",
    "clueweb22/b",
    "msmarco-document",
    "msmarco-passage",
    "msmarco-document-v2",
    "msmarco-passage-v2",
    "msmarco-document-v2.1",
    "msmarco-passage-v2.1",
    "trec-tot/2024",
    "longeval-sci/2024-11",
    "wows-owi/2025",
]


def parse_index(index_id: str) -> Index:
    if index_id == "cw09":
        return "clueweb09"
    elif index_id == "cw12":
        return "clueweb12"
    elif index_id == "cw22":
        return "clueweb22/b"
    elif index_id == "msmarco-document":
        return "msmarco-document"
    elif index_id == "msmarco-passage":
        return "msmarco-passage"
    elif index_id == "msmarco-document-v2":
        return "msmarco-document-v2"
    elif index_id == "msmarco-passage-v2":
        return "msmarco-passage-v2"
    elif index_id == "msmarco-v2.1":
        return "msmarco-document-v2.1"
    elif index_id == "msmarco-v2.1-segmented":
        return "msmarco-passage-v2.1"
    elif index_id == "trec-tot-2024":
        return "trec-tot/2024"
    elif index_id == "longeval-sci-2024-11":
        return "longeval-sci/2024-11"
    elif index_id == "wows-owi-2025":
        return "wows-owi/2025"
    else:
        raise ValueError(f"Unknown index ID: {index_id}")


def index_id(index: Index) -> str:
    if index == "clueweb09":
        return "cw09"
    elif index == "clueweb12":
        return "cw12"
    elif index == "clueweb22/b":
        return "cw22"
    elif index == "msmarco-document":
        return "msmarco-document"
    elif index == "msmarco-passage":
        return "msmarco-passage"
    elif index == "msmarco-document-v2":
        return "msmarco-document-v2"
    elif index == "msmarco-passage-v2":
        return "msmarco-passage-v2"
    elif index == "msmarco-document-v2.1":
        return "msmarco-v2.1"
    elif index == "msmarco-passage-v2.1":
        return "msmarco-v2.1-segmented"
    elif index == "trec-tot/2024":
        return "trec-tot-2024"
    elif index == "longeval-sci/2024-11":
        return "longeval-sci-2024-11"
    elif index == "wows-owi/2025":
        return "wows-owi-2025"
    else:
        raise ValueError(f"Unknown index: {index}")


def index_prefix(index: Index) -> str:
    if index == "clueweb09":
        return "clueweb09"
    elif index == "clueweb12":
        return "clueweb12"
    elif index == "clueweb22/b":
        return "clueweb22"
    elif index == "msmarco-document-v2.1":
        return "msmarco-v2.1-document"
    elif index == "msmarco-passage-v2.1":
        return "msmarco-v2.1-document-segmented"
    elif index == "msmarco-document-v2":
        return "msmarco-v2-document"
    elif index == "msmarco-passage-v2":
        return "msmarco-v2-passage"
    elif index == "msmarco-document":
        return "msmarco-v1-document"
    elif index == "msmarco-passage":
        return "msmarco-1-passage"
    elif index == "trec-tot/2024":
        return "trec-tot-2024-document"
    elif index == "longeval-sci/2024-11":
        return "longeval-sci-2024-11"
    elif index == "wows-owi/2025":
        return "wows-owi-2025"
    else:
        raise ValueError(f"Unknown index: {index}")


Slop = Literal[0, 1, 2]


class ShortUUID(UUID):
    def __init__(self, short_uuid: str):
        super().__init__(bytes=urlsafe_b64decode(f"{short_uuid}=="))


def decode_uuid(uuid_or_short_uuid: str) -> UUID:
    if "-" in uuid_or_short_uuid and len(uuid_or_short_uuid) >= 36:
        return UUID(uuid_or_short_uuid)
    else:
        return ShortUUID(uuid_or_short_uuid)


SearchMethod = Literal["default", "bm25"]
