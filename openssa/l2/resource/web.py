"""Web Informational Resources."""


from .abstract import AbstractResource
from ._global import global_register


@global_register
class WebPageResource(AbstractResource):
    """Webpage Informational Resource."""


@global_register
class WebSearchResource(AbstractResource):
    """Web-Search Informational Resource."""
