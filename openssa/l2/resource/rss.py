"""RSS informational resource."""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class RssResource(AbstractResource):
    """RSS informational resource."""
