# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class SimpleMove(BaseMove):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def get_dot_edge_label(self) -> str:
        return str(self.variable) + "->" + str(self.value)

    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"


class SimpleState(BaseState):

    def __init__(self, var_to_domain):
        self.var_to_domain = var_to_domain

        self.var_to_val = {}
        self.unassigned_vars = set(self.var_to_domain.keys())

    def get_moves(self) -> List[SimpleMove]:
        moves = list()
        for var in self.unassigned_vars:
            for val in self.var_to_domain[var]:
                moves.append(SimpleMove(var, val))
        return moves

    def is_terminate(self, end_state=None) -> bool:
        if len(self.unassigned_vars) > 0:
            return False
        return True

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_vars.remove(move.variable)
        return True

    def is_valid(self) -> bool:
        valid = True
        for k, v in self.var_to_val.items():
            if v not in self.var_to_domain[k]:
                valid = False
        return valid

    def get_dot_node_label(self, curr_iter_count: int):
        return str(curr_iter_count)

    def __str__(self) -> str:
        return str(self.var_to_val)


class SimpleTests(BaseTest):
    seed = random.randint(0, 100000)

    def test_dfs(self):
        explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
        possible_vals = {1: [1, 2], 2: [20, 10], 3: [100, 200]}

        starting_state = SimpleState(possible_vals)

        sol_state = explorer.search(starting_state)
        path = explorer._get_solution_path()
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
        end_state.unassigned_vars = {}

        sol_state = explorer.search(starting_state)
        self.assertTrue(sol_state.is_terminate(end_state=None))
