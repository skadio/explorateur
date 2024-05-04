''' Module for the BaseState class, which is an abstract class for the states. '''
import abc
from typing import List, Union
from explorateur.state.base_move import BaseMove


class BaseState(metaclass=abc.ABCMeta):
    ''' Abstract class for the states, model your problem as a sequence of states. '''

    @abc.abstractmethod
    def __init__(self):
        """ 
        Initializer for state, will likely contain variable assignments and variables
        """

    @abc.abstractmethod
    def get_moves(self) -> List[BaseMove]:
        """
        Return a list of moves (what else could be explored from this state) 

        Returns:
            List[BaseMove]: A list of moves that can be explored from this state.
        """

    @abc.abstractmethod
    def is_terminate(self, end_state: Union['BaseState', None]) -> bool:
        """
        Checks if the current state is a termination state.
            If doing tree search, this function should check if the state is a solution state to the problem.
            If doing graph search, this function should check if the state is equivalent to the end state.

        Parameters:
        - end_state: The end state to compare with (optional).

        Returns:
        - bool: True if the current state is a termination state, False otherwise.
        """

    @abc.abstractmethod
    def execute(self, move: BaseMove) -> bool:
        """
        Execute the given move on the state and returns a boolean on whether or not the execution was successful /
        valid.

        Parameters:
        - move (BaseMove): The move to be executed on the state.

        Returns:
        - bool: True if the execution was successful / valid, False otherwise.
        """

    def objective_function(self) -> float:
        """
        [Optional]Calculates and returns the objective function value for the state.
        
        Used in best first search algorithms that require a priority queue to rank the states. Note, if this function
        returns the same value for two states this prrogram will error because there is no comparator between Base
        States.
        
        Returns:
            float: The objective function value for the state.
        """
        raise NotImplementedError("Objective function not implemented")

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the given state is valid. This method is strongly encouraged to be used within the execute method.
        
        Returns:
            bool: True if the state is valid, False otherwise.
        """

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Return a string rerpesentation of the state. 

        Returns:
            str: A string representation of the state.
        """

    @abc.abstractmethod
    def make_node_label(self, iterations: int) -> str:
        """
        Method to generate a label for a node, will be passed number of iterations.

        Parameters:
        - iterations (int): The number of iterations.

        Returns:
        - str: The generated label for the node (Can be dependent on iterations or not).
        """
