from typing import List, NoReturn, Optional
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from explorateur.search.transition import Transition


class _BaseState(BaseState):

    """
    This is used by our search() function in explorateur.py as a wrapper class around BaseState that allows us to include more information about the state. 
    All the functions in this class just call the equivalent function in Base State. 
    """

    def __init__(self, user_state: BaseState, node_label: str = ""):
        self.user_state = user_state
        self.transition = None
        self.node_label = node_label
        self.node = None

    def get_moves(self) -> List[BaseMove]:
        return self.user_state.get_moves()

    def execute(self, move: BaseMove) -> bool:
        return self.user_state.execute(move)

    def get_data(self):
        return self.user_state.get_data()

    def set_data(self) -> NoReturn:
        return self.user_state.set_data()

    def is_terminate(self, end_state=None):
        return self.user_state.is_terminate()

    def objective_function(self):
        return self.user_state.objective_function()

    def get_transition(self) -> Optional[Transition]:
        return self.transition

    def set_transition(self, transition: Optional[Transition]):
        self.transition = transition

    def __str__(self) -> str:
        return str(self.user_state)

    def make_node_label(self, iterations : int) -> str:
        return self.user_state.make_node_label(iterations)
