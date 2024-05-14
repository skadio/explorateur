import abc


class BaseMove(metaclass=abc.ABCMeta):
    """
    Abstract class for the moves.
    Model your problem as a sequence of states with moves
    encoding information to transition from one state to another.
    """

    @abc.abstractmethod
    def __init__(self):
        """
        Initializes the BaseMove object
        This can contain variable assignments etc.
        """

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the move.

        Returns:
            str: A string representation of the move.
        """

    def get_dot_label(self) -> str:
        """
           Return a string label for dot graph edge.

           Returns:
               str: A string label to display in dot graph.
        """
        return str(self)
