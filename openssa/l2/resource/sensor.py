"""
===========================================
[future work] Sensor Informational Resource
===========================================
"""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class SensorResource(AbstractResource):
    """Sensor Informational Resource."""
