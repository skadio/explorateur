from tests.test_base import BaseTest, EmptyState
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.hash import HashSet
from explorateur.state.storage.priority_queue import PriorityQueue
from tests.test_base import BaseTest, MyState, MyMove


class StorageState(EmptyState):

    def __init__(self, val):
        super().__init__()
        self.val = val

    def get_objective(self):
        if self.val == 2:
            return 1
        else:
            return 10


class StorageTest(BaseTest):

    # can't test for contains() because it takes in a _BaseState
    def test_queue(self):
        q = Queue()
        b1 = StorageState(1)
        b2 = StorageState(2)
        q.insert(b1)
        self.assertTrue(q.contains(b1))
        q.insert(b2)
        res = q.remove()
        self.assertEqual(b1, res)
        self.assertEqual(q.size(), 1)
        q.remove()
        self.assertTrue(q.is_empty())

    def test_stack(self):
        s = Stack()
        b1 = StorageState(1)
        b2 = StorageState(2)
        s.insert(b1)
        self.assertTrue(s.contains(b1))
        s.insert(b2)
        res = s.remove()
        self.assertEqual(b2, res)
        self.assertEqual(s.size(), 1)
        self.assertFalse(s.is_empty())

    def test_hash(self):
        state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})
        move = MyMove("x", "==", 1)

        h = HashSet()
        self.assertTrue(h.is_empty())

        h.insert(state)
        self.assertTrue(h.contains(state))
        self.assertEqual(h.size(), 1)
        self.assertFalse(h.is_empty())

        d2 = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})
        self.assertEqual(h.contains(d2), d2)

        h.insert(d2)
        self.assertEqual(h.size(), 1)

        x = h.remove()
        self.assertEqual(x, d2)
        self.assertIsNone(h.contains(state))
        self.assertTrue(h.is_empty())
        self.assertEqual(h.size(), 0)

        h.insert(state)
        self.assertEqual(h.size(), 1)


    def test_priority_queue(self):
        # TODO
        pass
        # pq = PriorityQueue()
        # b1 = StorageState(1)
        # b2 = StorageState(2)
        # pq.insert(b1)
        # pq.insert(b2)
        # self.assertEqual(pq.size(), 2)
        # res = pq.remove()
        # self.assertEqual(res, b2)
        # self.assertFalse(pq.is_empty())
