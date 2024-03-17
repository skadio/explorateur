from explorateur.state.base_move import BaseMove
from SAT_state import SATState

class SATMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.variable_assignment = variable_assignment


    def execute(self, state: SATState) -> bool:
        
        self.var_assignments = state.get_data()
        self.var_assignments[self.var] = self.variable_assignment
        state.variable_assignments = self.var_assignments
        return state.is_valid()
