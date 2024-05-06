# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from typing import List
from explorateur.state.storage.queue import Queue
from explorateur.state.storage.stack import Stack
from explorateur.state.storage.priority_queue import PriorityQueue
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class SimpleMove(BaseMove):

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass


class SimpleState(BaseState):

    def __init__(self, val):
        self.val = val

    def generate_vars(self):
        pass

    def get_moves(self) -> List[SimpleMove]:
        pass

    def is_terminate(self, end_state=None) -> bool:
        pass

    def execute(self, move: SimpleMove) -> bool:
        pass

    def __str__(self) -> str:
        pass

    def is_valid(self) -> bool:
        pass

    def make_node_label(self, iterations: int) -> str:
        pass

    def objective_function(self):
        if self.val == 2:
            return 1
        else:
            return 10


class StorageTests(BaseTest):
    seed = random.randint(0, 100000)

    # can't test for contains() because it takes in a _BaseState
    def test_queue(self):
        q = Queue()
        b1 = SimpleState(1)
        b2 = SimpleState(2)
        q.insert(b1)
        self.assertTrue(q.contains(b1))
        q.insert(b2)
        res = q.remove()
        self.assertEqual(b1, res)
        self.assertEqual(q.get_size(), 1)
        q.remove()
        self.assertTrue(q.is_empty())

    def test_stack(self):
        s = Stack()
        b1 = SimpleState(1)
        b2 = SimpleState(2)
        s.insert(b1)
        self.assertTrue(s.contains(b1))
        s.insert(b2)
        res = s.remove()
        self.assertEqual(b2, res)
        self.assertEqual(s.get_size(), 1)
        self.assertFalse(s.is_empty())

    def test_priority_queue(self):
        pq = PriorityQueue()
        b1 = SimpleState(1)
        b2 = SimpleState(2)
        pq.insert(b1)
        pq.insert(b2)
        self.assertEqual(pq.get_size(), 2)
        res = pq.remove()
        self.assertEqual(res, b2)
        self.assertFalse(pq.is_empty())
