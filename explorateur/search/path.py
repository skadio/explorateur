from typing import List
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class Path:
    """A path with a list of moves from the initial state to the final state."""

    def __init__(self,
                 initial_state: BaseState,
                 final_state: BaseState,
                 moves: List[BaseMove],
                 is_success: bool):

        self.initial_state = initial_state
        self.final_state = final_state
        self.moves = moves
        self.is_success = is_success
