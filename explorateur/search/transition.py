from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class Transition:

    def __init__(self, previous_state: BaseState, move: BaseMove):
        self.previous_state = previous_state
        self.move = move
