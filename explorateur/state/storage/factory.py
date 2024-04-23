from explorateur.search.storage_type import _StorageType
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.priority_queue import PriorityQueue
from explorateur.state.storage.base_storage import BaseStorage


class StorageFactory:

    @staticmethod
    def create(storage_type: _StorageType) -> BaseStorage:
        if storage_type is None:
            raise ValueError
        elif isinstance(storage_type, _StorageType.Queue):
            return Queue
        elif isinstance(storage_type, _StorageType.Stack):
            return Stack()
        elif isinstance(storage_type, _StorageType.PriorityQueue):
            return PriorityQueue()
        elif isinstance(storage_type, _StorageType.Hash):
            raise ValueError
        else:
            raise ValueError
