import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, MyState
from explorateur import Explorateur, ExplorationType, SearchType


class UsageExampleTest(BaseTest):

    def test_usage_example(self):

        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        initial_state = MyState({"x":[1,2], "y":[10, 20], "z":[100, 200]})

        # Search
        self.search(explorer,
                    initial_state,
                    goal_state=None,
                    exploration_type=ExplorationType.DepthFirst(),
                    search_type=SearchType.TreeSearch(),
                    is_solution_path=True,
                    max_depth=100,
                    max_moves=100,
                    max_runtime=100,
                    dot_filename=os.path.join(Constants.TEST_DATA_DIR, "usage_example.dot"),
                    is_verbose=True)

        self.assertEqual(explorer.num_decisions, 14)
        self.assertEqual(explorer.num_failed_decisions, 0)
