from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.priority_queue import PriorityQueue
from explorateur.state.storage.hash import HashSet
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from explorateur.utils import All_Exploration_Types
from typing import Union, Optional


class StorageFactory:
    """ A factory class for creating different types of storage objects."""

    factory = {ExplorationType.BestFirst: PriorityQueue,
               ExplorationType.BreadthFirst: Queue,
               ExplorationType.DepthFirst: Stack,
               SearchType.GraphSearch: HashSet}

    @staticmethod
    def create(storage_type: Union[All_Exploration_Types, SearchType.GraphSearch]) -> Optional[BaseStorage]:
        """
        Create a storage object based on the given storage type.
        If storage type does not exist, returns None.

        Args:
            storage_type (Union[All_Exploration_Types, SearchType.GraphSearch]): The type of storage to create.

        Returns:
            Optional(BaseStorage): The created storage object or None if storage type does not exist.

        """
        storage = StorageFactory.factory.get(type(storage_type))
        return storage() if storage else None
