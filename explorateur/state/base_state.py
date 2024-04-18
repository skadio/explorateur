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
    def get_moves(self) -> List[BaseMove]:   #comment for the user about the order for bfs
        """
        """
        pass

    @abc.abstractmethod
    def is_terminate(self) -> bool:
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
    def execute(self, move: BaseMove) -> bool:
        """ Execute the given move on the state and returns a boolean on whether or not the execution on the previous state
        """
        pass
    
    @abc.abstractmethod
    def objective_function(self) -> float:
        """
        If the user decides to implement a best first search that requires a priority queue which needs a way to "rank" the states
        """
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        """
        pass

    