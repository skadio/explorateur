from typing import Set, Optional

from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.base_state import BaseState


class HashSet(BaseStorage):
    """ Class representing a stack."""

    def __init__(self):
        super().__init__()
        self.storage: Set[BaseState] = set()

    def insert(self, state: BaseState):
        self.storage.add(state)

    def remove(self) -> BaseState:
        return self.storage.pop()

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, state: BaseState) -> Optional[BaseState]:
        """ Returns the state if it is in the hashset, None otherwise."""
        return state if state in self.storage else None
