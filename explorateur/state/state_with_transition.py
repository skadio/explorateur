from typing import List, NoReturn
from explorateur.state.base_state import BaseState
from explorateur.search.transition import Transition

class TransitionState():
    transition = Transition()
    base_state: BaseState

    def __init__(self, base_state: BaseState):
        self.base_state = base_state
    
    def get_transition(self) -> Transition:
        return self.transition

    def set_transition(self, transition: Transition):
        self.transition = transition