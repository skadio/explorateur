import unittest
from typing import Dict, List
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType


class EmptyMove(BaseMove):

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass


class EmptyState(BaseState):

    def __init__(self):
        super().__init__()

    def get_moves(self):
        pass

    def is_terminate(self, goal_state):
        pass

    def execute(self, move):
        pass

    def __str__(self):
        pass


class MyMove(BaseMove):

    # Define move object
    def __init__(self, var, constraint, val):
        self.var: str = var
        self.constraint: str = constraint
        self.val: int = val

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return str(self.var) + " " + self.constraint + " " + str(self.val)

    # This is required for graph search to check contains on already visited decisions
    def __eq__(self, other):
        if isinstance(other, MyMove):
            return self.var == other.var and \
                self.constraint == other.constraint and \
                self.val == other.val
        return False

    # This is required for graph search when adding closed decision into hashset
    def __hash__(self):
        return hash((self.var, self.constraint, self.val))


class MyState(BaseState):

    # Problem specific state representation
    def __init__(self, var_to_domain, is_exhaustive_search=True, fake_fails=None):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()

        if fake_fails is None:
            fake_fails = []
        self.var_to_domain: Dict[str, List[int]] = var_to_domain
        self.var_to_val: Dict[str, int] = {}
        self.unassigned: List[str] = list(self.var_to_domain.keys())
        self.is_exhaustive_search = is_exhaustive_search
        self.fake_fails = fake_fails

    # Design branching decisions
    def get_moves(self) -> List[MyMove]:
        # If all vars are assigned, no more moves
        if len(self.unassigned) == 0: return list()

        # Select first unassigned variable and first value in domain
        var = self.unassigned[0]
        val = self.var_to_domain[var][0]

        # Binary branching
        moves = [MyMove(var, "==", val), MyMove(var, "!=", val)]
        print("USER moves [", moves[0], ",", moves[1], "]")
        return moves

    # Check whether a state is the solution/termination
    def is_terminate(self, goal_state=None) -> bool:
        # For demo purposes, no termination, search exhaustively
        if self.is_exhaustive_search: return False
        return len(self.unassigned) == 0

    # Execute the move on the state, return success flag
    def execute(self, move: MyMove) -> bool:
        print("USER Execute:", move)
        var, constraint, val = move.var, move.constraint, move.val

        if move in self.fake_fails:
            print("\t Fake fail [", move, "]")
            return False

        # Propagate EQ and NEQ constraints
        if constraint == "==":
            print("\tEQ assigns", var, "<-", val)
            self.var_to_val[var] = val
            self.var_to_domain[var] = [val]
            self.unassigned.remove(var)
        elif constraint == "!=":
            print("\tNEQ removes", val, "from", var)
            self.var_to_domain[var].remove(val)
            if len(self.var_to_domain[var]) == 0:
                print("USER Execute: FAILS, empty domain var:", var)
                return False
            elif len(self.var_to_domain[var]) == 1:
                self.var_to_val[var] = self.var_to_domain[var][0]
                self.unassigned.remove(var)
                print("\tNEQ fixed", var, "<-", self.var_to_val[var])

        # Successful execution
        print("USER Execute: SUCCESS")
        return True

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        text = "State ID: " + str(self._id) + "\n"
        text += "Assignment: " + str(self.var_to_val) + "\n"
        text += "Domains: " + str(self.var_to_domain)
        return text

    # This is required for graph search to check contains on already visited decisions
    def __eq__(self, other):
        if isinstance(other, MyState):
            return self.unassigned == other.unassigned and \
                self.var_to_val == other.var_to_val and \
                self.var_to_domain == other.var_to_domain
        return False

    # This is required for graph search when adding closed decision into hashset
    def __hash__(self):
        return hash((tuple(self.unassigned), tuple(self.var_to_val), tuple(self.var_to_domain)))


class BaseTest(unittest.TestCase):

    def search(self,
               explorer,
               initial_state, goal_state,
               exploration_type, search_type,
               is_solution_path,
               max_depth, max_moves, max_runtime, dot_filename, is_verbose):

        # Search for solutions
        if explorer.search(initial_state,
                           goal_state=goal_state,  # Optional goal state
                           exploration_type=exploration_type,
                           search_type=search_type,
                           is_solution_path=is_solution_path,
                           max_depth=max_depth,
                           max_moves=max_moves,
                           max_runtime=max_runtime,
                           dot_filename=dot_filename):

            if is_verbose:
                print("Solution:", explorer.solution_state)
                print("Solution Path:", *explorer.solution_path, sep="\n<-")
        else:
            if is_verbose:
                print("No solution found!")

        if is_verbose:
            # Search statistics
            print("Total Decisions:", explorer.num_decisions)
            print("Total Failures:", explorer.num_failed_decisions)
            print("Total Time:", round(explorer.total_time, 3))

    def assertListAlmostEqual(self, list1, list2):
        """
        Asserts that floating values in the given lists (almost) equals to each other
        """
        if not isinstance(list1, list):
            list1 = list(list1)

        if not isinstance(list2, list):
            list2 = list(list2)

        self.assertEqual(len(list1), len(list2))

        for index, val in enumerate(list1):
            self.assertAlmostEqual(val, list2[index])
