import json
from explorateur import Explorateur, ExplorationType, SearchType
from state import MyState
from explorateur.utils import run


# Romania graph[node] = Dict[node, distance]
with open('input.json') as json_file:
    graph = json.load(json_file)

initial_vertex = "Arad"
initial_state = MyState(initial_vertex, graph)

goal_vertex = "Bucharest"
goal_state = MyState(goal_vertex, graph)

# Arguments
args = {}
args["initial_state"] = initial_state
args["goal_state"] = goal_state
args["exploration_type"] = ExplorationType.DepthFirst()
args["search_type"] = SearchType.GraphSearch()
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