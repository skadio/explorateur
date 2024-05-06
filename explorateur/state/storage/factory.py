"""  This module contains the StorageFactory class which is responsible
for creating different types of storage objects. """
from explorateur.search.storage_type import _StorageType
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.priority_queue import PriorityQueue
from explorateur.state.storage.base_storage import BaseStorage


class StorageFactory:
    """
    A factory class for creating different types of storage objects.
    """

    @staticmethod
    def create(storage_type: _StorageType) -> BaseStorage:
        """
        Create a storage object based on the given storage type.

        Args:
            storage_type (_StorageType): The type of storage to create.

        Returns:
            BaseStorage: The created storage object.

        Raises:
            ValueError: If the storage type is None or not recognized.

        """
        # Implementation code goes here
        if storage_type is None:
            raise ValueError
        elif isinstance(storage_type, _StorageType.Queue):
            return Queue()
        elif isinstance(storage_type, _StorageType.Stack):
            return Stack()
        elif isinstance(storage_type, _StorageType.PriorityQueue):
            return PriorityQueue()
        elif isinstance(storage_type, _StorageType.Hash):
            raise ValueError
        else:
            raise ValueError
