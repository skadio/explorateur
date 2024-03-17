# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur, SearchType
from SAT_Classes.SAT_state import SATState


class ExampleTest(BaseTest):

    # def main():
    #     # dfs = ExplorationType.DepthFirst(1)

    def test_dfs_example(self):
        seed = random.randint(0,100000)
        explorer = Explorateur(SearchType.DepthFirst, seed)
        clauses = [(1,2,3), (-1,2)]
        vars = set()
        for c in clauses:
            for v in c:
                vars.add(v)
        starting_state = SATState({}, clauses, vars)
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertEqual(True, False)

    # def test_bfs_example(self):
    #     self.assertEqual(True, False)