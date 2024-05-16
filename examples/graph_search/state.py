from typing import Dict, List
from explorateur import BaseState
from move import MyMove


class MyState(BaseState):

    # Store a single copy of the problem graph
    graph = None

    # Problem specific state representation
    def __init__(self, v, problem_graph: Dict[str, Dict[str, int]] = None):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()

        # Save the problem graph, only once
        if not MyState.graph:
            MyState.graph = problem_graph

        # State is the current vertex
        self.v = v

    # Design branching decisions
    def get_moves(self) -> List[MyMove]:
        # Moves: Visit the neighbors of the current vertex
        return [MyMove(u) for u in MyState.graph[self.v].keys()]

    # Check whether a state is the solution/termination
    def is_terminate(self, goal_state: 'MyState') -> bool:
        if goal_state:
            return self.v == goal_state.v

    # Execute the move on the state, return success flag
    def execute(self, move: MyMove) -> bool:
        # Move to the next vertex
        self.v = move.u
        return True

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        return str(self.v)

    # This is required for graph search to check contains on already visited decisions
    def __eq__(self, other):
        if isinstance(other, MyState):
            return self.v == other.v
        return False

    # This is required for graph search when adding closed decision into hashset
    def __hash__(self):
        return hash(self.v)


