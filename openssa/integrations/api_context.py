from abc import abstractmethod, ABC
from typing import Optional
from pydantic import BaseModel


# pylint: disable=too-many-instance-attributes
class AbstractAPIContext(BaseModel, ABC):
    type: Optional[str] = None
    key: Optional[str] = None
    base: Optional[str] = None
    version: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    is_chat_completion: Optional[bool] = None

    @classmethod
    @abstractmethod
    def from_defaults(cls):
        """Return a new instance of this class with default values filled in."""
