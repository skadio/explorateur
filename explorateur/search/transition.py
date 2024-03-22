from typing import Optional
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class Transition:
    def __init__(self, previous_state: 'TransitionState', move: BaseMove):
        self.previous_state = previous_state
        self.move = move


class TransitionState: #rename this
    def __init__(self, base_state: BaseState):
        self.base_state = base_state
        self.transition: Optional[Transition] = None

    def get_transition(self) -> Optional[Transition]:
        return self.transition

    def set_transition(self, transition: Optional[Transition]):
        self.transition = transition


#state.py (put transition state in there right now, one is the one the user gave us and the other one is the internal one)
# _BaseState --> internal one (look at what the prof will have emailed us)
