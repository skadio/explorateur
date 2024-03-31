import abc
import heapq
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.base_state import BaseState

from collections import deque

# need to figure out what they key is to push + where is it going to be stored


class PriorityQueue(BaseStorage):

    @abc.abstractmethod
    def __init__(self):
        """Abstract method.
        """
        super().__init__()
        # self.storage: heap = heapq()

    @abc.abstractmethod
    def insert(self, state: BaseState):
        """
        """
        self.storage.append(state)

    @abc.abstractmethod
    def remove(self, state: BaseState) -> BaseState:
        """
        """
        return self.storage.remove(state)

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """
        """
        pass

    @abc.abstractmethod
    def get_size(self) -> int:
        """
        """
        pass

    @abc.abstractmethod
    def contains(self, state: BaseState) -> BaseState:
        """
        """

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass
