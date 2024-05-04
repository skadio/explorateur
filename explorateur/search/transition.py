'''Module for the Transition class.'''
from explorateur.state.base_move import BaseMove


class Transition:
    """
    Allows us to know what "move" (ie. transition) and previous state created a new state.
    """

    def __init__(self, previous_state: '_BaseState', move: BaseMove):
        self.previous_state = previous_state
        self.move = move
