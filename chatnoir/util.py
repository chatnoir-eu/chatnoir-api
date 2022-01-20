try:
    from functools import cached_property
except ImportError:
    cached_property = property

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
