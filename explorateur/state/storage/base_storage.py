''' This module has the abstract class BaseStorage which is the base for all storage classes.'''
from typing import Union
import abc
from explorateur.state._base_state import _BaseState


class BaseStorage(metaclass=abc.ABCMeta):
    """Abstract class for the storage classes."""

    @abc.abstractmethod
    def __init__(self):
        """Initializer for the storage class."""

    @abc.abstractmethod
    def insert(self, state: _BaseState):
        """Inserts a state into storage."""

    @abc.abstractmethod
    def remove(self) -> _BaseState:
        """Removes a state from storage."""

    @abc.abstractmethod
    def is_empty(self) -> bool:
        """Returns True if the storage is empty, False otherwise."""

    @abc.abstractmethod
    def get_size(self) -> int:
        """Returns the number of elements in the storage."""

    @abc.abstractmethod
    def contains(self, state: _BaseState) -> bool:
        """ Returns True if the state is in the storage, False otherwise."""
