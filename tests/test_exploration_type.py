# -*- coding: utf-8 -*-

import random
import logging
import numpy as np
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
# from tests.SAT_Class import SATState

from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState

"""Uses a SAT problem to run and test breath-first, depth-first and best-first search. We implement the functions 
needed for BaseMove and BaseState to function. """


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
        '''
        This function is not part of the ones the user has to implement for BaseState, it's a helper.
        '''
        variables = set()
        for c in clauses:
            for v in c:
                variables.add(abs(v))
        return variables

    def get_moves(self) -> List[SATMove]:
        moves_list = []
        for var in self.unassigned_variables:
            moves_list.append(SATMove(var, True))
            moves_list.append(SATMove(var, False))

        return moves_list

    def is_terminate(self, end_state=None) -> bool:
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

    def objective_function(self) -> float:
        res = np.random.uniform(2.0, 10.0)
        if 2 in self.var_to_val.keys():
            if self.var_to_val[2] is False and self.flag is False:
                self.flag = True
                return 0.5
        return res

    def __str__(self) -> str:
        return str(self.var_to_val)

    def make_node_label(self, iterations):
        return str(iterations)


class ExplorationTypeTests(BaseTest):
    seed = random.randint(0, 100000)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def test_dfs_1(self):
        """
        This is a Depth-First search for a satisfiable / solveable instance and writes the tree to "temp/test_dfs_1"
        """
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state, file_path="tmp/test_dfs_1")
        self.assertTrue(sol_state.is_terminate())

    def test_dfs_2(self):
        """
        This is a Depth-First Search search over an UNSAT problem, that is to say there should be no solution state.
        The tree is written to "temp/test_dfs_2" and all the leaf nodes are red with no green nodes since there is no
        solution state.
        """
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state, file_path="tmp/test_dfs_2")
        self.assertEqual(sol_state, None)

    def test_bfs_1(self):
        """
        This is a Breadth-First search for a satisfiable / solveable instance same as the first one with the tree
        written to "tmp/test_bfs_1".
        """
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state, file_path="tmp/test_bfs_1")
        # explorer.print_path(sol_state)
        self.assertTrue(sol_state.is_terminate())

    def test_bfs_2(self):
        """
        This is a Breadth-First search for a unsatisfiable instance and writes the tree to "tmp/test_bfs_2"
        """
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state, file_path="tmp/test_bfs_2")
        self.assertEqual(sol_state, None)

    def test_best_first(self):
        """
        This is a Best-First search done with the objective function defined above. Since we let the first instance
        of 2 being false have the lowest value for the priority queue we expect this to be the first element explored
        (seen in "tmp/test_pq")
        """
        explorer = Explorateur(ExplorationType.BestFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state, file_path="tmp/test_pq")
        # explorer.visualize_tree("tmp/test_pq.dot")
        self.assertIsNone(sol_state)
