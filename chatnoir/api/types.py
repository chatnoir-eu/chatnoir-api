try:
    from functools import cached_property  # noqa: F401
except ImportError:
    cached_property = property  # noqa: F401

try:
    from typing import Literal  # noqa: F401
except ImportError:
    from typing_extensions import Literal  # noqa: F401
