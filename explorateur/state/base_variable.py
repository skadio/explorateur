import abc


class BaseVariable(metaclass=abc.ABCMeta):

    possible_values = []
    # List of bools or list of ints / what type should this be

    @abc.abstractmethod
    def __init__(self, possible_values):
        """Abstract method.
        """
        pass

    @abc.abstractmethod
    def get_possible_values(self) -> list:
        pass