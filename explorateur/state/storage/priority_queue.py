import heapq
from typing import List, Optional

from explorateur.search.decision import Decision
from explorateur.state.storage.base_storage import BaseStorage


class PriorityQueue(BaseStorage):
    """  Class representing a priority queue. Root is the smallest element. """

    def __init__(self):
        super().__init__()
        self.storage: List[Decision] = list()

    def insert(self, decision: Decision):
        heapq.heappush(self.storage, (decision.state.get_objective(), decision))

    def remove(self) -> Decision:
        """ Removes a state from the priority queue."""
        return heapq.heappop(self.storage)[1]  # the first item is the key

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, decision: Decision) -> Optional[Decision]:
        """ Returns the state if it is in the priority queue, None otherwise."""
        try:
            return self.storage[self.storage.index(decision)]
        except ValueError:
            return None
