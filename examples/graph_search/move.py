from explorateur import BaseMove


class MyMove(BaseMove):

    def __init__(self, u):
        # Move is the next vertex to visit
        self.u: str = u

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return str(self.u)

    # This is required for graph search to check contains on already visited decisions
    def __eq__(self, other):
        if isinstance(other, MyMove):
            return self.u == other.u
        return False

    # This is required for graph search when adding closed decision into hashset
    def __hash__(self):
        return hash(self.u)
