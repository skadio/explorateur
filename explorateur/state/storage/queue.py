from collections  import deque
from typing import Deque
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.base_state import BaseState

class Queue(BaseStorage):

    def __init__(self):
        super().__init__()
        self.storage: Deque[BaseState] = deque()

    def insert(self, state: BaseState):
        self.storage.append(state)

    def remove(self) -> BaseState:
        return self.storage.popleft()

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def get_size(self) -> int:
        return len(self.storage)

    def contains(self, state: BaseState) -> BaseState:
        if state in self.storage:
            return state
        return None

    def __iter__(self):
        pass

    def __next__(self):
        pass

