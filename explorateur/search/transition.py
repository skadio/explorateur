class Transition:
    """
    Transition from a previous state with a move
    """

    def __init__(self, previous_state: 'BaseState', move: 'BaseMove', depth: int):
        self.previous_state = previous_state
        self.move = move
        self.depth = depth

    def __str__(self):
        return str(self.move) + " depth: " + str(self.depth)
