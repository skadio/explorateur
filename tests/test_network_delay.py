from typing import Dict, List
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType
import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, matrix_to_str
from explorateur import Explorateur, ExplorationType, SearchType
from explorateur.utils import run


class MyMove(BaseMove):

    # Define move object
    def __init__(self, u):
        self.u = u

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return "Move to: " + str(self.u)


class MyState(BaseState):
    # Store a single copy of the problem graph
    graph = None

    # Problem specific state representation
    def __init__(self, v, cost=999, problem_graph: Dict[int, Dict[int, int]] = None):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()

        # Save the problem graph, only once
        if not MyState.graph:
            MyState.graph = problem_graph

        # State is the current vertex
        self.v = v
        self.cost = cost

    # Design branching decisions
    def get_moves(self) -> List[MyMove]:
        # Moves: Visit the neighbors of the current vertex
        return [MyMove(u) for u in MyState.graph[self.v].keys()]

    # Execute the move on the state, return success flag
    def execute(self, move: MyMove) -> bool:
        # Move to the next vertex and incur the cost
        self.cost = self.cost + self.graph[self.v][move.u]
        self.v = move.u

        return True

    # Check whether a state is the solution/termination
    def is_terminate(self, goal_state=None) -> bool:
        # Don't terminate, keep searching until all nodes are visited
        return False

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        text = "ID: " + str(self.id) + "\n"
        text += "Node: " + str(self.v) + "\n"
        text += "Cost: " + str(self.cost)
        return text

    # This is required for graph search to check contains on already visited states
    def __eq__(self, other):
        if isinstance(other, MyState):
            return self.v == other.v and self.cost < other.cost
        return False

    def __lt__(self, other):
        if isinstance(other, MyState):
            return self.cost < other.cost

    def __gt__(self, other):
        if isinstance(other, MyState):
            return self.cost > other.cost

    # This is required for graph search when adding closed states into hashset
    def __hash__(self):
        # The same vertex with a different cost is treated as different
        return hash(self.v) + hash(self.cost)

    def get_objective(self) -> float:
        return self.cost


class NetworkTest(BaseTest):

    # https://neetcode.io/problems/network-delay-time
    def test_game_of_death(self):

        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState(v=1, cost=0,
                                problem_graph={1: {2: 1, 4: 4},
                                               2: {3: 1},
                                               3: {4: 1},
                                               4: {}})

        # Arguments
        args = {}
        args["initial_state"] = initial_state
        args["goal_state"] = None
        args["exploration_type"] = ExplorationType.BestFirst()
        args["search_type"] = SearchType.GraphSearch()
        args["is_solution_path"] = True
        args["max_depth"] = 100
        args["max_moves"] = 100
        args["max_runtime"] = None
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "leet_network.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        # TODO Dijsktra's algorithm is currently incomplete..

        # Solution label
        # ground_truth_solution = [[MyState.DEAD, MyState.DEAD, MyState.EMPTY],
        #                          [MyState.EMPTY, MyState.DEAD, MyState.DEAD],
        #                          [MyState.EMPTY, MyState.DEAD, MyState.DEAD]]
        #
        # self.assertEqual(explorer.num_decisions, 4)
        # self.assertEqual(explorer.num_failed_decisions, 0)
        # self.assertEqual(len(explorer.solution_path), 5)
        # self.assertEqual(explorer.solution_state.grid, ground_truth_solution)
        # self.assertEqual(explorer.solution_state.num_alive, 0)

    # def test_game_of_death_no_solution(self):
    #     # Explorateur
    #     explorer = Explorateur(is_verbose=True)
    #
    #     # Initial state
    #     # Don't search the whole tree, stop at first feasible
    #     # Fake a few failing decisions
    #     initial_state = MyState()
    #
    #     # Arguments
    #     args = {}
    #     args["initial_state"] = initial_state
    #     args["goal_state"] = None
    #     args["exploration_type"] = ExplorationType.BreadthFirst()
    #     args["search_type"] = SearchType.TreeSearch()
    #     args["is_solution_path"] = True
    #     args["max_depth"] = 100
    #     args["max_moves"] = 100
    #     args["max_runtime"] = 100
    #     args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "tree_god.dot")
    #     args["is_verbose"] = True
    #
    #     # Run
    #     run(explorer, args)
    #
    #     # Solution label -- None
    #     self.assertIsNone(explorer.solution_state)
    #     self.assertIsNone(explorer.solution_path)
    #     # self.assertEqual(len(explorer.solution_path), 4)
    #     # self.assertEqual(explorer.solution_path[-1], initial_state)
