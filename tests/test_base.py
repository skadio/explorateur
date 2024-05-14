import unittest
from explorateur.state.base_state import BaseState, BaseMove


class EmptyMove(BaseMove):

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass


class EmptyState(BaseState):

    def __init__(self):
        super().__init__()

    def get_moves(self):
        pass

    def is_terminate(self, goal_state):
        pass

    def execute(self, move):
        pass

    def __str__(self):
        pass


class BaseTest(unittest.TestCase):

    def assertListAlmostEqual(self, list1, list2):
        """
        Asserts that floating values in the given lists (almost) equals to each other
        """
        if not isinstance(list1, list):
            list1 = list(list1)

        if not isinstance(list2, list):
            list2 = list(list2)

        self.assertEqual(len(list1), len(list2))

        for index, val in enumerate(list1):
            self.assertAlmostEqual(val, list2[index])
