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

    # This is required for graph search to check contains on already visited decisions
    def __eq__(self, other):
        if isinstance(other, Decision):
            return self.move == other.move and self.state == other.state
        return False

    # This is required for graph search when adding closed decision into hashset
    def __hash__(self):
        if self.move:
            return hash((self.state.__hash__(), self.move.__hash__()))
        else:
            return hash((self.state.__hash__()))