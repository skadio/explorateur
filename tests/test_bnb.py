import sys
import os

# Add the branch_and_bound example directory to the Python path
# so that the relative imports work
branch_and_bound_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'branch_and_bound')
sys.path.insert(0, os.path.abspath(branch_and_bound_dir))

try:
    from tests.test_base import BaseTest
    from examples.branch_and_bound.main import BranchAndBound
finally:
    # Clean up: remove the added path from sys.path
    if os.path.abspath(branch_and_bound_dir) in sys.path:
        sys.path.remove(os.path.abspath(branch_and_bound_dir))


class GraphDepthTest(BaseTest):
    def solve_and_assert(self, filepath):
        # Solve with branch and bound
        bnb_solver = BranchAndBound(filepath)
        bnb_result = bnb_solver.solve()

        # Solve with OR Tools directly on the same instance
        ortools_result = bnb_solver.lp_instance.solve(use_relaxation=False)
        
        # Assert
        if bnb_result != float("inf") and ortools_result[0] != float("inf"):
            self.assertAlmostEqual(bnb_result, ortools_result[0], places=5)

    def test_model1(self):
        # File
        model1_path = "examples/data/model1.mps"
        model2_path = "examples/data/model2.mps"

        # Solve and assert
        self.solve_and_assert(model1_path)
        self.solve_and_assert(model2_path)


