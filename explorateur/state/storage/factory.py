from explorateur.search.storage_type import _StorageType
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state._base_state import _BaseState

class StorageFactory:

    @staticmethod
    def create(storage_type:_StorageType) -> BaseStorage:
      match storage_type:
          case _StorageType.Queue(param=p):
              return Queue()
          case _StorageType.Stack(param=p):
              return Stack()
          case _StorageType.Hash(param=p):
              raise ValueError
          case _StorageType.PriorityQueue(param=p):
              raise ValueError
          case _:
              raise ValueError
