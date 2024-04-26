"""Global Informational Resources Register."""


from typing import TYPE_CHECKING

from .abstract import AResource

if TYPE_CHECKING:
    from collections.abc import Callable


GLOBAL_RESOURCES: dict[str, AResource] = {}


def global_register(resource_class):
    orig_init: Callable[..., None] = resource_class.__init__

    def wrapped_init(self, *args, **kwargs) -> None:
        orig_init(self, *args, **kwargs)  # pylint: disable=unnecessary-dunder-call

        if self.unique_name not in GLOBAL_RESOURCES:
            GLOBAL_RESOURCES[self.unique_name]: AResource = self

    resource_class.__init__: Callable[..., None] = wrapped_init

    return resource_class
