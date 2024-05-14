from collections import deque
from typing import Deque, Optional
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.search.decision import Decision


class Stack(BaseStorage):
    """ Class representing a stack."""

    def __init__(self):
        super().__init__()
        self.storage: Deque[Decision] = deque()

    def insert(self, decision: Decision):
        self.storage.append(decision)

    def remove(self) -> Decision:
        return self.storage.pop()

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, decision: Decision) -> Optional[Decision]:
        """ Returns the state if it is in the stack, None otherwise."""
        try:
            return self.storage[self.storage.index(decision)]
        except ValueError:
            return None
