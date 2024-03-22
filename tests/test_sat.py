# -*- coding: utf-8 -*-

import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur, SearchType
from tests.SAT_Class import SATState


def generate_vars(clauses):
        vars = set()
        for c in clauses:
            for v in c:
                vars.add(abs(v))
        return vars


class SAT_Tests(BaseTest):
    seed = random.randint(0,100000)

    
    def test_dfs_1(self):
        explorer = Explorateur(SearchType.DepthFirst, self.seed)
        clauses = [(1,2,3), (-1,2)]

        starting_state = SATState()
        starting_state.clauses = clauses
        starting_state.unassigned_variables = generate_vars(clauses)
        
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertNotEqual(sol_state, None)
    
    def test_dfs_2(self):
        explorer = Explorateur(SearchType.DepthFirst, self.seed)
        clauses = [(1, -2, 0), (-1,-2,0), (2,3,0), (-3,2,0), (1,4,0)]

        #could move the following setup into SATState()
        starting_state = SATState()
        starting_state.clauses = clauses
        starting_state.unassigned_variables = generate_vars(clauses)

        
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertEqual(sol_state, None)

    def test_bfs_2(self):
        explorer = Explorateur(SearchType.BreadthFirst, self.seed)
        clauses = [(1, -2, 0), (-1,-2,0), (2,3,0), (-3,2,0), (1,4,0)]

        starting_state = SATState()
        starting_state.clauses = clauses
        starting_state.unassigned_variables = generate_vars(clauses)

        
        sol_state = explorer.search(starting_state)
        print(sol_state)
        self.assertEqual(sol_state, None)



# Comments
# pep-8 for ofrmatting, test_simple from class
        