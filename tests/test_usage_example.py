import logging
from collections import OrderedDict
from typing import List

from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
from explorateur.state.base_dot_labeler import BaseDotLabeler
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from tests.test_base import BaseTest


class MyMove(BaseMove, BaseDotLabeler):

    def __init__(self, variable, constraint, value):
        self.variable = variable
        self.constraint = constraint
        self.value = value

    def get_dot_label(self, num_moves: int, depth: int) -> str:
        return "[M" + str(num_moves) + "-D" + str(depth) + "]\n" + str(self)

    def __str__(self) -> str:
        return str(self.variable) + " " + self.constraint + " " + str(self.value)


class MyState(BaseState, BaseDotLabeler):

    def __init__(self, var_to_domain):
        self.var_to_domain = var_to_domain
        self.var_to_val = {}
        self.unassigned_variables = list(self.var_to_domain.keys())

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
        logging.info("USER moves [%s, %s]", moves[0], moves[1])

        return moves

    def is_terminate(self, end_state=None) -> bool:
        # Search finishes when all variables are assigned
        # return len(self.unassigned_variables) == 0
        return False

    def execute(self, move: MyMove) -> bool:
        logging.info("USER Execute: %s", move)
        var, val, constraint = move.variable, move.value, move.constraint

        # Propagation
        if constraint == "==":
            logging.info("\tEQ assigns var-val: %s-%s", var, val)
            self.var_to_val[var] = val
            self.var_to_domain[var] = [val]
            self.unassigned_variables.remove(var)
        elif constraint == "!=":
            logging.info("\tNEQ removes var-val: %s-%s", var, val)
            self.var_to_domain[var].remove(val)
            if len(self.var_to_domain[var]) == 0:
                logging.info("USER Execute: FAILS, empty domain var: %s", var)
                return False
            elif len(self.var_to_domain[var]) == 1:
                self.var_to_val[var] = self.var_to_domain[var][0]
                self.unassigned_variables.remove(var)
                logging.info("\tNEQ fixed var-val: %s-%s", var, self.var_to_val[var])

        # Successful execution
        logging.info("USER Execute: SUCCESS")
        return True

    def get_dot_label(self, num_moves: int, depth: int):

        return "[M" + str(num_moves) + "-D" + str(depth) + "]\n" + " ".join(self.var_to_val)

    def __str__(self) -> str:
        return "Assignment: " + str(self.var_to_val) + "\n" + \
                "Unassigned: " + str(self.unassigned_variables) + "\n" +\
                "Variables: " + str(self.var_to_domain)


class SimpleTests(BaseTest):

    def test_usage_example(self):

        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        explorer = Explorateur()

        # Initial state with variables and possible domain values
        initial_state = MyState(OrderedDict([("x", [1, 2]),
                                             ("y", [10, 20]),
                                             ("z", [100, 200])]))

        # Find a solution via search
        solution_state = explorer.search(initial_state, exploration_type=ExplorationType.BreadthFirst(),
                                         dot_file_path="example.dot")
        print("Solution: ", solution_state)

        solution_path = explorer.get_path()
        print("Path: ", solution_path)

        # self.assertTrue(sol_state.is_terminate(end_state=None))
