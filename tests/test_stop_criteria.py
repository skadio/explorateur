import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, MyState
from explorateur import Explorateur, ExplorationType, SearchType



class ExplorationStoppingCriteriaTests(BaseTest):

    def test_max_moves_5(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Search
        self.search(explorer,
                    initial_state,
                    goal_state=None,
                    exploration_type=ExplorationType.DepthFirst(),
                    search_type=SearchType.TreeSearch(),
                    is_solution_path=True,
                    max_depth=100,
                    max_moves=5,
                    max_runtime=100,
                    dot_filename=os.path.join(Constants.TEST_DATA_DIR, "usage_example.dot"),
                    is_verbose=True)

        self.assertEqual(explorer.num_decisions, 5)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_moves_0(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Search
        self.search(explorer,
                    initial_state,
                    goal_state=None,
                    exploration_type=ExplorationType.DepthFirst(),
                    search_type=SearchType.TreeSearch(),
                    is_solution_path=True,
                    max_depth=100,
                    max_moves=0,
                    max_runtime=100,
                    dot_filename=os.path.join(Constants.TEST_DATA_DIR, "usage_example.dot"),
                    is_verbose=True)

        self.assertEqual(explorer.num_decisions, 5)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_depth_1(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Search
        self.search(explorer,
                    initial_state,
                    goal_state=None,
                    exploration_type=ExplorationType.DepthFirst(),
                    search_type=SearchType.TreeSearch(),
                    is_solution_path=True,
                    max_depth=1,
                    max_moves=100,
                    max_runtime=100,
                    dot_filename=os.path.join(Constants.TEST_DATA_DIR, "stop_criteria.dot"),
                    is_verbose=True)

        self.assertEqual(explorer.num_decisions, 2)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_depth_2(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        # Search
        self.search(explorer,
                    initial_state,
                    goal_state=None,
                    exploration_type=ExplorationType.DepthFirst(),
                    search_type=SearchType.TreeSearch(),
                    is_solution_path=True,
                    max_depth=2,
                    max_moves=100,
                    max_runtime=100,
                    dot_filename=os.path.join(Constants.TEST_DATA_DIR, "stop_criteria.dot"),
                    is_verbose=True)

        self.assertEqual(explorer.num_decisions, 6)
        self.assertEqual(explorer.num_failed_decisions, 0)

    def test_max_runtime(self):
        pass