from explorateur import BaseMove


class MyMove(BaseMove):

    def __init__(self, u):
        # Move is the next vertex to visit
        self.u: str = u

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return str(self.u)
