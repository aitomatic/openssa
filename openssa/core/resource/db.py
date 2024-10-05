"""
==============================================
[future work] Database Informational Resources
==============================================
"""


from __future__ import annotations

from .base import BaseResource
from ._global import global_register


@global_register
class DbResource(BaseResource):
    """Database Informational Resource."""
