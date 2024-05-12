import abc
from typing import List, Union
from explorateur.state.base_move import BaseMove


class BaseState(metaclass=abc.ABCMeta):
    """
    Abstract class for the states.
    Model your problem as a state and transition between states via moves until termination.
    """

    @abc.abstractmethod
    def __init__(self):
        """ 
        Initializer for state.
        For example, this can store variable and value assignments in the current state.
        """

    @abc.abstractmethod
    def execute(self, move: BaseMove) -> bool:
        """
        Execute the given move on the state and return a boolean to denote successful (valid) execution.

        Parameters:
        move (BaseMove): The move to be executed on the state.

        Returns:
            bool: True if the execution was successful (valid), False otherwise.
        """

    @abc.abstractmethod
    def get_moves(self) -> List[BaseMove]:
        """
        Return an ordered list of moves.
        Moves are alternative search decisions to be explored from this state.

        Returns:
            List[BaseMove]: A list of moves to explore from this state.
        """

    @abc.abstractmethod
    def is_terminate(self, end_state: Union['BaseState', None]) -> bool:
        """
        Checks if the current state is a termination state.
            If doing tree search, this can check if the state is a solution to the problem.
            If doing graph search, this can check if the state is equivalent to the given end state.

        Parameters:
            end_state: The end state to compare with (optional).

        Returns:
            bool: True if the current state is a termination state, False otherwise.
        """

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the state.

        Returns:
            str: A string representation of the state.
        """
