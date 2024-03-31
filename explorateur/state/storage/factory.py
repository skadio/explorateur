from explorateur.explorateur import _StorageType
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack

class StorageFactory:

    @staticmethod
    def create(storage_type:_StorageType):
        return Queue()
      # match type(storage_type):
      #     case _StorageType.Queue:
      #         return Queue()
      #     case _StorageType.Stack:
      #         return Stack()
      #     case _StorageType.Hash:
      #         return ValueError
      #     case _StorageType.PriorityQueue:
      #         return ValueError