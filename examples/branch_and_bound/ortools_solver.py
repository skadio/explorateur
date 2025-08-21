import numpy as np
from ortools.linear_solver.python import model_builder
import numpy.typing as npt
from typing import Union, Dict, Tuple


class ORToolsInstance:
    """
    OR-Tools based LP/IP solver that reads MPS files.
    Used for the lower bound computation in branch and bound algorithm.
    """
    
    def __init__(self, mps_file_path: str) -> None:
        self._load_from_mps(mps_file_path)
    
    def _load_from_mps(self, mps_file_path: str) -> None:
        """Load problem from MPS file."""
        self.mps_file_path = mps_file_path
        
        # Create model builder and load MPS file
        self.model = model_builder.ModelBuilder()
        
        try:
            self.model.import_from_mps_file(mps_file_path)
        except Exception as e:
            raise Exception(f'Failed to load MPS file {mps_file_path}: {e}')
        
        # Store variable information
        self.variables = list(self.model.get_variables())
        self.variable_names = [var.name for var in self.variables]
        self.variable_indices = {var.name: i for i, var in enumerate(self.variables)}
        
        self.num_variables = len(self.variables)
        self.num_constraints = len(list(self.model.get_linear_constraints()))
        
        print(f"Loaded MPS file: {mps_file_path}")
        print(f"Variables: {self.num_variables}, Constraints: {self.num_constraints}")
        
        # Store original bounds and integer status for restoration
        self.original_bounds = {}
        self.original_integer_status = {}
        for i, var in enumerate(self.variables):
            self.original_bounds[i] = (var.lower_bound, var.upper_bound)
            self.original_integer_status[i] = var.is_integral

    def solve(
        self,
        fixed_vars: Union[Dict[int, float], None] = None,
        bound_modifications: Union[Dict[int, Tuple[str, float]], None] = None,
        use_relaxation: bool = True
    ) -> Tuple[float, Union[npt.NDArray[np.float64], None]]:
        """
        Solve the LP relaxation or IP depending on use_relaxation flag.
        
        Args:
            fixed_vars: Dictionary mapping variable index to fixed value
            bound_modifications: Dictionary mapping variable index to (bound_type, value) 
                               where bound_type is "<=", ">=" or "="
            use_relaxation: If True, solve LP relaxation; if False, solve as IP
            
        Returns:
            Tuple of (objective_value, solution_vector)
        """
        
        return self._solve_mps_problem(fixed_vars, bound_modifications, use_relaxation)
    
    def _solve_mps_problem(self, fixed_vars, bound_modifications, use_relaxation):
        """Solve using model_builder for MPS problems."""
        # Set variable bounds for fixed variables and bound modifications
        modified_vars = []
        
        # Handle fixed variables (equality constraints)
        if fixed_vars:
            for var_index, value in fixed_vars.items():
                if 0 <= var_index < len(self.variables):
                    var = self.variables[var_index]
                    var.lower_bound = value
                    var.upper_bound = value
                    modified_vars.append(var_index)
        
        # Handle bound modifications (inequality constraints)
        if bound_modifications:
            for var_index, (bound_type, value) in bound_modifications.items():
                if 0 <= var_index < len(self.variables):
                    var = self.variables[var_index]
                    if bound_type == "<=":
                        var.upper_bound = min(var.upper_bound, value)
                    elif bound_type == ">=":
                        var.lower_bound = max(var.lower_bound, value)
                    elif bound_type == "=":
                        var.lower_bound = value
                        var.upper_bound = value
                    modified_vars.append(var_index)
        
        # For LP relaxation, make integer variables continuous
        modified_integer_vars = []
        if use_relaxation:
            for i, var in enumerate(self.variables):
                if var.is_integral:
                    var.is_integral = False
                    modified_integer_vars.append(i)
        
        # Create solver and solve
        solver = model_builder.ModelSolver('SCIP')
        status = solver.solve(self.model)
        
        objective_value = float("inf")
        solution_vector = None
        
        # Check if solution was found
        if status == model_builder.SolveStatus.OPTIMAL:
            objective_value = solver.objective_value
            solution_vector = np.array([solver.value(var) for var in self.variables])
        elif status == model_builder.SolveStatus.FEASIBLE:
            objective_value = solver.objective_value
            solution_vector = np.array([solver.value(var) for var in self.variables])
        
        # Restore original bounds for modified variables
        for var_index in modified_vars:
            if var_index in self.original_bounds:
                lb, ub = self.original_bounds[var_index]
                self.variables[var_index].lower_bound = lb
                self.variables[var_index].upper_bound = ub
        
        # Restore integer constraints if we were doing relaxation
        for var_index in modified_integer_vars:
            self.variables[var_index].is_integral = self.original_integer_status[var_index]
        
        return objective_value, solution_vector
    
    def get_objective_coefficients(self) -> np.ndarray:
        """Get the objective function coefficients from the MPS file."""
        coeffs = np.zeros(self.num_variables)
        
        # Get actual objective coefficients from the model
        try:
            obj_expr = self.model.objective_expression()
            coeffs_list = obj_expr.coeffs
            var_indices = obj_expr.variable_indices()
            
            # Map coefficients to variable indices
            for coeff, var_idx in zip(coeffs_list, var_indices):
                if var_idx < len(coeffs):
                    coeffs[var_idx] = coeff
                    
        except Exception as e:
            print(f"Warning: Could not get objective coefficients: {e}")
            # Fallback to uniform coefficients
            coeffs.fill(1.0)
            
        return coeffs
    
    def is_variable_integer(self, var_index: int) -> bool:
        """Check if a variable is integer."""
        if var_index >= len(self.variables):
            return False
        
        var = self.variables[var_index]
        return var.is_integral
    
    def get_variable_bounds(self, var_index: int) -> Tuple[float, float]:
        """Get the bounds of a variable."""
        if var_index >= len(self.variables):
            return (0.0, 0.0)
        
        var = self.variables[var_index]
        return (var.lower_bound, var.upper_bound)
    
    def export_model_string(self) -> str:
        """Export the model as a string for debugging."""
        return f"OR-Tools MPS model with {self.num_variables} variables and {self.num_constraints} constraints"
    
    def __str__(self) -> str:
        return f"ORToolsInstance: {self.num_variables} vars, {self.num_constraints} constraints"
