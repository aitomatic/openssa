"""Web informational resource."""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class WebResource(AbstractResource):
    """Web informational resource."""
