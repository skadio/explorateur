# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List
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
        self.unassigned_variables = self.generate_vars()

    def generate_vars(self):
        variables = set()
        for v in self.possible_vals.keys():
            variables.add(v)
        return variables

    def get_moves(self) -> List[SimpleMove]:
        moves_list = []
        for var in self.unassigned_variables:
            for val in self.possible_vals[var]:
                moves_list.append(SimpleMove(var, val))
        return moves_list

    def is_terminate(self, end_state=None) -> bool:
        if len(self.unassigned_variables) > 0:
            return False
        return True

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)
        return True

    def is_valid(self) -> bool:
        valid = True
        for k, v in self.var_to_val.items():
            if v not in self.possible_vals[k]:
                valid = False
        return valid

    def make_node_label(self, iterations: int):
        return str(iterations)

    def __str__(self) -> str:
        return str(self.var_to_val)


class SimpleTests(BaseTest):
    seed = random.randint(0, 100000)

    def test_dfs(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        possible_vals = {1: [1, 2], 2: [20, 10], 3: [100, 200]}

        starting_state = SimpleState(possible_vals)

        sol_state = explorer.search(starting_state)
        path = explorer.get_path()
        self.assertTrue(sol_state.is_terminate(end_state=None))

    def test_bfs(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        possible_vals = {1: [1, 2], 2: [20, 10], 3: [100, 200]}

        starting_state = SimpleState(possible_vals)

        sol_state = explorer.search(starting_state)
        # explorer.print_path(sol_state)
        self.assertTrue(sol_state.is_terminate(end_state=None))

    def test_graph_search(self):
        explorer = Explorateur(ExplorationType.BreadthFirst(), self.seed)
        possible_vals = {1: [1, 2], 2: [20, 10], 3: [100, 200]}

        starting_state = SimpleState(possible_vals)
        end_state = SimpleState({1: [1, 2], 2: [20, 10], 3: [100, 200]})
        end_state.var_to_val = {1: 1, 2: 20, 3: 200}
        end_state.unassigned_variables = {}

        sol_state = explorer.search(starting_state)
        self.assertTrue(sol_state.is_terminate(end_state=None))
