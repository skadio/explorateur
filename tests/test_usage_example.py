import logging
from collections import OrderedDict
from typing import List

from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from tests.test_base import BaseTest


class MyMove(BaseMove):

    def __init__(self, variable, constraint, value):
        self.variable = variable
        self.constraint = constraint
        self.value = value

    def get_dot_label(self) -> str:
        return str(self.variable) + " " + self.constraint + " " + str(self.value)

    def __str__(self) -> str:
        return str(self.variable) + " " + self.constraint + " " + str(self.value)


class MyState(BaseState):

    def __init__(self, var_to_domain, is_all_solutions, logger):
        self.var_to_domain = var_to_domain
        self.is_all_solutions = is_all_solutions
        self.var_to_val = {}
        self.unassigned_variables = list(self.var_to_domain.keys())
        self.logger = logger

    def get_moves(self) -> List[MyMove]:

        # No more moves if all variables are assigned
        moves = list()
        if len(self.unassigned_variables) == 0:
            return moves

        # Select first unassigned variable and first value in domain
        var = self.unassigned_variables[0]
        val = self.var_to_domain[var][0]
        moves.append(MyMove(var, "==", val))
        moves.append(MyMove(var, "!=", val))
        self.logger.info("USER moves [%s, %s]", moves[0], moves[1])

        return moves

    def is_terminate(self, end_state=None) -> bool:
        # Search finishes when all variables are assigned
        if self.is_all_solutions: return False
        return len(self.unassigned_variables) == 0

    def execute(self, move: MyMove) -> bool:
        self.logger.info("USER Execute: %s", move)
        var, constraint, val = move.variable, move.constraint, move.value

        if var == "x" and constraint == "==" and val == 1:
            return False

        if var == "z" and constraint == "==" and val == 100:
            return False

        # Propagation
        if constraint == "==":
            self.logger.info("\tEQ assigns var-val: %s-%s", var, val)
            self.var_to_val[var] = val
            self.var_to_domain[var] = [val]
            self.unassigned_variables.remove(var)
        elif constraint == "!=":
            self.logger.info("\tNEQ removes var-val: %s-%s", var, val)
            self.var_to_domain[var].remove(val)
            if len(self.var_to_domain[var]) == 0:
                self.logger.info("USER Execute: FAILS, empty domain var: %s", var)
                return False
            elif len(self.var_to_domain[var]) == 1:
                self.var_to_val[var] = self.var_to_domain[var][0]
                self.unassigned_variables.remove(var)
                self.logger.info("\tNEQ fixed var-val: %s-%s", var, self.var_to_val[var])

        # Successful execution
        self.logger.info("USER Execute: SUCCESS")
        return True

    def get_dot_label(self):
        label = "STATE\n"
        for var, val in self.var_to_val.items():
            label += str(var) + " = " + str(val) + "\n"
        return label

    def __str__(self) -> str:
        return "Assignment: " + str(self.var_to_val) + "\n" + \
                "Unassigned: " + str(self.unassigned_variables) + "\n" +\
                "Variables: " + str(self.var_to_domain)


class SimpleTests(BaseTest):

    def test_usage_example(self):

        # logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        # Explorateur
        explorer = Explorateur(logging.DEBUG)

        # Initial state
        initial_state = MyState(OrderedDict([("x", [1, 2]),
                                             ("y", [10, 20]),
                                             ("z", [100, 200])]),
                                is_all_solutions=False,
                                logger=explorer.logger)

        # Solve via search
        solution_path = explorer.search(initial_state,
                                        exploration_type=ExplorationType.DepthFirst(),
                                        search_type=SearchType.TreeSearch(),
                                        is_solution_path=True,
                                        dot_file_path="example.dot")
        # end = time.perf_counter()
        # Solution
        if solution_path:
            solution_state = solution_path[0]
            print("Solution:\n", solution_state)
            print("Solution Path:", *solution_path, sep="\n")
        # self.assertTrue(sol_state.is_terminate(end_state=None))
