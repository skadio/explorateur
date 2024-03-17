import abc
from typing import List, NoReturn
from explorateur.state.base_move import BaseMove

class BaseState(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """ Initializer for state, will likely contain variable assignments and variables
        """
        pass

    @abc.abstractmethod
    def get_valid_moves(self) -> List[BaseMove]:
        """
        """
        pass

    @abc.abstractmethod
    def is_solution(self) -> bool:
        """
        """
        pass

    @abc.abstractmethod
    def get_data(self):
        """
        """
        pass

    @abc.abstractmethod
    def set_data(self) -> NoReturn:
        """
        """
        pass



    @abc.abstractmethod
    def is_valid(self) -> bool:
        """
        """
        
        pass

    @abc.abstractmethod
    def execute(self, move: BaseMove) -> bool:
        """ Execute the given move on the state.
        """
        pass


