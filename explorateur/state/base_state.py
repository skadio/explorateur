import abc
from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_variable import BaseVariable
from explorateur.search.transition import Transition


class BaseState(metaclass=abc.ABCMeta):

    variable_assignments = {}
    unassigned_variables: List[BaseVariable] = []


    @abc.abstractmethod
    def __init__(self, variable_assignments, unassigned_variables):
        """Abstract method.
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
    def get_data(self) -> dict:
        """
        """
        pass

    @abc.abstractmethod
    def set_data(self) -> NoReturn:
        """
        """
        pass

    @abc.abstractmethod
    def get_transition(self) -> Transition:
        """
        """
        pass

    @abc.abstractmethod
    def set_transition(self, transition: Transition) -> NoReturn:
        """
        """
        pass

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """
        """
        
        pass

