from typing import Dict, List
from explorateur import BaseState
from move import MyMove


class MyState(BaseState):

    # Problem specific state representation
    def __init__(self, var_to_domain):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()

        # State is variable domains, value assigments, and unassigned vars
        self.var_to_domain: Dict[str, List[int]] = var_to_domain
        self.var_to_val: Dict[str, int] = {}
        self.unassigned: List[str] = list(self.var_to_domain.keys())

    # Design branching decisions
    def get_moves(self) -> List[MyMove]:
        # If all vars are assigned, no more moves
        if len(self.unassigned) == 0: return list()

        # Select first unassigned variable and first value in domain
        var = self.unassigned[0]
        val = self.var_to_domain[var][0]

        # Binary branching
        return [MyMove(var, "==", val), MyMove(var, "!=", val)]

    # Check whether a state is the solution/termination
    def is_terminate(self, goal_state=None) -> bool:
        # For demo purposes, no termination, search exhaustively
        return False

    # Execute the move on the state, return success flag
    def execute(self, move: MyMove) -> bool:
        var, constraint, val = move.var, move.constraint, move.val

        # Propagate EQ and NEQ constraints
        if constraint == "==":
            self.var_to_val[var] = val
            self.var_to_domain[var] = [val]
            self.unassigned.remove(var)
        elif constraint == "!=":
            self.var_to_domain[var].remove(val)
            if len(self.var_to_domain[var]) == 0:
                return False
            elif len(self.var_to_domain[var]) == 1:
                self.var_to_val[var] = self.var_to_domain[var][0]
                self.unassigned.remove(var)
        return True

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        text = "State ID: " + str(self._id) + "\n"
        text += "Assignment: " + str(self.var_to_val) + "\n"
        text += "Domains: " + str(self.var_to_domain)
        return text

