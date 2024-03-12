"""Sensor informational resource."""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class SensorResource(AbstractResource):
    """Sensor informational resource."""
