import abc
from explorateur.state.base_state import BaseState
from explorateur.state.base_variable import BaseVariable


class BaseMove(metaclass=abc.ABCMeta):

    variable: BaseVariable
    variable_assignment = 0

    @abc.abstractmethod
    def __init__(self):
        """Abstract method.
        """
        pass

    @abc.abstractmethod
    def __init__(self, variable, variable_assignment):
        """Abstract method.
        """
        pass

    @abc.abstractmethod
    def execute(self, state: BaseState) -> bool:
        """ Execute the move on the given state.
        """
        pass

    @abc.abstractmethod
    def undo(self, state: BaseState) -> bool:
        """ Undo the move on the given state.
        """
        pass

    # Not sure where this would be used, validity should be a function of a state 
    # b/c access to constraints is only in the state, not in the move
    # @abc.abstractmethod
    # def is_valid(self, state: BaseState) -> bool:
    #     """ Determine if move is valid in the given state.
    #     """
    #     pass
