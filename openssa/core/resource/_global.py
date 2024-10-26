"""Global Resources Register."""


from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from .base import BaseResource


GLOBAL_RESOURCES: dict[str, BaseResource] = {}


def global_register(resource_class):
    orig_init: Callable[..., None] = resource_class.__init__

    def wrapped_init(self, *args, **kwargs) -> None:
        orig_init(self, *args, **kwargs)  # pylint: disable=unnecessary-dunder-call

        if self.unique_name not in GLOBAL_RESOURCES:
            GLOBAL_RESOURCES[self.unique_name]: BaseResource = self

    resource_class.__init__: Callable[..., None] = wrapped_init

    return resource_class
