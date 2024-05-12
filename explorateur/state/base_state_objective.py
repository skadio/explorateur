import abc
from explorateur.state.base_state import BaseState


class BaseStateObjective(metaclass=abc.ABCMeta):
    """
    Abstract class for returning the objective of a given state.
    To be used for optimization problems.
    """

    @abc.abstractmethod
    def get_objective(self, state: BaseState) -> float:
        """
        Return the objective value of the state.

        Best-First Search requires an evaluation of states for ranking.

        Note, if this function returns the same value for two states
        there will be an error because there is no comparator between abstract Base States.

        Returns:
            float: The objective function value for the state.
        """
