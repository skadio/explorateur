from typing import List, Optional
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from explorateur.state.base_state_objective import BaseStateObjective
from explorateur.state.base_dot_labeler import BaseDotLabeler
from explorateur.search.transition import Transition
from pydot import Node


class _State(BaseState, BaseStateObjective, BaseDotLabeler):
    """
    An internal class to wrap user BaseState.
    The wrapper extends BaseState with transition, get_transition() and set_transition().
    This is used by explorateur.search() as a wrapper of the user provided initial state.
    Other than transition, calls equivalent functions in BaseState.
    """

    def __init__(self, base_state: BaseState):
        self.base = base_state

        # Transition is the main difference between BaseState and State_
        self.transition: Optional[Transition] = None

        # If dot, then store the dot.Node() and its label at the time of this _state
        self.dot_node: Optional[Node] = None
        self.dot_node_label = None

    def execute(self, move: BaseMove) -> bool:
        return self.base.execute(move)

    def get_moves(self) -> List[BaseMove]:
        return self.base.get_moves()

    def is_terminate(self, end_state: Optional[BaseState] = None):
        return self.base.is_terminate(end_state)

    # Implement BaseStateObjective
    def get_objective(self, state: BaseState) -> float:
        return self.base.get_objective(state)

    # Implement BaseDotLabeler
    def get_dot_label(self, num_moves: int, depth: int) -> str:
        return self.base.get_dot_label(num_moves, depth)

    def __str__(self) -> str:
        return str(self.base)
