import abc


class BaseDotLabeler(metaclass=abc.ABCMeta):
    """
    Abstract class for returning dot representation to visualize nodes (BaseState) and edges (BaseMove) in dot graph.
    """

    @abc.abstractmethod
    def get_dot_label(self, num_moves: int, depth: int) -> str:
        """
        Return dot label to display to visualize dot graph.
        IF called from base state, it will return node label.
        IF called from base move, it will return edge label.

        Parameters:
            num_moves (int): The current iteration counter.
            depth (int): The current depth counter.

        Returns:
            str: The dot label string to visualize dot graph.
        """
