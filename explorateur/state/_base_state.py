from typing import Optional
from explorateur.state.base_state import BaseState
from explorateur.search.transition import Transition

def _BaseState(BaseState):

	def __init__(self, user_state: BaseState):
	    self.user_state = user_state

	def is_valid(self):
		return self.user_state.is_valid()
    
    def is_solution(self):
        return self.user_state.is_solution()

	def get_transition(self) -> Optional[Transition]:
		return self.transition

	def set_transition(self, transition: Optional[Transition]):
		self.transition = transition