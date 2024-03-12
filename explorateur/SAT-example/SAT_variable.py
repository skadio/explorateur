import abc

from explorateur.state.base_variable import BaseVariable

class SATVariable(BaseVariable):

    def __init__(self, possible_values):
        self.possible_values = possible_values

    def get_possible_values(self) -> list:
        return self.possible_values