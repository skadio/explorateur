import abc
from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.search.transition import Transition


class BaseState(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
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
    def get_transition(self) -> Transition:
        """
        """
        pass

    @abc.abstractmethod
    def set_transition(self, transition: Transition) -> NoReturn:
        """
        """
        pass