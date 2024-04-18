from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


class SATMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable  # variable
        self.value = variable_assignment
        # self.variable_assignment = variable_assignment


class SATState(BaseState):

    def __init__(self):
        self.variable_assignments = {}  # varToVal (naming convention)
        self.clauses = []
        self.unassigned_variables = set()

    def get_valid_moves(self) -> List[SATMove]:
        """
        """
        moves_list = []
        for var in self.unassigned_variables:
            moves_list.append(SATMove(var, True))
            moves_list.append(SATMove(var, False))

        return moves_list

    def is_terminate(self) -> bool:
        """
        """
        for clause in self.clauses:
            isSatisfied = False
            for literal in clause:
                if abs(literal) not in self.variable_assignments.keys():
                    continue
                if literal > 0 and self.variable_assignments[abs(literal)]:
                    isSatisfied = True
                    break
                elif literal < 0 and not self.variable_assignments[abs(literal)]:
                    isSatisfied = True
                    break
            if not isSatisfied:
                return False
        return True

    def get_data(self) -> dict:
        return self.variable_assignments

    def set_data(self) -> NoReturn:
        """
        """
        pass

    def is_valid(self) -> bool:
        for clause in self.clauses:
            isUnsatisfiable = True
            for var in clause:
                if abs(var) not in self.variable_assignments.keys():
                    isUnsatisfiable = False
                    break
                elif var > 0 and self.variable_assignments[abs(var)]:
                    isUnsatisfiable = False
                    break
                elif var < 0 and not self.variable_assignments[abs(var)]:
                    isUnsatisfiable = False
                    break
            if isUnsatisfiable:
                return False
        return True

    def execute(self, move: SATMove) -> bool:
        # don't need the absolute
        self.variable_assignments[abs(
            move.variable)] = move.variable_assignment
        self.unassigned_variables.remove(abs(move.variable))
        # can move is_valid() to inside this function, the contract for execute should also include letting us know if the move was successful or not
        return self.is_valid()
