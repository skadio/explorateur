from collections import deque
from typing import Deque, Optional

from explorateur.search.decision import Decision
from explorateur.state.storage.base_storage import BaseStorage


class Queue(BaseStorage):
    """ Class representing a queue. """

    def __init__(self):
        super().__init__()
        self.storage: Deque[Decision] = deque()

    def insert(self, decision: Decision):
        self.storage.append(decision)

    def remove(self) -> Decision:
        return self.storage.popleft()

    def is_empty(self) -> bool:
        return self.size() == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, decision: Decision) -> Optional[Decision]:
        """ Returns the state if it is in the stack, None otherwise."""
        try:
            return self.storage[self.storage.index(decision)]
        except ValueError:
            return None
