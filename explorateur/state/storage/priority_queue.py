''' Contains the PriorityQueue class, which is a subclass of BaseStorage.'''
import heapq
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState


class PriorityQueue(BaseStorage):
    ''' Class representing a priority queue.'''

    def __init__(self):
        super().__init__()
        self.storage = []

    def insert(self, state: _BaseState):
        """ Inserts a state into the priority queue."""
        heapq.heappush(self.storage, (state.objective_function(), state))

    def remove(self) -> _BaseState:
        """ Removes a state from the priority queue."""
        return heapq.heappop(self.storage)[1]  # the first item is the key

    def is_empty(self) -> bool:
        """ Returns True if the priority queue is empty, False otherwise."""
        return len(self.storage) == 0

    def get_size(self) -> int:
        """ Returns the number of elements in the priority queue."""
        return len(self.storage)

    def contains(self, state: _BaseState) -> bool:
        """ Returns the state if it is in the priority queue, None otherwise."""
        return state in self.storage
