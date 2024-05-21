import abc
from typing import Optional

from explorateur.state.base_state import BaseState


class BaseStorage(metaclass=abc.ABCMeta):
    """
    Abstract class for the storage classes.
    """

    @abc.abstractmethod
    def __init__(self):
        """Initializer for the storage class."""

    @abc.abstractmethod
    def insert(self, state: BaseState):
        """Inserts a state into storage."""

    @abc.abstractmethod
    def remove(self) -> BaseState:
        """Removes a state from storage."""

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the storage is empty, False otherwise."""

    @abc.abstractmethod
    def size(self) -> int:
        """Returns the number of elements in the storage."""

    @abc.abstractmethod
    def contains(self, state: BaseState) -> Optional[BaseState]:
        """ Returns the state if it is in the storage, None otherwise."""
