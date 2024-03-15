"""File-stored informational resource."""


from collections.abc import Collection
from dataclasses import dataclass
from functools import cached_property
import os
from pathlib import Path
from typing import TYPE_CHECKING

from fsspec.spec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from gcsfs.core import GCSFileSystem
from s3fs.core import S3FileSystem

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


# file suffixes: text files, plus a subset of those supported Llama Index
_DEFAULT_SUFFIXES: tuple[str] = (
    '.txt',
    '.pdf',
    '.docx',
    '.pptx',
    # '.jpg', '.jpeg', '.png',
    # '.mp3', '.mp4',
    '.csv',
    # '.epub',
    '.md',
    # '.mbox',
    # '.ipynb',
)


# local file system
_LOCAL_FS = LocalFileSystem(auto_mkdir=True, use_listings_cache=False, listings_expiry_time=None, max_paths=None)

# GCS file system
# _GCS_FS = GCSFileSystem()
_GCS_PROTOCOL_PREFIX: str = 'gcs://'
_GCS_PROTOCOL_PREFIX_LEN: int = len(_GCS_PROTOCOL_PREFIX)

# S3 file system
_S3_FS = S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'), secret=os.environ.get('AWS_SECRET_ACCESS_KEY'))
_S3_PROTOCOL_PREFIX: str = 's3://'
_S3_PROTOCOL_PREFIX_LEN: int = len(_S3_PROTOCOL_PREFIX)


# explicit typing for clarity to developers/maintainers
type DirOrFilePath = str
type FilePathSet = frozenset[DirOrFilePath]


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True,  # frozen -> hashable
           match_args=True, kw_only=False, slots=False)
class FileSource:
    """Manager class for files on local storage or cloud object storage (S3/GCS/GDrive/ADL)."""

    path: DirOrFilePath

    @cached_property
    def on_gcs(self) -> bool:
        """Check if source is on GCS."""
        return self.path.startswith(_GCS_PROTOCOL_PREFIX)

    @cached_property
    def on_s3(self) -> bool:
        """Check if source is on S3."""
        return self.path.startswith(_S3_PROTOCOL_PREFIX)

    @cached_property
    def native_path(self) -> DirOrFilePath:
        """Get path without protocol prefix (e.g., "gcs://", "s3://")."""
        if self.on_gcs:
            return self.path[_GCS_PROTOCOL_PREFIX_LEN:]

        if self.on_s3:
            return self.path[_S3_PROTOCOL_PREFIX_LEN:]

        return self.path

    @cached_property
    def fs(self) -> AbstractFileSystem:  # pylint: disable=invalid-name
        """Get applicable file system."""
        if self.on_gcs:
            return GCSFileSystem()

        if self.on_s3:
            return _S3_FS

        return _LOCAL_FS

    @cached_property
    def is_dir(self) -> bool:
        """Check if source is directory."""
        return self.fs.isdir(self.native_path)

    @cached_property
    def is_single_file(self) -> bool:
        """Check if source is single file."""
        return self.fs.isfile(self.native_path)

    def file_paths(self, *, relative: bool = False, suffixes: Collection[str] = _DEFAULT_SUFFIXES) -> FilePathSet:
        """Get file paths with relevant suffixes from provided path."""
        if self.is_dir:
            native_path_w_trail_slash: DirOrFilePath = f'{self.native_path}/'
            path_len_wo_protocol_prefix_w_trail_slash: int = len(native_path_w_trail_slash)

            file_paths: list[str] = sum((self.fs.glob(f'{native_path_w_trail_slash}**/*{suffix}')
                                         for suffix in suffixes), start=[])
            file_relpaths: FilePathSet = frozenset(_[path_len_wo_protocol_prefix_w_trail_slash:] for _ in file_paths)

            return file_relpaths if relative else frozenset(f'{self.path}/{_}' for _ in file_relpaths)

        assert self.is_single_file and (Path(self.path).suffix in suffixes), \
            ValueError(f'"{self.path}" not a file with suffix among {suffixes}')
        return frozenset({self.path})
