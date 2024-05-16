from explorateur import BaseMove


class MyMove(BaseMove):

    def __init__(self, var, constraint, val):
        # Move is the variable value assignment
        self.var: str = var
        self.constraint: str = constraint
        self.val: int = val

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return str(self.var) + " " + self.constraint + " " + str(self.val)

