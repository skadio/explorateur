# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
# from tests.SAT_Class import SATState

from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class SimpleMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.value = variable_assignment
    
    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"
    


class SimpleState(BaseState):

    def __init__(self, possible_vals):
        self.var_to_val = {}
        self.possible_vals = possible_vals
        self.unassigned_variables = self.generate_vars(self.possible_vals)

    def generate_vars(self, clauses):
        variables = set()
        for v in self.possible_vals.keys():
            variables.add(v)
        return variables

    def get_moves(self) -> List[SimpleMove]:
        """
        """
        moves_list = []
        for var in self.unassigned_variables:
            for val in self.possible_vals[var]:
                moves_list.append(SimpleMove(var, val))
        return moves_list

    def is_solution(self) -> bool:
        """
        """
        if len(self.unassigned_variables) > 0:
            return False
        return True

    def get_data(self) -> dict:
        return self.var_to_val

    def set_data(self) -> NoReturn:
        """
        """
        pass

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)
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
    


class Simple_Tests(BaseTest):
    seed = random.randint(0, 100000)

    def test_dfs(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        possible_vals = {1: [1,2], 2: [20,10], 3: [100,200]}

        starting_state = SimpleState(possible_vals)

        sol_state = explorer.search(starting_state)
        explorer.print_path(sol_state)
        explorer.visualize_tree("tmp/simple_dfs")
        self.assertTrue(sol_state.is_solution())

    def test_bfs(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        possible_vals = {1: [1,2], 2: [20,10], 3: [100,200]}

        starting_state = SimpleState(possible_vals)

        sol_state = explorer.search(starting_state)
        explorer.print_path(sol_state)
        explorer.visualize_tree("tmp/simple_dfs")
        self.assertTrue(sol_state.is_solution())

    # def test_pq(self):
    #     explorer = Explorateur(ExplorationType.BestFirst(), self.seed)
    #     clauses = [(1, 2, 3), (-1, 2)]

    #     starting_state = SATState(clauses)

    #     sol_state = explorer.search(starting_state)
    #     explorer.print_path(sol_state)
    #     explorer.visualize_tree("tmp/test_pq")
    #     self.assertTrue(sol_state.is_solution())


# Comments
# pep-8 for ofrmatting, test_simple from class, maybe get rid of the state folder so the importbecomes explorateur.base_state
