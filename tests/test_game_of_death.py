from typing import Dict, List
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType
import os
from explorateur.utils import Constants

from tests.test_base import BaseTest, matrix_to_str
from explorateur import Explorateur, ExplorationType, SearchType
from explorateur.utils import run


class MyMove(BaseMove):

    # Define move object
    def __init__(self, kill_cells):
        self.kill_cells = kill_cells

    # String representation, also used for edge labels in DOT graph
    def __str__(self) -> str:
        return "Kill cells " + str(self.kill_cells)


class MyState(BaseState):
    EMPTY = "| |"
    ALIVE = "A"
    DEAD = "X"
    DIRECTIONS = [[0, 1],   # cell on the right
                  [0, -1],  # cell on the left
                  [1, 0],   # cell on the bottom
                  [-1, 0]]  # cell on the above

    # Problem specific state representation
    def __init__(self, grid: List[List[str]]):
        # IMPORTANT: Make sure to initialize the base state
        super().__init__()
        self.grid = grid
        self.num_alive = 0

        # Count the number of alive cells
        self.Rows = range(len(grid))
        self.Cols = range(len(grid[0]))
        for r in self.Rows:
            for c in self.Cols:
                if grid[r][c] is self.ALIVE:
                    self.num_alive += 1

    # Design branching decisions
    def get_moves(self) -> List[MyMove]:
        kill_moves = []

        # Find all the cells to kill.
        # This MUST be a set to avoid inserting duplicates
        kill_cells = set()
        for r in self.Rows:
            for c in self.Cols:
                # If r, c is dead
                if self.grid[r][c] == self.DEAD:
                    # Look around r,c
                    for dr, dc in self.DIRECTIONS:
                        # neighbor cell
                        row, col = r + dr, c + dc

                        # if neighbor exists and is alive, then must die
                        if row in self.Rows and col in self.Cols and self.grid[row][col] == self.ALIVE:
                            kill_cells.add((row, col))
        if kill_cells:
            kill_moves.append(MyMove(kill_cells))

        # Unary branching (next state is current state + kill cells)
        print("User Moves: ", kill_moves)
        return kill_moves

    # Execute the move on the state, return success flag
    def execute(self, move: MyMove) -> bool:
        print("USER Execute:", move)

        if move.kill_cells:
            # kill all the given cells in the move
            for cell in move.kill_cells:
                row, col = cell[0], cell[1]
                self.grid[row][col] = self.DEAD
                self.num_alive -= 1
            print("USER Execute: SUCCESS ", self.grid)
            return True
        else:
            print("USER Execute: FAIL ", self.grid)
            return False

    # Check whether a state is the solution/termination
    def is_terminate(self, goal_state=None) -> bool:
        return self.num_alive == 0

    # String representation, also used for node labels in DOT graph
    def __str__(self) -> str:
        text = "ID: " + str(self.id) + "\n"
        text += matrix_to_str(self.grid) + "\n"
        text += "ALIVE: " + str(self.num_alive) + "\n"
        return text


class GODTest(BaseTest):

    # https://neetcode.io/problems/rotting-fruit
    def test_game_of_death(self):
        # Explorateur
        explorer = Explorateur(is_verbose=True)

        # Initial state
        # Don't search the whole tree, stop at first feasible
        # Fake a few failing decisions
        initial_state = MyState(grid=[[MyState.ALIVE, MyState.ALIVE, MyState.EMPTY],
                                      [MyState.EMPTY, MyState.ALIVE, MyState.ALIVE],
                                      [MyState.EMPTY, MyState.ALIVE, MyState.DEAD]])

        # Arguments
        args = {}
        args["initial_state"] = initial_state
        args["goal_state"] = None
        args["exploration_type"] = ExplorationType.BreadthFirst()
        args["search_type"] = SearchType.TreeSearch()
        args["is_solution_path"] = True
        args["max_depth"] = 100
        args["max_moves"] = 100
        args["max_runtime"] = 100
        args["dot_filename"] = os.path.join(Constants.TEST_DATA_DIR, "tree_god.dot")
        args["is_verbose"] = True

        # Run
        run(explorer, args)

        # # Solution label
        # ground_truth_solution = {"x": 1, "y": 10, "z": 100}
        # self.assertEqual(explorer.num_decisions, 3)
        # self.assertEqual(explorer.num_failed_decisions, 0)
        # self.assertEqual(len(explorer.solution_path), 4)
        # self.assertEqual(explorer.solution_path[-1], initial_state)
        # self.assertEqual(explorer.solution_state.var_to_val, ground_truth_solution)
        # self.assertEqual(explorer.solution_state.unassigned, [])
