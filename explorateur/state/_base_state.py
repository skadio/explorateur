from typing import List, NoReturn, Optional
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from explorateur.search.transition import Transition

class _BaseState(BaseState):
    
    def __init__(self, user_state: BaseState):
        self.user_state = user_state
    
    def get_moves(self) -> List[BaseMove]:
        return self.user_state.get_moves()
    
    def execute(self, move: BaseMove) -> bool:
        return self.user_state.execute(move)
    
    def get_data(self):
        return self.user_state.get_data()

    def set_data(self) -> NoReturn:
        return self.user_state.set_data()
        
    def is_valid(self):
        return self.user_state.is_valid()
    
    def is_solution(self):
        return self.user_state.is_solution()

    def get_transition(self) -> Optional[Transition]:
        return self.transition

    def set_transition(self, transition: Optional[Transition]):
        self.transition = transition