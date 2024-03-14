"""File-stored informational resource."""


from functools import cached_property
import os
from pathlib import Path
from typing import TYPE_CHECKING

from fsspec.spec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.openai.base import OpenAIEmbedding

from .abstract import AbstractResource
from ._global import global_register
from ._prompts import RESOURCE_QA_PROMPT_TEMPLATE

if TYPE_CHECKING:
    from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine


@global_register
class FileResource(AbstractResource):
    """File-stored informational resource."""

    def __init__(self,
                 path: Path | str,
                 fs: AbstractFileSystem = LocalFileSystem(auto_mkdir=False),  # TODO: fix after Llama-Index bug fix
                 embed_model: BaseEmbedding = OpenAIEmbedding(), re_index: bool = False):
        """Initialize file-stored informational resource and associated RAG."""
        self.path: str = (path.resolve(strict=True)
                          if isinstance(path, Path)
                          else path.lstrip().rstrip('/\\'))

        self.embed_model_name: str = embed_model.model_name

        self.hidden_index_dir_path: str = (str(self.path / f'.{self.embed_model_name}')
                                           if isinstance(path, Path)
                                           else f'{self.path}/.{self.embed_model_name}')

        if fs.isdir(path=self.hidden_index_dir_path) and fs.ls(path=self.hidden_index_dir_path, detail=False) \
                and (not re_index):
            index: VectorStoreIndex = load_index_from_storage(
                storage_context=StorageContext.from_defaults(persist_dir=self.hidden_index_dir_path, fs=fs),
                index_id=None)

        else:
            index: VectorStoreIndex = VectorStoreIndex.from_documents(
                documents=SimpleDirectoryReader(input_dir=self.path,
                                                input_files=None,
                                                exclude=[
                                                    '.DS_Store',  # MacOS
                                                    '*.json',  # potential nested index files
                                                ],
                                                exclude_hidden=False,
                                                errors='strict',
                                                recursive=True,
                                                encoding='utf-8',
                                                filename_as_id=False,
                                                required_exts=None,
                                                file_extractor=None,
                                                num_files_limit=None,
                                                file_metadata=None,
                                                fs=fs).load_data(show_progress=True,
                                                                 num_workers=os.cpu_count()),
                storage_context=None,
                show_progress=True,
                callback_manager=None,
                transformations=None)

            index.storage_context.persist(persist_dir=self.hidden_index_dir_path, fs=fs)

        self.query_engine: RetrieverQueryEngine = index.as_query_engine()

    @cached_property
    def unique_name(self) -> str:
        """Return globally-unique name of file-stored informational resource."""
        return self.hidden_index_dir_path

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of file-stored informational resource."""
        return os.path.basename(self.path)

    def __repr__(self) -> str:
        """Return string representation of file-stored informational resource."""
        return f'"{self.name}" {type(self).__name__}[{self.path}]'

    def answer(self, question: str, n_words: int = 300) -> str:
        """Answer question by RAG from file-stored informational resource."""
        return self.query_engine.query(RESOURCE_QA_PROMPT_TEMPLATE.format(n_words=n_words, question=question)).response
