from .base import *  # noqa: F403
from .base import env

DEBUG = env("DEBUG")

try:
    from .local import *  # noqa: F403
except ImportError:
    pass
