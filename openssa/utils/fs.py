"""Utilities for managing files on local storage or cloud object storage (S3/GCS/GDrive/ADL)."""


from collections.abc import Collection, Sequence
from dataclasses import dataclass
from functools import cached_property
import os
from pathlib import Path

from fsspec.spec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from gcsfs.core import GCSFileSystem
from s3fs.core import S3FileSystem


__all__: Sequence[str] = 'DirOrFilePath', 'FilePathSet', 'FileSource'


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
_GCS_FS = GCSFileSystem()
_GCS_PROTOCOL_PREFIX: str = 'gcs://'
_GCS_PROTOCOL_PREFIX_LEN: int = len(_GCS_PROTOCOL_PREFIX)

# S3 file system
_S3_FS = S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'), secret=os.environ.get('AWS_SECRET_ACCESS_KEY'))
_S3_PROTOCOL_PREFIX: str = 's3://'
_S3_PROTOCOL_PREFIX_LEN: int = len(_S3_PROTOCOL_PREFIX)


# explicit typing for clarity to developers/maintainers
DirOrFilePath: type = str
FilePathSet: type = frozenset[DirOrFilePath]


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
            return _GCS_FS

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

            file_paths: list[str] = sum((self.fs.glob(f'{native_path_w_trail_slash}**{suffix}')
                                         for suffix in suffixes), start=[])
            file_relpaths: FilePathSet = frozenset(_[path_len_wo_protocol_prefix_w_trail_slash:] for _ in file_paths)

            return file_relpaths if relative else frozenset(f'{self.path}/{_}' for _ in file_relpaths)

        assert self.is_single_file and (Path(self.path).suffix in suffixes), \
            ValueError(f'"{self.path}" not a file with suffix among {suffixes}')
        return frozenset({self.path})
