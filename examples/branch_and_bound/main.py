import json
import sys
import time

from pathlib import Path

from explorateur import Explorateur, ExplorationType, SearchType
from ortools_solver import ORToolsInstance
from state import State



# Branch and bound algorithm for solving generic binary/integer programming problems
# Uses the linear programming relaxation of the integer programming problem
# as a lower bound for the search
class BranchAndBound:
    def __init__(self, mps_file_path: str) -> None:
        self.lp_instance = ORToolsInstance(mps_file_path)

        
    def objective_function(self, state):
        return state.get_objective()

    def solve(self, var_selection_strategy="weighted", exploration_type="best_first"):
        # Reset class variables before starting a new search
        State._lp_instance = None
        State._best_objective = float("inf")
        State._best_solution = None
        State._best_fixed_vars = None
        State._found_solution = False
        
        # Debug
        explorer = Explorateur(is_verbose=False) 

        # Root node
        initial_state = State(
            self.lp_instance, var_selection_strategy=var_selection_strategy
        )

        # Search type - Use BestFirst for branch and bound (always explore lowest bound first)
        exp_type = ExplorationType.BestFirst()
        
        # Run search
        print(
            f"Starting Explorateur search with BestFirst strategy and {var_selection_strategy} variable selection"
        )
        print(f"Problem has {self.lp_instance.num_variables} variables and {self.lp_instance.num_constraints} constraints")

        found_solution = explorer.search(
            initial_state,
            exploration_type=exp_type,
            search_type=SearchType.GraphSearch(),  # This yields the same result as TreeSearch() for bnb, as the graph is a tree
            is_solution_path=False,             
            max_depth=100,                     
            max_moves=10000,                  
            dot_filename="output.dot",
        )

        print(f"Explorateur processed {explorer.num_decisions} nodes.")
        
        if State._found_solution:
            print(f"Best objective: {State._best_objective}")
            return State._best_objective
        else:
            print("No solution found.")
            return float("inf")




# Main function
def main(mps_file_path: str):
    filename = Path(mps_file_path).name
    print(f"Solving MPS file: {filename}")
    
    start_time = time.time()

    solver = BranchAndBound(mps_file_path)
    print(solver.lp_instance.export_model_string())
    
    # Solve the LP relaxation first to get an initial bound
    lp_obj, lp_sol = solver.lp_instance.solve(use_relaxation=True)
    print(f"LP relaxation objective: {lp_obj}")

    best_cost = solver.solve()
    end_time = time.time()

    total_time = "{:.2f}".format(end_time - start_time)
    best_cost = best_cost if best_cost != float("inf") else "--"

    sol_dict = {
        "Instance": filename,
        "Time": total_time,
        "Result": best_cost,
        # "Solution": "OPT" if best_cost != float("inf") else "--"
    }
    print(json.dumps(sol_dict))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <mps_file>")
        print("Example: python main.py ../data/model1.mps")
        sys.exit(1)
        
    mps_file_path = sys.argv[1]
    main(mps_file_path)