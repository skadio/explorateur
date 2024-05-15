import os
from explorateur.utils import Constants
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from tests.test_base import BaseTest, MyState


class InvalidTest(BaseTest):

    def test_no_initial_state(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        with self.assertRaises(ValueError):
            # Search
            self.search(explorer,
                        initial_state=None,
                        goal_state=None,
                        exploration_type=ExplorationType.DepthFirst(),
                        search_type=SearchType.TreeSearch(),
                        is_solution_path=True,
                        max_depth=100,
                        max_moves=100,
                        max_runtime=100,
                        dot_filename=os.path.join(Constants.TEST_DATA_DIR, "invalid.dot"),
                        is_verbose=True)

    def test_initial_state_type_error(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        with self.assertRaises(TypeError):
            # Search
            self.search(explorer,
                        initial_state=list(),
                        goal_state=None,
                        exploration_type=ExplorationType.DepthFirst(),
                        search_type=SearchType.TreeSearch(),
                        is_solution_path=True,
                        max_depth=100,
                        max_moves=100,
                        max_runtime=100,
                        dot_filename=os.path.join(Constants.TEST_DATA_DIR, "invalid.dot"),
                        is_verbose=True)

    def test_max_moves_0(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        with self.assertRaises(ValueError):
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
                        dot_filename=os.path.join(Constants.TEST_DATA_DIR, "invalid.dot"),
                        is_verbose=True)

    def test_depth_0(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        with self.assertRaises(ValueError):
            # Search
            self.search(explorer,
                        initial_state,
                        goal_state=None,
                        exploration_type=ExplorationType.DepthFirst(),
                        search_type=SearchType.TreeSearch(),
                        is_solution_path=True,
                        max_depth=0,
                        max_moves=100,
                        max_runtime=100,
                        dot_filename=os.path.join(Constants.TEST_DATA_DIR, "invalid.dot"),
                        is_verbose=True)

    def test_runtime_0(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x": [1, 2], "y": [10, 20], "z": [100, 200]})

        with self.assertRaises(ValueError):
            # Search
            self.search(explorer,
                        initial_state,
                        goal_state=None,
                        exploration_type=ExplorationType.DepthFirst(),
                        search_type=SearchType.TreeSearch(),
                        is_solution_path=True,
                        max_depth=100,
                        max_moves=100,
                        max_runtime=0,
                        dot_filename=os.path.join(Constants.TEST_DATA_DIR, "invalid.dot"),
                        is_verbose=True)