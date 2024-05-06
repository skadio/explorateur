"""  Contains the Stack class which is a subclass of BaseStorage """
from collections import deque
from typing import Deque
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState
from typing import Union


class Stack(BaseStorage):
    """  Class representing a stack."""

    def __init__(self):
        super().__init__()
        self.storage: Deque[_BaseState] = deque()

    def insert(self, state: _BaseState):
        """ Inserts a state into the stack."""
        self.storage.append(state)

    def remove(self) -> _BaseState:
        """ Removes a state from the stack."""
        return self.storage.pop()

    def is_empty(self) -> bool:
        """ Returns True if the stack is empty, False otherwise."""
        return len(self.storage) == 0

    def get_size(self) -> int:
        """ Returns the number of elements in the stack."""
        return len(self.storage)

    def contains(self, state: _BaseState) -> bool:
        """ Returns the state if it is in the stack, None otherwise."""
        return state in self.storage
