"""Global informational resources register."""


from typing import TYPE_CHECKING

from .abstract import AbstractResource

if TYPE_CHECKING:
    from collections.abc import Callable


GLOBAL_RESOURCES: dict[str, AbstractResource] = {}


def global_register(resource_class):
    orig_init: Callable[..., None] = resource_class.__init__

    def wrapped_init(self, *args, **kwargs) -> None:
        orig_init(self, *args, **kwargs)  # pylint: disable=unnecessary-dunder-call

        assert self.unique_name not in GLOBAL_RESOURCES, \
            KeyError(f'*** RESOURCE UNIQUE NAME CONFLICT: "{self.unique_name}"')
        GLOBAL_RESOURCES[self.unique_name]: AbstractResource = self

    resource_class.__init__: Callable[..., None] = wrapped_init

    return resource_class
