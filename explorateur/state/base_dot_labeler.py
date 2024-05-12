import abc


class BaseDotLabeler(metaclass=abc.ABCMeta):
    """
    Abstract class for returning dot representation to visualize nodes (BaseState) and edges (BaseMove) in dot graph.
    """

    @abc.abstractmethod
    def get_dot_label(self, num_decisions: int, depth: int) -> str:
        """
        Return dot label to display to visualize dot graph.
        IF called from base state, it will return node label.
        IF called from base move, it will return edge label.

        Parameters:
            num_decisions (int): The current decision counter.
                                 Decision refers to a particular state paired with a particular move.
            depth (int): The current depth counter.
                         Depth refers to the decision levels.
                         All moves from the same state will have the same depth.
                         The moves from a successor state will have depth + 1, and so on.

        Returns:
            str: The dot label string to visualize dot graph.
        """
