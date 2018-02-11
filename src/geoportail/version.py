# {# pkglts, version
#  -*- coding: utf-8 -*-

MAJOR = 0
"""(int) Version major component."""

MINOR = 2
"""(int) Version minor component."""

POST = 0
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (MAJOR, MINOR, POST)])
# #}
