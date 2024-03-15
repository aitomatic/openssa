"""Web informational resource."""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class WebPageResource(AbstractResource):
    """Web page informational resource."""


@global_register
class WebSearchResource(AbstractResource):
    """Web search informational resource."""
