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
DEFAULT_RETRIES: int = 5
DEFAULT_BACKOFF_SECONDS: int = 1
DEFAULT_TIMEOUT: int = 60
# Note: This public API key has a small request budget. If you want to use ChatNoir more extensively, please request an API key at https://www.chatnoir.eu/apikey/
DEFAULT_API_KEY = "LTmnNLQeQvBlNjwWeuNxz1vdya3HpSzN"
DEFAULT_SEARCH_METHOD: SearchMethod = "default"
