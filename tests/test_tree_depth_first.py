import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, MyState, MyMove
from explorateur import Explorateur, ExplorationType, SearchType
from explorateur.utils import run


class TreeDepthTest(BaseTest):

    def test_tree_depth_feasible(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        # Don't search the whole tree, stop at first feasible
        # Fake a few failing decisions
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]},
                                is_exhaustive_search=False)

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
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "tree_depth_first.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        # Solution label
        ground_truth_solution = {"x": 1, "y": 10, "z": 100}
        self.assertEqual(explorer.num_decisions, 3)
        self.assertEqual(explorer.num_failed_decisions, 0)
        self.assertEqual(len(explorer.solution_path), 4)
        self.assertEqual(explorer.solution_path[-1], initial_state)
        self.assertEqual(explorer.solution_state.var_to_val, ground_truth_solution)
        self.assertEqual(explorer.solution_state.unassigned, [])

    def test_tree_depth_feasible_with_fakefails(self):

        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        # Don't search the whole tree, stop at first feasible
        # Fake a few failing decisions
        initial_state = MyState({"x":[1,2], "y":[10, 20], "z":[100, 200]},
                                is_exhaustive_search=False,
                                fake_fails=[MyMove("x", "==", 1), MyMove("z", "==", 100)])

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
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "tree_depth_first.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        # Solution label
        ground_truth_solution = {"x": 2, "y": 10, "z": 200}
        self.assertEqual(explorer.num_decisions, 5)
        self.assertEqual(explorer.num_failed_decisions, 2)
        self.assertEqual(len(explorer.solution_path), 4)
        self.assertEqual(explorer.solution_path[-1], initial_state)
        self.assertEqual(explorer.solution_state.var_to_val, ground_truth_solution)
        self.assertEqual(explorer.solution_state.unassigned, [])
