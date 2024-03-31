import abc
from explorateur.state._base_state import _BaseState


class BaseStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """Abstract method.
        """

    @abc.abstractmethod
    def insert(self, state: _BaseState):
        """
        """

    @abc.abstractmethod
    def remove(self) -> _BaseState:
        """
        """

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """
        """

    @abc.abstractmethod
    def get_size(self) -> int:
        """
        """

    @abc.abstractmethod
    def contains(self, state: _BaseState) -> _BaseState:
        """
        """

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass
