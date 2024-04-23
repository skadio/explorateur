'''Module providing the ExplorationType class to be passed into explorateur.'''
from typing import NamedTuple
from explorateur.utils import check_true
from explorateur.search.storage_type import _StorageType


class ExplorationType(NamedTuple):
    """Exploration Type"""
    storage_type: _StorageType

    class DepthFirst(NamedTuple):
        "DepthFirst Type"
        storage_type: _StorageType = _StorageType.Stack()
        param: float = 1.0

        def _validate(self):
            check_true(isinstance(self.param, (int, float)),
                       TypeError("param must be an integer or float."))

    class BestFirst(NamedTuple):
        "BestFirst Type"
        storage_type: _StorageType = _StorageType.PriorityQueue()
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError(
                "The value of param must be greater than zero."))

    class BreadthFirst(NamedTuple):
        "BreadthFirst Type"
        storage_type: _StorageType = _StorageType.Queue()
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError(
                "The value of param must be greater than zero."))
