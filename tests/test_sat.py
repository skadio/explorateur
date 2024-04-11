# -*- coding: utf-8 -*-

import random
import logging
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
# from tests.SAT_Class import SATState

from typing import List, NoReturn
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

    def is_solution(self) -> bool:
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

    def get_data(self) -> dict:
        return self.var_to_val

    def set_data(self) -> NoReturn:
        """
        """
        pass

    def execute(self, move: SATMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)

        # checking the validity of the move
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

    # def objective_function(self) -> float:
    #     # this is a trivial function, not necessarily helpful to solving the problem faster
    #     total_trues = 0
    #     for var in self.var_to_val:
    #         if self.var_to_val[var] == True:
    #             total_trues += 1
    #     return float(total_trues)
    
    def objective_function(self):
        return 0.0

    # def objective_function(self) -> float:
    #     total_falses = 0
    #     for var in self.var_to_val:
    #         if self.var_to_val[var] == False:
    #             total_falses += 1
    #     return total_falses
    
    def __str__(self) -> str:
        return str(self.var_to_val)
    


class SAT_Tests(BaseTest):
    seed = random.randint(0, 100000)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def test_dfs_1(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state)
        explorer.print_path(sol_state)
        explorer.visualize_tree("tmp/test_dfs_1")
        self.assertTrue(sol_state.is_solution())

    def test_dfs_2(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state)
        explorer.visualize_tree("tmp/test_dfs_2")
        self.assertEqual(sol_state, None)

    def test_bfs_1(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)
        sol_state = explorer.search(starting_state)
        explorer.print_path(sol_state)
        explorer.visualize_tree("tmp/test_bfs_1")
        self.assertTrue(sol_state.is_solution())

    def test_bfs_2(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        clauses = [(1, -2), (-1, -2), (2, 3), (-3, 2), (1, 4)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state)
        explorer.visualize_tree("tmp/test_bfs_2")
        self.assertEqual(sol_state, None)
    
    def test_pq(self):
        explorer = Explorateur(ExplorationType.BestFirst(), self.seed)
        clauses = [(1, 2, 3), (-1, 2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state)
        explorer.print_path(sol_state)
        explorer.visualize_tree("tmp/test_pq")
        self.assertTrue(sol_state.is_solution())


# Comments
# pep-8 for ofrmatting, test_simple from class, maybe get rid of the state folder so the importbecomes explorateur.base_state
