from typing import Set, Optional, Type

from explorateur.search.decision import Decision
from explorateur.state.storage.base_storage import BaseStorage


class HashSet(BaseStorage):
    """ Class representing a stack."""

    def __init__(self):
        super().__init__()
        self.storage: Set[Decision] = set()

    def insert(self, decision: Decision):
        self.storage.add(decision)

    def remove(self) -> Decision:
        return self.storage.pop()

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, decision: Decision) -> Optional[Decision]:
        """ Returns the state if it is in the hashset, None otherwise."""
        return decision if decision in self.storage else None
