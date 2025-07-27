"""
========================================
[future work] RSS Informational Resource
========================================
"""


from __future__ import annotations

from .base import BaseResource
from ._global import global_register


@global_register
class RssResource(BaseResource):
    """RSS Informational Resource."""
