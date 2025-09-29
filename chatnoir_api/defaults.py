from typing import Set
from chatnoir_api.model import Index, Slop, SearchMethod

DEFAULT_START: int = 0
DEFAULT_SIZE: int = 10
DEFAULT_SLOP: Slop = 0
DEFAULT_INDEX: Set[Index] = {
    "clueweb22/b",
}
DEFAULT_MINIMAL: bool = False
DEFAULT_EXPLAIN: bool = False
DEFAULT_EXTENDED_META: bool = False
DEFAULT_RETRIES: int = 5
DEFAULT_BACKOFF_SECONDS: int = 1
DEFAULT_TIMEOUT: int = 60
DEFAULT_SEARCH_METHOD: SearchMethod = "default"
