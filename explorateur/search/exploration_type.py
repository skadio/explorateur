from typing import NamedTuple


class ExplorationType(NamedTuple):

    class BestFirst(NamedTuple):
        # _storage: _Storage = _Storage.PriorityQueue()
        pass

    class BreadthFirst(NamedTuple):
        # _storage: _Storage = _Storage.Queue()
        pass

    class DepthFirst(NamedTuple):
        # _storage: _Storage = _Storage.Stack()
        pass
