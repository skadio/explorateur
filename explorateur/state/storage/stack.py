from collections import deque
from typing import Deque, Optional
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.base_state import BaseState


class Stack(BaseStorage):
    """ Class representing a stack."""

    def __init__(self):
        super().__init__()
        self.storage: Deque[BaseState] = deque()

    def insert(self, state: BaseState):
        self.storage.append(state)

    def remove(self) -> BaseState:
        return self.storage.pop()

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, state: BaseState) -> Optional[BaseState]:
        """ Returns the state if it is in the stack, None otherwise."""
        try:
            return self.storage[self.storage.index(state)]
        except ValueError:
            return None
