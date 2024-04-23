import abc


class BaseMove(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        """ 
        Initializer, will likely conain variable and assignment
        """
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        """ 
        Return a string representation of the move.
        """
        pass

    # @abc.abstractmethod
    # def execute(self, state: BaseState) -> bool:
    #     """ Execute the move on the given state.
    #     """
    #     pass
