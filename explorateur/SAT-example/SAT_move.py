import abc
from explorateur.state.base_state import BaseState
from explorateur.state.base_move import BaseMove


# class BaseMove(metaclass=abc.ABCMeta):

#     @abc.abstractmethod
#     def __init__(self):
#         """Abstract method.
#         """
#         pass

#     @abc.abstractmethod
#     def execute(self, state: BaseState) -> bool:
#         """ Execute the move on the given state.
#         """
#         pass

#     @abc.abstractmethod
#     def undo(self, state: BaseState) -> bool:
#         """ Undo the move on the given state.
#         """
#         pass

#     @abc.abstractmethod
#     def is_valid(self, state: BaseState) -> bool:
#         """ Determine if move is valid in the given state.
#         """
#         pass

class SATMove(BaseMove):

    def __init__(self):
        self.variable = 0
        self.variable_assignment = True
        pass

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.variable_assignment = variable_assignment
        pass


    def execute(self, state: BaseState) -> bool:
        var_assignments = state.get_data()
        var_assignments[self.var] = self.variable_assignment
        state.variable_assignments = var_assignments
        return state.is_valid()
