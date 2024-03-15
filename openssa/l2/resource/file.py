"""File-stored informational resource."""


from collections.abc import Collection
from dataclasses import dataclass, field, InitVar
from functools import cached_property
import os
from pathlib import Path
from tempfile import mkdtemp
from typing import TypeVar

from fsspec.spec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from gcsfs.core import GCSFileSystem
from s3fs.core import S3FileSystem

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.openai.base import OpenAIEmbedding
from llama_index.llms.openai.base import OpenAI as OpenAILM

from .abstract import AbstractResource
from ._global import global_register
from ._prompts import RESOURCE_QA_PROMPT_TEMPLATE


# file suffixes: text files, plus a subset of those supported by Llama Index
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


AFileSystem: TypeVar = TypeVar('AFileSystem', bound=AbstractFileSystem, covariant=False, contravariant=False)

# GCS file system
_GCS_PROTOCOL_PREFIX: str = 'gcs://'
_GCS_PROTOCOL_PREFIX_LEN: int = len(_GCS_PROTOCOL_PREFIX)

# S3 file system
_S3_PROTOCOL_PREFIX: str = 's3://'
_S3_PROTOCOL_PREFIX_LEN: int = len(_S3_PROTOCOL_PREFIX)


type DirOrFileStrPath = str
type FileStrPathSet = frozenset[DirOrFileStrPath]

AnEmbedModel: TypeVar = TypeVar('AnEmbedModel', bound=BaseEmbedding, covariant=False, contravariant=False)
AnLM: TypeVar = TypeVar('AnLM', bound=BaseLLM, covariant=False, contravariant=False)


@global_register
@dataclass(init=True,
           repr=True,
           eq=True,
           order=False,
           unsafe_hash=False,
           frozen=False,  # mutable
           match_args=True,
           kw_only=False,
           slots=False)
class FileResource(AbstractResource):
    """File-stored informational resource."""

    path: Path | DirOrFileStrPath

    embed_model: AnEmbedModel = field(default_factory=OpenAIEmbedding)
    re_index: InitVar[bool] = False

    lm: AnLM = field(default_factory=OpenAILM)

    def __post_init__(self, re_index: bool):
        """Post-initialize file-stored informational resource."""
        if isinstance(self.path, Path):
            self.path: Path = self.path.resolve(strict=True)
            self.str_path: DirOrFileStrPath = str(self.path)

        else:
            self.str_path = self.path = self.path.lstrip().rstrip('/\\')
            if not self.on_remote:
                self.str_path = self.path = os.path.abspath(path=self.path)

        self.embed_model_name: str = self.embed_model.model_name

        self.to_re_index: bool = re_index

        self.index_dir_str_path: DirOrFileStrPath = ((str(self.path / f'.{self.embed_model_name}')
                                                      if isinstance(self.path, Path)
                                                      else os.path.join(self.path, f'.{self.embed_model_name}'))
                                                     if self.is_dir
                                                     else mkdtemp(suffix=None, prefix=None, dir=None))

    def __hash__(self) -> int:
        """Return integer hash."""
        return hash(self.unique_name)

    @cached_property
    def unique_name(self) -> str:
        """Return globally-unique name of file-stored informational resource."""
        return self.index_dir_str_path

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of file-stored informational resource."""
        return os.path.basename(self.path)

    @cached_property
    def on_gcs(self) -> bool:
        """Check if source is on GCS."""
        return self.str_path.startswith(_GCS_PROTOCOL_PREFIX)

    @cached_property
    def on_s3(self) -> bool:
        """Check if source is on S3."""
        return self.str_path.startswith(_S3_PROTOCOL_PREFIX)

    @cached_property
    def on_remote(self) -> bool:
        """Check if source is on remote file service."""
        return self.on_gcs or self.on_s3

    @cached_property
    def fs(self) -> AFileSystem:
        """Get applicable file system."""
        if self.on_gcs:
            return GCSFileSystem()

        if self.on_s3:
            return S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'), secret=os.environ.get('AWS_SECRET_ACCESS_KEY'))

        return LocalFileSystem(auto_mkdir=True, use_listings_cache=False, listings_expiry_time=None, max_paths=None)

    @cached_property
    def native_str_path(self) -> DirOrFileStrPath:
        """Get path without protocol prefix (e.g., "gcs://", "s3://")."""
        if self.on_gcs:
            return self.str_path[_GCS_PROTOCOL_PREFIX_LEN:]

        if self.on_s3:
            return self.str_path[_S3_PROTOCOL_PREFIX_LEN:]

        return self.str_path

    @cached_property
    def is_dir(self) -> bool:
        """Check if source is directory."""
        return self.fs.isdir(self.native_str_path)

    @cached_property
    def is_single_file(self) -> bool:
        """Check if source is single file."""
        return self.fs.isfile(self.native_str_path)

    def file_paths(self, *, relative: bool = False, suffixes: Collection[str] = _DEFAULT_SUFFIXES) -> FileStrPathSet:
        """Get file paths with relevant suffixes from provided path."""
        if self.is_dir:
            native_str_path_w_trail_slash: DirOrFileStrPath = f'{self.native_str_path}/'
            path_len_wo_protocol_prefix_w_trail_slash: int = len(native_str_path_w_trail_slash)

            file_paths: list[str] = sum((self.fs.glob(f'{native_str_path_w_trail_slash}**/*{suffix}')
                                         for suffix in suffixes), start=[])
            file_relpaths: FileStrPathSet = frozenset(_[path_len_wo_protocol_prefix_w_trail_slash:] for _ in file_paths)

            return file_relpaths if relative else frozenset(f'{self.path}/{_}' for _ in file_relpaths)

        assert self.is_single_file and (Path(self.path).suffix in suffixes), \
            ValueError(f'"{self.path}" not a file with suffix among {suffixes}')
        return frozenset({self.path})

    @cached_property
    def query_engine(self) -> RetrieverQueryEngine:
        if self.is_dir and (self.fs.isdir(path=self.index_dir_str_path) and
                            self.fs.ls(path=self.index_dir_str_path, detail=False)) and (not self.to_re_index):
            index: VectorStoreIndex = load_index_from_storage(
                storage_context=StorageContext.from_defaults(
                    # docs.llamaindex.ai/en/latest/api_reference/storage.html#llama_index.core.storage.storage_context.StorageContext.from_defaults
                    docstore=None,
                    index_store=None,
                    vector_store=None,
                    image_store=None,
                    vector_stores=None,
                    graph_store=None,
                    persist_dir=self.index_dir_str_path,
                    fs=self.fs),
                index_id=None,

                # other BaseIndex.__init__(...) args:
                # docs.llamaindex.ai/en/latest/api_reference/indices.html#llama_index.core.indices.base.BaseIndex
                nodes=None,
                objects=None,
                callback_manager=None,
                transformations=None,
                show_progress=True)

        else:
            fs: AFileSystem | None = self.fs if self.is_dir else None

            index: VectorStoreIndex = VectorStoreIndex.from_documents(
                # BaseIndex.from_documents(...) args:
                # docs.llamaindex.ai/en/latest/api_reference/indices.html#llama_index.core.indices.base.BaseIndex.from_documents
                documents=SimpleDirectoryReader(
                    # docs.llamaindex.ai/en/latest/examples/data_connectors/simple_directory_reader.html#full-configuration
                    input_dir=self.native_str_path,
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
                    fs=fs,
                ).load_data(show_progress=True,
                            num_workers=os.cpu_count()),
                storage_context=None,
                show_progress=True,
                callback_manager=None,
                transformations=None,

                # other VectorStoreIndex.__init__(...) args:
                # docs.llamaindex.ai/en/latest/api_reference/indices/vector_store.html#llama_index.core.indices.vector_store.base.VectorStoreIndex
                use_async=False,
                store_nodes_override=False,
                embed_model=self.embed_model,
                insert_batch_size=2048,
                objects=None,
                index_struct=None)

            index.storage_context.persist(
                # docs.llamaindex.ai/en/latest/api_reference/storage.html#llama_index.core.storage.storage_context.StorageContext.persist
                persist_dir=self.index_dir_str_path,
                fs=fs)

        return index.as_query_engine(
            # docs.llamaindex.ai/en/latest/understanding/querying/querying.html
            llm=self.lm,

            # other RetrieverQueryEngine.from_args(...) args:
            # docs.llamaindex.ai/en/latest/api_reference/query/query_engines/retriever_query_engine.html#llama_index.core.query_engine.retriever_query_engine.RetrieverQueryEngine.from_args
            response_synthesizer=None,
            node_postprocessors=None,
            response_mode=ResponseMode.COMPACT,
            text_qa_template=None,
            refine_template=None,
            summary_template=None,
            simple_template=None,
            output_cls=None,
            use_async=False,
            streaming=False)

    def answer(self, question: str, n_words: int = 300) -> str:
        """Answer question by RAG from file-stored informational resource."""
        return self.query_engine.query(RESOURCE_QA_PROMPT_TEMPLATE.format(n_words=n_words, question=question)).response
