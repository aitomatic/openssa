"""
========================================
[future work] RSS Informational Resource
========================================
"""


from __future__ import annotations

from .abstract import AbstractResource
from ._global import global_register


@global_register
class RssResource(AbstractResource):
    """RSS Informational Resource."""
