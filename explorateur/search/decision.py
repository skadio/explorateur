from typing import Optional
from explorateur.state.state import _State
from explorateur.state.base_move import BaseMove


class Decision:
    """
    Represents a decision on a given state with a given move.
    The decision is used to determine whether a valid successor state exist.
    Executing the move on this state will generate a _State, if successful.
    If executing the move fails, there will be no successor state from this decision.
    """
    def __init__(self, state_: _State, move: BaseMove = None) -> None:
        self.state_: _State = state_
        self.move: BaseMove = move

    def __str__(self):
        if self.move:
            return str(self.state_) + " " + str(self.move)
        return str(self.state_)
