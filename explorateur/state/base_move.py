import abc
from explorateur.state.base_state import BaseState


class BaseMove(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
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

    @abc.abstractmethod
    def is_valid(self, state: BaseState) -> bool:
        """ Determine if move is valid in the given state.
        """
        pass
