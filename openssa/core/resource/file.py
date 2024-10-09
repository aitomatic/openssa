"""
==================================
FILE-STORED INFORMATIONAL RESOURCE
==================================

`FileResource` enables querying information from directories or files
stored either locally or on remote cloud file storage services.

This implementation employs `LlamaIndex`-based Retrieval-Augmented Generation (RAG)
to index such file-stored content into vector indices, and to respond to information queries.

A file resource needs to be specified with a local or remote cloud directory/file path,
a `LlamaIndex`-compliant embedding model and a `LlamaIndex`-compliant LM.
"""


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

from llama_index.core.base.embeddings.base import BaseEmbedding as LlamaIndexEmbedModel
from llama_index.core.base.llms.base import BaseLLM as LlamaIndexLM
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core.readers.file.base import SimpleDirectoryReader
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.vector_stores.types import VectorStoreQueryMode

from openssa.core.util.lm.openai import default_llama_index_openai_embed_model, default_llama_index_openai_lm

from .base import BaseResource
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

# S3 file system
_S3_PROTOCOL_PREFIX: str = 's3://'


type DirOrFileStrPath = str
type FileStrPathSet = frozenset[DirOrFileStrPath]


@global_register
@dataclass
class FileResource(BaseResource):
    """File-stored Informational Resource."""

    # directory or file path to file-stored Informational Resource
    path: Path | DirOrFileStrPath

    # embedding model for indexing and retrieving information
    embed_model: LlamaIndexEmbedModel = field(default_factory=default_llama_index_openai_embed_model,
                                              init=True,
                                              repr=False,
                                              hash=None,
                                              compare=True,
                                              metadata=None,
                                              kw_only=True)

    # whether to re-index information upon initialization
    re_index: InitVar[bool] = False

    # language model for generating answers
    lm: LlamaIndexLM = field(default_factory=default_llama_index_openai_lm,
                             init=True,
                             repr=False,
                             hash=None,
                             compare=True,
                             metadata=None,
                             kw_only=True)

    def __post_init__(self, re_index: bool):
        """Post-initialize file-stored Informational Resource."""
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
        """Return globally-unique name of file-stored Informational Resource."""
        return self.index_dir_str_path

    @cached_property
    def name(self) -> str:
        """Return potentially non-unique, but informationally helpful name of file-stored Informational Resource."""
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

        return LocalFileSystem(auto_mkdir=False,  # note: important for being recognized as default FS on Windows
                               use_listings_cache=False, listings_expiry_time=None, max_paths=None)

    @cached_property
    def native_str_path(self) -> DirOrFileStrPath:
        """Get path without protocol prefix (e.g., "gcs://", "s3://")."""
        return self.fs._strip_protocol(path=self.str_path)  # pylint: disable=protected-access

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
        """Return RAG query engine."""
        # TODO: get Llama Index to fix known issues:
        # - error with remote FS when using Windows:
        #   github.com/run-llama/llama_index/issues/11810
        # - loading from remote FS encounters error `.load_data() got unexpected keyword argument 'fs'`:
        #   github.com/run-llama/llama_index/issues/9793

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
                    input_dir=self.native_str_path if self.on_remote else self.str_path,
                    input_files=None,
                    exclude=[
                        '.DS_Store',  # MacOS
                        '*.json',  # potential nested index files
                    ],
                    exclude_hidden=False,
                    errors='strict',
                    recursive=self.is_dir,
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

            # other VectorIndexRetriever.__init__(...) args:
            # docs.llamaindex.ai/en/latest/api_reference/query/retrievers/vector_store.html#llama_index.core.indices.vector_store.retrievers.retriever.VectorIndexRetriever
            similarity_top_k=12,
            vector_store_query_mode=VectorStoreQueryMode.MMR,
            filters=None,
            alpha=None,
            doc_ids=None,
            sparse_top_k=None,
            vector_store_kwargs={'mmr_threshold': 0.5},
            embed_model=self.embed_model,
            verbose=False,

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

    def answer(self, question: str, n_words: int = 1000) -> str:
        """Answer question by RAG from file-stored Informational Resource."""
        prompt: str = RESOURCE_QA_PROMPT_TEMPLATE.format(n_words=n_words, question=question)

        for _ in range(9):
            answer: str = self.query_engine.query(prompt).response

            if not answer.strip().lower().startswith('repeat'):
                break

        return answer
