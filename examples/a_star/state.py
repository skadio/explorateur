from typing import Dict, List
from explorateur import BaseState
from move import MyMove


class MyState(BaseState):

    # Store a single copy of the problem graph
    graph = None
    cost_forward = None

    # Problem specific state representation
    def __init__(self, v, problem_graph: Dict[str, Dict[str, int]] = None, node_to_heuristic: Dict[str, int] = None):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()

        # Save the problem input, only once
        if not MyState.graph:
            MyState.graph = problem_graph
            MyState.cost_forward = node_to_heuristic

        # State is the current vertex
        self.v = v
        self.cost_backward = 0

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
        # Add cost travelling v -> u
        self.cost_backward += self.graph[self.v][move.u]
        # Move to the next vertex
        self.v = move.u
        return True

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        return (str(self.id) + "\n" + str(self.v) +
                "\nBackward Cost " + str(self.cost_backward) +
                "\nForward Cost " + str(self.cost_forward[self.v]) +
                "\nTotal Cost " + str(self.cost_backward + self.cost_forward[self.v]))

    # This is required for graph search to check contains on already visited states
    def __eq__(self, other):
        if isinstance(other, MyState):
            return self.v == other.v
        return False

    # This is required for graph search when adding closed states into hashset
    def __hash__(self):
        return hash(self.v)

    def get_objective(self) -> float:
        """
        Return the objective value of the state.
        A* search: f(n) = g(n) + h(n), where
        - g(n) is the backward cost based on the path so far
        - h(n) is the forward heuristic cost

        Returns:
            float: The objective function value for the state.
        """
        return self.cost_backward + self.cost_forward[self.v]


