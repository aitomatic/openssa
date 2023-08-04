import os
from abc import abstractmethod, ABC
from openssm.core.backend.base_backend import BaseBackend
from openssm.utils.utils import Utils
from openssm.utils.logs import Logs


class AbstractRAGBackend(BaseBackend, ABC):
    def __init__(self):
        super().__init__()

    @Logs.do_log_entry_and_exit()
    def _get_source_dir(self, storage_dir: str):
        return os.path.join(storage_dir, ".sources")

    @Logs.do_log_entry_and_exit()
    def _get_index_dir(self, storage_dir: str):
        return os.path.join(storage_dir, ".indexes")

    @Logs.do_log_entry_and_exit()
    def _load_index_if_exists(self, storage_dir: str) -> bool:
        """
        Attempt to load an existing index from the storage directory.
        Returns True if an index was loaded, False otherwise.

        @param storage_dir: The path to the base storage directory.
        """
        index_dir = self._get_index_dir(storage_dir)
        if os.path.isdir(index_dir) and len(os.listdir(index_dir)) != 0:
            self.load(storage_dir)
            return True

        return False

    @abstractmethod
    def _do_read_directory(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    @Logs.do_log_entry_and_exit()
    def read_directory(self, storage_dir: str, use_existing_index: bool = True):
        """
        Read a directory of documents and create an index.

        @param storage_dir: The path to the base storage directory.
        @param use_existing_index: [optional] If True, try to load an existing index from the storage directory first.

        Side effects:
        - If use_existing_index is True, the index will be automatically saved (for future use)
        """
        success = False

        if use_existing_index:
            success = self._load_index_if_exists(storage_dir)

        if not success or not use_existing_index:
            self._do_read_directory(storage_dir)
            if use_existing_index:
                # Side effect: save the index to the storage directory
                self.save(storage_dir)

    def read_gdrive(self, folder_id: str, storage_dir: str, use_existing_index: bool = True):
        """
        Read a directory of documents from a Google Drive folder and create an index.
        Internally, the documents will first be downloaded to a local directory.

        @param folder_id: The ID of the Google Drive folder.
        @param storage_dir: The path to the base storage directory.
        @param use_existing_index: [optional] If True, try to load an existing index from the storage directory first.

        Side effects:
        - If use_existing_index is True, the index will be automatically saved (for future use)
        """
        success = False

        if use_existing_index:
            success = self._load_index_if_exists(storage_dir)

        if not success or not use_existing_index:
            Utils.download_gdrive(folder_id, self._get_source_dir(storage_dir))
            self.read_directory(storage_dir, use_existing_index)

    @abstractmethod
    def _do_save(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    def save(self, storage_dir: str):
        """
        Save the index to the storage directory.

        @param storage_dir: The path to the base storage directory.
        """
        self._do_save(storage_dir)
        return super().save(storage_dir)

    @abstractmethod
    def _do_load(self, storage_dir: str):
        """
        Must be implemented by subclasses.

        @param storage_dir: The path to the base storage directory.
        """
        pass

    def load(self, storage_dir: str):
        """
        Load the index from the storage directory.

        @param storage_dir: The path to the base storage directory.
        """
        self._do_load(storage_dir)
        return super().load(storage_dir)
