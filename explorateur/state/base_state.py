import abc
from typing import List, NoReturn
from explorateur.state.base_move import BaseMove


class BaseState(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """ 
        Initializer for state, will likely contain variable assignments and variables
        """
        pass

    @abc.abstractmethod
    def get_moves(self) -> List[BaseMove]:   
        """
        Return a list of moves (what else could be explored from this state) 
        """
        pass

    @abc.abstractmethod
    def is_terminate(self) -> bool:
        """
        If doing tree search, will check if the state is a solution state to the problem and in the case of graph search check if this state is equivalent to the goal state. 
        """
        pass

    @abc.abstractmethod
    def get_data(self):
        """
        Any data the user would like to see from the state. 
        """
        pass

    @abc.abstractmethod
    def set_data(self) -> NoReturn:
        """
        Setting any data that the user would like get_data() to provide. 
        """
        pass

    @abc.abstractmethod
    def execute(self, move: BaseMove) -> bool:
        """ 
        Execute the given move on the state and returns a boolean on whether or not the execution was successful / valid. 
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
        Return a string rerpesentation of the state. 
        """
        pass

    