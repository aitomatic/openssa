"""
===========================================
[future work] Sensor Informational Resource
===========================================
"""


from __future__ import annotations

from .base import BaseResource
from ._global import global_register


@global_register
class SensorResource(BaseResource):
    """Sensor Informational Resource."""
