import abc
from explorateur.state.base_state import BaseState


class BaseStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """Abstract method.
        """
        pass

    @abc.abstractmethod
    def insert(self, state: BaseState):
        """
        """
        pass

    @abc.abstractmethod
    def remove(self, state: BaseState) -> BaseState:
        """
        """
        pass

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """
        """
        pass

    @abc.abstractmethod
    def get_size(self) -> int:
        """
        """
        pass

    @abc.abstractmethod
    def contains(self, state: BaseState) -> BaseState:
        """
        """
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass