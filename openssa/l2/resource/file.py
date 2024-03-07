"""File-stored informational resource."""


from functools import cached_property
import os
from pathlib import Path
from typing import TYPE_CHECKING

# pylint: disable=unused-import
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.settings import Settings

from openssa.integrations.llama_index.backend import Backend as LlamaIndexRAG
from openssa import LlamaIndexSSM

from .abstract import AbstractResource
from ._global import global_register

if TYPE_CHECKING:
    from openssa.core.backend.rag_backend import AbstractRAGBackend
    from openssa.core.ssm.rag_ssm import RAGSSM


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
        """Return globally-unique name."""
        return self.path

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name."""
        return os.path.basename(self.path)

    def __repr__(self) -> str:
        """Return string representation."""
        return f'"{self.name}" {type(self).__name__}[{self.path}]'

    def answer(self, question: str) -> str:
        """Answer question from informational resource."""
        return self.rag.discuss(user_input=question)['content']
