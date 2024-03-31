# -*- coding: utf-8 -*-

import random
from test_base import BaseTest
from explorateur.explorateur import Explorateur, ExplorationType
# from tests.SAT_Class import SATState

from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState

class SATMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable  #variable
        self.value = variable_assignment

class SATState(BaseState):

    def __init__(self, clauses):
        self.variable_assignments = {}  #varToVal (naming convention)
        self.clauses = clauses
        self.unassigned_variables = self.generate_vars(self.clauses) 

    def generate_vars(self, clauses):
        vars = set()
        for c in clauses:
            for v in c:
                vars.add(abs(v))
        return vars
    
    def get_valid_moves(self) -> List[SATMove]:
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
            isSatisfied = False
            for literal in clause:
                if abs(literal) not in self.variable_assignments.keys():
                    continue
                if literal > 0 and self.variable_assignments[abs(literal)]:
                    isSatisfied = True
                    break
                elif literal < 0 and not self.variable_assignments[abs(literal)]:
                    isSatisfied = True
                    break
            if not isSatisfied:
                return False
        return True

    def get_data(self) -> dict:
        return self.variable_assignments

    def set_data(self) -> NoReturn:
        """
        """
        pass        

    def execute(self, move: SATMove) -> bool:
        self.variable_assignments[move.variable] = move.variable_assignment  #don't need the absolute 
        self.unassigned_variables.remove(move.variable)
        
        #checking the validity of the move
        for clause in self.clauses:
            is_unsatisfiable = True
            for literal in clause:
                if abs(literal) not in self.variable_assignments.keys():
                    is_unsatisfiable  = False
                    break
                elif literal > 0 and self.variable_assignments[abs(literal)]:
                    is_unsatisfiable  = False
                    break
                elif literal < 0 and not self.variable_assignments[abs(literal)]:
                    is_unsatisfiable  = False
                    break
            if is_unsatisfiable:
                return False
        return True



class SAT_Tests(BaseTest):
    seed = random.randint(0,100000)

    
    def test_dfs_1(self):
        explorer = Explorateur(ExplorationType.DepthFirst, self.seed)
        clauses = [(1,2,3), (-1,2)]

        starting_state = SATState(clauses)

        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertNotEqual(sol_state, None)
    
    def test_dfs_2(self):
        explorer = Explorateur(ExplorationType.DepthFirst, self.seed)
        clauses = [(1, -2, 0), (-1,-2,0), (2,3,0), (-3,2,0), (1,4,0)]

        #could move the following setup into SATState()
        starting_state = SATState(clauses)

        
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertEqual(sol_state, None)

    def test_bfs_2(self):
        explorer = Explorateur(ExplorationType.BreadthFirst, self.seed)
        clauses = [(1, -2, 0), (-1,-2,0), (2,3,0), (-3,2,0), (1,4,0)]

        starting_state = SATState(clauses)
        
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertEqual(sol_state, None)



# Comments
# pep-8 for ofrmatting, test_simple from class, maybe get rid of the state folder so the importbecomes explorateur.base_state
        