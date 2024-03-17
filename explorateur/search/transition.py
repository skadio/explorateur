from explorateur.state.base_move import BaseMove
# from explorateur.state.base_state import BaseState
from explorateur.state.state_with_transition import TransitionState


class Transition:

    def __init__(self, previous_state: TransitionState, move: BaseMove):
        self.previous_state = previous_state
        self.move = move
