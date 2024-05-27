"""
=============================================
[future work] Database Informational Resource
=============================================
"""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class DbResource(AbstractResource):
    """Database Informational Resource."""
