from collections import OrderedDict
from typing import List

from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from explorateur.state.base_state import BaseState, BaseMove
from tests.test_base import BaseTest


class MyMove(BaseMove):

    def __init__(self, variable, constraint, value):
        self.variable = variable
        self.constraint = constraint
        self.value = value

    def __str__(self) -> str:
        return str(self.variable) + " " + self.constraint + " " + str(self.value)


class MyState(BaseState):

    def __init__(self, var_to_domain, is_all_solutions):
        super().__init__()
        self.var_to_domain = var_to_domain
        self.is_all_solutions = is_all_solutions
        self.var_to_val = {}
        self.unassigned_variables = list(self.var_to_domain.keys())

    def get_moves(self) -> List[MyMove]:

        # if all variables are assigned, no more moves left
        moves = list()
        if len(self.unassigned_variables) == 0:
            return moves

        # Select first unassigned variable and first value in domain
        var = self.unassigned_variables[0]
        val = self.var_to_domain[var][0]
        moves.append(MyMove(var, "==", val))
        moves.append(MyMove(var, "!=", val))
        print("USER moves [", moves[0], ",", moves[1],"]")

        return moves

    def is_terminate(self, goal_state=None) -> bool:
        # Search finishes when all variables are assigned
        if self.is_all_solutions: return False
        return len(self.unassigned_variables) == 0

    def execute(self, move: MyMove) -> bool:
        print("USER Execute:", move)
        var, constraint, val = move.variable, move.constraint, move.value

        if var == "x" and constraint == "==" and val == 1:
            return False

        if var == "z" and constraint == "==" and val == 100:
            return False

        # Propagation
        if constraint == "==":
            print("\tEQ assigns", var, "<-", val)
            self.var_to_val[var] = val
            self.var_to_domain[var] = [val]
            self.unassigned_variables.remove(var)
        elif constraint == "!=":
            print("\tNEQ removes", val, "from", var)
            self.var_to_domain[var].remove(val)
            if len(self.var_to_domain[var]) == 0:
                print("USER Execute: FAILS, empty domain var:", var)
                return False
            elif len(self.var_to_domain[var]) == 1:
                self.var_to_val[var] = self.var_to_domain[var][0]
                self.unassigned_variables.remove(var)
                print("\tNEQ fixed", var, "<-", self.var_to_val[var])

        # Successful execution
        print("USER Execute: SUCCESS")
        return True

    def __str__(self) -> str:
        text = "State ID: " + str(self._id)
        text += "\nAssignment: "
        for var, val in self.var_to_val.items():
            text += str(var) + " = " + str(val) + ", "
        text += "\nUnassigned: "
        for var in self.unassigned_variables:
            text += str(var) +","
        text += "\nDomains: "
        for var, domain in self.var_to_domain.items():
            text += str(var) + "{"
            for var in domain:
                text += str(var) + ","
            text += "} "
        return text


class SimpleTests(BaseTest):

    def test_usage_example(self):

        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState(OrderedDict([("x", [1, 2]),
                                             ("y", [10, 20]),
                                             ("z", [100, 200])]),
                                is_all_solutions=False)

        # Solve via search
        if explorer.search(initial_state,
                           goal_state=None, # Optional goal state
                           exploration_type=ExplorationType.DepthFirst(),
                           search_type=SearchType.TreeSearch(),
                           is_solution_path=True,
                           dot_file_path="data/tree_search_dfs.dot"):
            print("Solution:", explorer.solution_state)
            print("Solution Path:", *explorer.solution_path, sep="\n<-")
        else:
            print("No solution found!")

        # self.assertTrue(sol_state.is_terminate(end_state=None))