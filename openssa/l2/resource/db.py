"""
==============================================
[future work] Database Informational Resources
==============================================
"""


from __future__ import annotations

from .abstract import AbstractResource
from ._global import global_register


@global_register
class DbResource(AbstractResource):
    """Database Informational Resource."""
