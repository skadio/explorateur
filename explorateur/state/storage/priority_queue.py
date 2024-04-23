import abc
from ast import List
import heapq
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState
from typing import Union


# need to figure out what they key is to push + where is it going to be stored


class PriorityQueue(BaseStorage):

    def __init__(self):
        super().__init__()
        self.storage = []

    def insert(self, state: _BaseState):
        """
        """
        heapq.heappush(self.storage, (state.objective_function(), state))

    def remove(self) -> _BaseState:
        """
        """
        return heapq.heappop(self.storage)[1] #the first item is the key

    def is_empty(self) -> bool:
        """
        """
        return len(self.storage) == 0

    def get_size(self) -> int:
        """
        """
        return len(self.storage)

    def contains(self, state: _BaseState) -> Union[_BaseState, None]:
        """
        """
        if state in self.storage:
            return state
        else:
            return None

    def __iter__(self):
        pass

    def __next__(self):
        pass
