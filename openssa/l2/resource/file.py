"""File-stored informational resource."""


from functools import cached_property
import os
from pathlib import Path

from openssa import LlamaIndexSSM

from .abstract import AbstractResource
from ._global import global_register
from ._prompts import RESOURCE_QA_PROMPT_TEMPLATE


@global_register
class FileResource(AbstractResource):
    """File-stored informational resource."""

    def __init__(self, path: Path | str):
        """Initialize file-stored informational resource and associated RAG."""
        self.path: str = (str(path.resolve(strict=True))
                          if isinstance(path, Path)
                          else path.lstrip().rstrip('/\\'))

        self.rag = LlamaIndexSSM()
        if self.path.startswith('s3://'):
            self.rag.read_s3(s3_paths=self.path)
        else:
            self.rag.read_directory(storage_dir=self.path)

    @cached_property
    def unique_name(self) -> str:
        """Return globally-unique name of file-stored informational resource."""
        return self.path

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of file-stored informational resource."""
        return os.path.basename(self.path)

    def __repr__(self) -> str:
        """Return string representation of file-stored informational resource."""
        return f'"{self.name}" {type(self).__name__}[{self.path}]'

    def answer(self, question: str, n_words: int = 300) -> str:
        """Answer question by RAG from file-stored informational resource."""
        return self.rag.discuss(RESOURCE_QA_PROMPT_TEMPLATE.format(n_words=n_words, question=question))['content']
