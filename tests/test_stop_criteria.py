import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, MyState
from explorateur import Explorateur, ExplorationType, SearchType
from explorateur.utils import run


class StopCriteriaTest(BaseTest):

    def test_max_moves_5(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Arguments
        args = {}
        args["initial_state"] = initial_state
        args["goal_state"] = None
        args["exploration_type"] = ExplorationType.DepthFirst()
        args["search_type"] = SearchType.TreeSearch()
        args["is_solution_path"] = True
        args["max_depth"] = 100
        args["max_moves"] = 5
        args["max_runtime"] = 100
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "stop_criteria.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        self.assertEqual(explorer.num_decisions, 5)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_depth_1(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Arguments
        args = {}
        args["initial_state"] = initial_state
        args["goal_state"] = None
        args["exploration_type"] = ExplorationType.DepthFirst()
        args["search_type"] = SearchType.TreeSearch()
        args["is_solution_path"] = True
        args["max_depth"] = 1
        args["max_moves"] = 100
        args["max_runtime"] = 100
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "stop_criteria.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        self.assertEqual(explorer.num_decisions, 2)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_depth_2(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Arguments
        args = {}
        args["initial_state"] = initial_state
        args["goal_state"] = None
        args["exploration_type"] = ExplorationType.DepthFirst()
        args["search_type"] = SearchType.TreeSearch()
        args["is_solution_path"] = True
        args["max_depth"] = 2
        args["max_moves"] = 100
        args["max_runtime"] = 100
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "stop_criteria.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        self.assertEqual(explorer.num_decisions, 6)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_runtime(self):
        pass
