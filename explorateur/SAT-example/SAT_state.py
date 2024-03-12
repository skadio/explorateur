import abc
from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from SAT_move import SATMove
from explorateur.state.base_state import BaseState
from explorateur.state.base_variable import BaseVariable
from explorateur.search.transition import Transition


class SATState(BaseState):

    def __init__(self):
        self.variable_assignments = {}
        self.clauses = []
        self.unassigned_variables = []
        pass

    def get_valid_moves(self) -> List[BaseMove]:
        """
        """
        moves_list = []
        for var in self.unassigned_variables:
            for possible_val in var.get_possible_values():
                moves_list.append(SATMove(var, possible_val))

        return moves_list

    def is_solution(self) -> bool:
        """
        """
        for clause in self.clauses:
            isSatisfied = False
            for var in clause:
                if var > 0 and self.assignments[abs(var)]:
                    isSatisfied = True
                    break
                elif var < 0 and not self.assignments[abs(var)]:
                    isSatisfied = True
                    break
            if not isSatisfied:
                return False
        return True

    @abc.abstractmethod
    def get_data(self):
        """
        """
        return self.assignments

    @abc.abstractmethod
    def set_data(self) -> NoReturn:
        """
        """
        pass

    @abc.abstractmethod
    def get_transition(self) -> Transition:
        """
        """
        pass

    @abc.abstractmethod
    def set_transition(self, transition: Transition) -> NoReturn:
        """
        """
        pass

    def is_valid(self) -> bool:
        for clause in self.clauses:
            isUnsatisfiable = True
            for var in clause:
                if var > 0 and self.assignments[abs(var)]:
                    isUnsatisfiable = False
                    break
                elif var < 0 and not self.assignments[abs(var)]:
                    isUnsatisfiable = False
                    break
                elif abs(var) in self.variable_assignments.keys():
                    isUnsatisfiable = False
                    break
            if isUnsatisfiable:
                return False
        return True