import heapq
from typing import List, Optional

from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.base_state import BaseState


class PriorityQueue(BaseStorage):
    """  Class representing a priority queue. Root is the smallest element. """

    def __init__(self):
        super().__init__()
        self.storage: List[BaseState] = list()

    def insert(self, state: BaseState):
        heapq.heappush(self.storage, (state.get_objective(), state))

    def remove(self) -> BaseState:
        """ Removes a state from the priority queue."""
        return heapq.heappop(self.storage)[1]  # the first item is the key

    def is_empty(self) -> bool:
        return len(self.storage) == 0

    def size(self) -> int:
        return len(self.storage)

    def contains(self, state: BaseState) -> Optional[BaseState]:
        """ Returns the state if it is in the priority queue, None otherwise."""
        try:
            return self.storage[self.storage.index(state)]
        except ValueError:
            return None
