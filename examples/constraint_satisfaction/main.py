from explorateur import Explorateur, ExplorationType, SearchType
from state import MyState
from explorateur.utils import run

# CSP with 3 variables each with 2 values in their domain
var_to_domain={"x": [1, 2], "y": [10, 20], "z": [100, 200]}
initial_state = MyState(var_to_domain)

# Arguments
args = {}
args["initial_state"] = initial_state
args["goal_state"] = None
args["exploration_type"] = ExplorationType.DepthFirst()
args["search_type"] = SearchType.TreeSearch()
args["is_solution_path"] = True
args["max_depth"] = 100
args["max_moves"] = 100
args["max_runtime"] = 100
args["dot_filename"] = "output.dot"
args["is_verbose"] = True

# Explorateur
explorer = Explorateur(is_verbose=True)
run(explorer, args)
assert explorer.num_decisions == 14
assert explorer.num_failed_decisions == 0

# Example DOT file viewer: https://dreampuf.github.io/GraphvizOnline
