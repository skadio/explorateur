import abc
from explorateur.state.base_state import BaseState
from typing import NoReturn


class BaseObjective(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """Abstract method.
        """
        pass

    @abc.abstractmethod
    def get_objective_value(self, state: BaseState) -> float:
        """
        """
        pass

    @abc.abstractmethod
    def set_objective_value(self, state: BaseState) -> NoReturn:
        """
        """
        pass