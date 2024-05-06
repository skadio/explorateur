""" Contains the Queue class, subclass of BaseStorage """
from collections import deque
from typing import Deque
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState


class Queue(BaseStorage):
    """ Class representing a queue. """

    def __init__(self):
        super().__init__()
        self.storage: Deque[_BaseState] = deque()

    def insert(self, state: _BaseState):
        """ Inserts a state into the queue."""
        self.storage.append(state)

    def remove(self) -> _BaseState:
        """ Removes a state from the queue."""
        return self.storage.popleft()

    def is_empty(self) -> bool:
        """ Returns True if the queue is empty, False otherwise."""
        return self.get_size() == 0

    def get_size(self) -> int:
        """ Returns the number of elements in the queue."""
        return len(self.storage)

    def contains(self, state: _BaseState) -> bool:
        """ Returns True if the state is in the queue, False otherwise."""
        return state in self.storage
