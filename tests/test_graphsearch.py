# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState

"""
Test for graph search using a simple problem where by three variables need to be assigned values which are chosen from
a predetermined set. 
"""

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

    def is_terminate(self, end_state = None) -> bool:
        """
        """
        return True
        end_assignment = {1:1 , 2:20, 3:100}
        if end_state.var_to_val == end_assignment:
            return True
        return False


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

    
    def objective_function(self):
        return 0.0
    
    def __str__(self) -> str:
        return str(self.var_to_val)
    
    def is_valid(self):
        valid = True
        for k,v in self.var_to_val.items():
            if v not in self.possible_vals[k]:
                valid = False
        return valid
    
    def make_node_label(self, iterations):
        return str(iterations)
    


class GraphSearchTest(BaseTest):
    def test_graphsearch(self):
        """
        Tests graph search by choosing an end_state where we want the search to terminate, in this case it is a specific assignment
        to the variable. 
        """
        seed = random.randint(0, 100000)
        explorer = Explorateur(ExplorationType.BreadthFirst(), seed)
        possible_vals = {1: [1,2], 2: [20,10], 3: [100,200]}

        starting_state = SimpleState(possible_vals)
        #We only want to terminate the search once this specific set of variable assignment has been reached
        end_state = SimpleState({1: [1,2], 2: [20,10], 3: [100,200]})
        end_state.var_to_val = {1: 1, 2: 20, 3: 200}
        end_state.unassigned_variables = {}
        
        sol_state = explorer.search(starting_state)
        # explorer.print_path(sol_state)
        # explorer.visualize_tree("tmp/simple_graphsearch")
        self.assertTrue(sol_state.is_terminate())

