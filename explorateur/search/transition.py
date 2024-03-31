from explorateur.state.base_move import BaseMove
# from explorateur.state._base_state import _BaseState


class Transition:
    # previous_state should be type decorated, but can't bc of circular imports
    def __init__(self, previous_state, move: BaseMove):
        self.previous_state = previous_state
        self.move = move
        