from explorateur import BaseState
import numpy as np

from move import Move

class State(BaseState):
    _lp_instance = None
    _best_objective = float("inf")
    _best_solution = None
    _best_fixed_vars = None
    _integer_tolerance = 1e-5 # For integer solution detection
    _found_solution = False

    def __init__(
        self,
        lp_instance,
        fixed_vars=None,
        bound_modifications=None,
        var_selection_strategy="weighted",
    ):
        super().__init__()
        if State._lp_instance is None:
            State._lp_instance = lp_instance
        
        self.fixed_vars = dict(fixed_vars) if fixed_vars else {}
        self.bound_modifications = dict(bound_modifications) if bound_modifications else {}
        self.var_selection_strategy = var_selection_strategy
        
        # Solve LP relaxation
        self.objective, self.solution = State._lp_instance.solve(
            fixed_vars=self.fixed_vars,
            bound_modifications=self.bound_modifications,
            use_relaxation=True
        )

        # Update best solution if needed
        if self.solution is not None and self.is_integer_solution() and self.objective < State._best_objective:
            State._best_objective = self.objective
            State._best_solution = np.copy(self.solution)
            State._best_fixed_vars = dict(self.fixed_vars)
            State._found_solution = True
            
    def __lt__(self, other):
        """For BestFirst search: compare states based on objective value (lower is better)"""
        if self.solution is None:
            return False
        if other.solution is None:
            return True
        
        return self.objective < other.objective

    def is_integer_solution(self):
        """Check if the solution satisfies integer constraints for integer variables"""
        if self.solution is None:
            return False
        
        # Check only integer variables for integrality
        for i, val in enumerate(self.solution):
            if State._lp_instance.is_variable_integer(i):
                # Check if the value is close to an integer
                if abs(val - round(val)) > self._integer_tolerance:
                    return False
        
        return True

    def is_terminate(self, goal_state=None) -> bool:
        # NEVER TERMINATE because we are looking for absolute optimal solution
        # We never terminate, we need to explore everything (implicity or explicitly)
        return False

    def get_moves(self) -> list[Move]:
        # Prune: only prune if current bound is worse than best known solution
        if self.solution is None or self.objective >= State._best_objective:
            return []

        # Find fractional integer variables that need branching
        fractional_indices = []
        for i, val in enumerate(self.solution):
            if State._lp_instance.is_variable_integer(i):
                # Check if the value is fractional (not close to an integer)
                if abs(val - round(val)) > self._integer_tolerance:
                    fractional_indices.append(i)
        
        fractional_indices = np.array(fractional_indices)
        
        # Integer solution
        if len(fractional_indices) == 0:
            return []

        # Choose variable to branch on
        branch_var = self.select_branching_variable(fractional_indices)

        # Create branching moves: x <= floor(val) and x >= ceil(val)
        val = self.solution[branch_var]
        floor_val = int(np.floor(val))
        ceil_val = int(np.ceil(val))
        
        # Create two branches: x <= floor_val and x >= ceil_val
        return [Move(branch_var, floor_val, "<="), Move(branch_var, ceil_val, ">=")]

    def select_branching_variable(self, fractional_indices):
        if self.var_selection_strategy == "first":
            return fractional_indices[0]

        elif self.var_selection_strategy == "most_fractional":
            distances = np.abs(self.solution[fractional_indices] - 0.5)
            return fractional_indices[np.argmin(distances)]

        elif self.var_selection_strategy == "weighted":
            # Use objective coefficients as weights for variable selection
            obj_coeffs = State._lp_instance.get_objective_coefficients()
            weights = obj_coeffs[fractional_indices]
            return fractional_indices[np.argmax(weights)]

    def execute(self, move: Move) -> bool:
        # Handle different constraint types
        if move.bound_type == "=":
            # Fixed variable (equality constraint)
            new_fixed_vars = dict(self.fixed_vars)
            new_fixed_vars[move.var_index] = move.value
            self.fixed_vars = new_fixed_vars
        else:
            # Bound modification (inequality constraint)
            new_bound_modifications = dict(self.bound_modifications)
            new_bound_modifications[move.var_index] = (move.bound_type, move.value)
            self.bound_modifications = new_bound_modifications
        
        # Solve LP relaxation
        self.objective, self.solution = State._lp_instance.solve(
            fixed_vars=self.fixed_vars,
            bound_modifications=self.bound_modifications,
            use_relaxation=True
        )
        
        # Update best solution if needed
        if self.solution is not None and self.is_integer_solution() and self.objective < State._best_objective:
            State._best_objective = self.objective
            State._best_solution = np.copy(self.solution)
            State._best_fixed_vars = dict(self.fixed_vars)
            State._found_solution = True
            
        return self.solution is not None

    def get_objective(self) -> float:
        return self.objective if self.solution is not None else float("inf")

    def __str__(self) -> str:
        return f"Obj:{self.objective:.2f}, Fixed:{len(self.fixed_vars)}"
    
    def get_dot_label(self) -> str:
        return f"Obj:{self.objective:.2f}"

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.fixed_vars == other.fixed_vars and 
                self.bound_modifications == other.bound_modifications)

    def __hash__(self):
        fixed_items = frozenset(self.fixed_vars.items())
        bound_items = frozenset(self.bound_modifications.items())
        return hash((fixed_items, bound_items))