from explorateur.state.base_move import BaseMove


class Transition:
    """
    Transition from a previous state with a move
    """

    def __init__(self, previous_state_: '_State', move: BaseMove, depth: int):
        self.previous_state_ = previous_state_
        self.move = move
        self.depth = depth

    def __str__(self):
        return str(self.move) + " depth: " + str(self.depth)
