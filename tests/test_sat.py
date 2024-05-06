# -*- coding: utf-8 -*-

import random
import logging
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class SATMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.value = variable_assignment

    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"


class SATState(BaseState):

    def __init__(self, clauses):
        self.var_to_val = {}
        self.clauses = clauses
        self.unassigned_variables = self.generate_vars(self.clauses)
        self.flag = False

    def generate_vars(self, clauses):
        variables = set()
        for c in clauses:
            for v in c:
                variables.add(abs(v))
        return variables

    def get_moves(self) -> List[SATMove]:
        """
        """
        moves_list = []
        for var in self.unassigned_variables:
            moves_list.append(SATMove(var, True))
            moves_list.append(SATMove(var, False))

        return moves_list

    def is_terminate(self, end_state=None) -> bool:
        """
        """
        for clause in self.clauses:
            is_satisfied = False
            for literal in clause:
                if abs(literal) not in self.var_to_val:
                    continue
                if literal > 0 and self.var_to_val[abs(literal)]:
                    is_satisfied = True
                    break
                elif literal < 0 and not self.var_to_val[abs(literal)]:
                    is_satisfied = True
                    break
            if not is_satisfied:
                return False
        return True

    def execute(self, move: SATMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)

        return self.is_valid()

    def is_valid(self):
        for clause in self.clauses:
            is_unsatisfiable = True
            for literal in clause:
                if abs(literal) not in self.var_to_val.keys():
                    is_unsatisfiable = False
                    break
                elif literal > 0 and self.var_to_val[abs(literal)]:
                    is_unsatisfiable = False
                    break
                elif literal < 0 and not self.var_to_val[abs(literal)]:
                    is_unsatisfiable = False
                    break
            if is_unsatisfiable:
                return False
        return True

    def __str__(self) -> str:
        return str(self.var_to_val)

    def make_node_label(self, iterations) -> str:
        return str(iterations)


class SATTests(BaseTest):
    seed = random.randint(0, 100000)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def test_dfs_1(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state, file_path="tmp/test_dfs_1.dot")
        self.assertTrue(sol_state.is_terminate(end_state=None))

    def test_dfs_2(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state, file_path="tmp/test_dfs_2.dot")
        self.assertEqual(sol_state, None)

    def test_bfs_1(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state, file_path="tmp/test_bfs_1.dot")
        self.assertTrue(sol_state.is_terminate(end_state=None))

    def test_bfs_2(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state, file_path="tmp/test_bfs_2.dot")
        self.assertEqual(sol_state, None)

    def test_iterations(self):
        # this one is supposed to have a solution but we are cutting it of early
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state, max_iterations=2)
        self.assertEqual(sol_state, None)
