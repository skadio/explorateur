''' Contains the _BaseState class, a wrapper class around BaseState that allows us to include more information about
the state. '''
from typing import List, Optional, Union
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState
from explorateur.search.transition import Transition


class _BaseState():
    """
    This is used by our search() function in explorateur.py as a wrapper class around BaseState. 
    All the functions in this class just call the equivalent function in Base State. 
    """

    def __init__(self, user_state: BaseState, node_label: str = ""):
        self.user_state = user_state
        self.transition = None
        self.node_label = node_label
        self.node = None

    def get_moves(self) -> List[BaseMove]:
        """ Get the moves from the user state """
        return self.user_state.get_moves()

    def is_terminate(self, end_state: Union[BaseState, None] = None):
        """ Check if the user state is a termination state, using the user state's is_terminate function """
        return self.user_state.is_terminate(end_state)

    def execute(self, move: BaseMove) -> bool:
        """ Execute a move, using the user state's execute function """
        return self.user_state.execute(move)

    def objective_function(self):
        """ Return the objective function value, using the user state's objective_function function """
        return self.user_state.objective_function()

    def is_valid(self):
        """ Check if the user state is valid, using the user state's is_valid function """
        return self.user_state.is_valid()

    def __str__(self) -> str:
        """ Return the string representation of the user state """
        return str(self.user_state)

    def make_node_label(self, iterations: int) -> str:
        """ Make a node label, using the user state's make_node_label function """
        return self.user_state.make_node_label(iterations)

    def get_transition(self) -> Optional[Transition]:
        """ Get the transition that led to this state"""
        return self.transition

    def set_transition(self, transition: Optional[Transition]):
        """ Set the transition that led to this state"""
        self.transition = transition
