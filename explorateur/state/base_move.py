""" Module for the BaseMove class. """
import abc


class BaseMove(metaclass=abc.ABCMeta):
    """  Abstract class for the moves, model your problem as a sequence of states,
    with moves encoding information to transition from one state to another. """

    @abc.abstractmethod
    def __init__(self):
        """ Initializes the BaseMove object, can contain variable assignments and other setup."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """ 
        Return a string representation of the move.
        
        Returns:
            str: A string representation of the move.
        """