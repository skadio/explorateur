from typing import NamedTuple
from explorateur.utils import check_true

class _StorageType(NamedTuple):
    class Stack(NamedTuple):
        """Stack type"""
        param: float = 0.05

        def _validate(self):
            check_true(isinstance(self.param, (int, float)),
                       TypeError("param must be an integer or float."))

    class Queue(NamedTuple):
        """Queue type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError(
                "The value of param must be greater than zero."))

    class Hash(NamedTuple):
        """Hash type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError(
                "The value of param must be greater than zero."))

    class PriorityQueue(NamedTuple):
        """PQ type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError(
                "The value of param must be greater than zero."))
