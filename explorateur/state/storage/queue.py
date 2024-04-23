from collections import deque
from typing import Deque
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState
from typing import Union


class Queue(BaseStorage):

    def __init__(self):
        super().__init__()
        self.storage: Deque[_BaseState] = deque()

    def insert(self, state: _BaseState):
        self.storage.append(state)

    def remove(self) -> _BaseState:
        return self.storage.popleft()

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def get_size(self) -> int:
        return len(self.storage)

    def contains(self, state: _BaseState) -> Union[_BaseState, None]:
        if state in self.storage:
            return state
        return None

    def __iter__(self):
        pass

    def __next__(self):
        pass
