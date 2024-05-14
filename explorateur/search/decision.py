from explorateur.state.base_state import BaseState, BaseMove


class Decision:
    """
    Represents a decision on a given state with a given move.
    The decision is used to determine whether a valid successor state exist.
    Executing the given move on this given state will generate a new successor, if successful.
    If executing the move fails, there will be no successor state resulting from this decision.
    """
    def __init__(self, state: BaseState, move: BaseMove = None) -> None:
        self.state: BaseState = state
        self.move: BaseMove = move

    def __str__(self):
        if self.move:
            return str(self.state) + " " + str(self.move)
        return str(self.state)
