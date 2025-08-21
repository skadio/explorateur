from explorateur import BaseMove

class Move(BaseMove):
    def __init__(self, var_index, value, bound_type="="):
        self.var_index = var_index
        self.value = value
        self.bound_type = bound_type  # "=", "<=", ">="

    def __str__(self) -> str:
        return f"x_{self.var_index} {self.bound_type} {self.value}"

    def get_dot_label(self) -> str:
        return f"x_{self.var_index}{self.bound_type}{self.value}"