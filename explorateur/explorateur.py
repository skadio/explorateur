import copy as cp
import time
from typing import Optional, List, Tuple

from explorateur._version import __version__
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from explorateur.search.transition import Transition
from explorateur.state.base_state import BaseState
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.storage.factory import StorageFactory
from explorateur.utils import check_true, All_Exploration_Types, All_Search_Types, Constants

__version__ = __version__


class Explorateur:
    """
        Explorateur is a Python library to conduct State-Space-Search (SSS).
        SSS is a powerful framework for solving problems that require search over a collection of states.

        Explorateur performs generic state-space-search over problem-specific states and moves.
        The user defines the `BaseState` and `BaseMove` and the library drives the search for solutions.

        Given an initial user state, Explorateur performs iterative search moves until a stopping condition is reached:
            - A termination state is found
            - The search space is exhausted
            - Reached max iterations, runtime limit, max depth
            - Optionally, given a goal state, a goal state is encountered.

        The behavior of the overall algorithm is controlled by the Search Strategy and the Exploration Strategy.

        Search Strategy:
            - TreeSearch over open states
            - GraphSearch over open states while also storing the closed states to avoid visiting duplicates.

        Exploration Strategy:
            - BreadthFirst in uninformed fashion
            - DepthFirst in uninformed fashion
            - BestFirst in informed fashion assuming an objective function evaluates the solution quality of a state.

        To use Explorateur, you need to define BaseState and BaseMove, as in the quick start template.
    """

    def __init__(self, is_verbose=False):
        """ Initialize an Explorateur object. """

        # Validate arguments
        Explorateur._validate_args(is_verbose)

        # Set verbosity
        self.is_verbose: bool = is_verbose

        self._log("[Explorateur v." + str(__version__) + "]")

        # Solution state
        self.solution_state: Optional[BaseState] = None
        self.solution_path: Optional[List[BaseState]] = None

        # State collections open and closed (for graph search only)
        self._open: BaseStorage = None
        self.closed: Optional[BaseStorage] = None

        # Statistics
        self._start_time: float = 0
        self.total_time: float = 0
        self.num_decisions: int = 0
        self.num_failed_decisions: int = 0

        # Dot graph text representation of search
        self._dot_text: str = ""
        self._dot_filename: str = ""

    def search(self,
               initial_state: BaseState,
               goal_state: Optional[BaseState] = None,
               exploration_type: All_Exploration_Types = ExplorationType.DepthFirst(),
               search_type: All_Search_Types = SearchType.TreeSearch(),
               is_solution_path: bool = True,
               max_depth: int = 100,
               max_moves: int = 10000,
               max_runtime: int = None,
               dot_filename: str = None) -> bool:
        """
        This function performs search from the initial_state until:
            - a solution found, or
            - goal_state reached if given, or
            - stopping criteria, in terms of number of seconds, iterations, or depth, is reached.

        Arguments:
            - initial_state (BaseState): The initial state where the search will begin.
            - goal_state Optional(BaseState): Optional argument used for graph search to reach termination state.
                                              Default, None.
            - exploration_type Optional(ExplorationType): The exploration method.
                                                          Default, ExplorationType.DepthFirst().
            - search_type Optional(SearchType): The search method to decide whether to store visited states.
                                                Default, SearchType.TreeSearch().
            - is_solution_path (bool): If True, path starting from solution state back to initial_state is returned.
                                       If False, solution state is returned.
                                       Default, True.
            - max_depth Optional(int): Optional argument for the maximum depth to stop search.
                                       Default, 100.
            - max_moves Optional(int): Optional argument for the maximum number of moves to stop search.
                                       Default, 10,000 moves.
            - max_runtime Optional(int): Optional argument for the number of seconds the search should go on for.
                                         Default, None (no limit).
            - dot_file_path (str): Optional argument to write a graph dot representation of search iterations.
                                   It uses logging CRITICAL level to log the dot output
                                   Default, None (no dot file saved).
                                   Example dot graph visualizer: https://dreampuf.github.io/GraphvizOnline/
        Returns:
            - If no solution found or the search hits one of the stopping criteria, returns False.
            - if a solution is found and is_solution_path is set to False, returns the solution state.
            - If a solution is found, and is_solution_path is set to True, returns a list of solution states,
                denoting the path from solution state back to the initial_state.
        """

        # Check arguments
        self._log_start(">>> START SEARCH", max_depth, max_moves, max_runtime)
        Explorateur._validate_search_args(initial_state, goal_state,
                                          exploration_type, search_type, is_solution_path,
                                          max_depth, max_moves, max_runtime, dot_filename)

        # Reset rng, solution_states, collections, dot graph, start time, stats
        self._reset_search(dot_filename)

        # Create storage for open states, and optionally, for closed states in graph search to avoid duplicate visits
        self._open = StorageFactory.create(exploration_type)
        self.closed = StorageFactory.create(search_type)

        # Root node root from the given initial state
        root = cp.deepcopy(initial_state)
        root.id = self.num_decisions

        # Check termination, else expand current state with possible moves
        # as open decisions for execution within depth
        is_terminate, is_solution = self._is_terminate_or_expand(root, goal_state, exploration_type, max_depth)
        if is_solution:
            if is_solution_path:
                self.solution_path = self._get_solution_path()
            return True
        if is_terminate:
            return False

        # START SEARCH
        while not self._open.is_empty():
            self.num_decisions += 1
            self._log("\nDecision " + str(self.num_decisions))
            self._log("Open decisions: " + str(self._open.size()))

            # Pop the copied successor state from open for execution
            successor = self._open.remove()
            current = successor._transition.previous_state
            move = successor._transition.move
            self._log("Current decision: " + str(current))

            # Transition of the current state (there is no transition for initial moves)
            self._log("Current transition: " + str(current._transition))

            # Execute the move on a copy state
            if successor.execute(move):
                self._log("Move is successful.")

                successor.id = self.num_decisions - self.num_failed_decisions
                self._log("Create next transition: " + str(successor._transition) +
                          " from ID: " + str(current.id) + " to ID: " + str(successor.id))

                # Mark the decision as visited, if graph search
                if self.closed:
                    self._log("Mark current decision as visited in closed decisions: " + str(self.closed.size()))
                    self.closed.insert(current)

                # Skip already visited successor, if graph search
                if self.closed and self.closed.contains(successor):
                    self._log("Skip adding decision. It is already visited. " + str(successor))
                    self.num_decisions -= 1
                else:
                    # Create dot node transition
                    self._log_dot(current, move, successor, color="")

                    # Check termination, else expand successor state with possible moves for execution within depth
                    is_terminate, is_solution = self._is_terminate_or_expand(successor, goal_state, exploration_type, max_depth)
                    if is_solution:
                        if is_solution_path:
                            self.solution_path = self._get_solution_path()
                        return True
                    if is_terminate:
                        return False
            else:
                # Skip failed move and infeasible successor, reset failed transition
                successor._transition = None
                self.num_failed_decisions += 1
                self._log("Skip infeasible successor. Num fails: " + str(self.num_failed_decisions))

                # Create dot node transition to a failed node
                self._log_dot(current, move, None, color=Constants.FAIL_NODE_COLOR)

            # Check stopping conditions before next iteration. If hits a limit, color last successor state
            if self._is_search_limit(successor, self._start_time, self.num_decisions, max_runtime, max_moves):
                return False

        # No more open decisions left or limit reach and search finished, save the dot and return False
        self.total_time = time.perf_counter() - self._start_time
        self._log_finish("<<< FINISH SEARCH - FAILURE - No solution! ")
        self._log_dot_file()
        return False

    def _is_terminate_or_expand(self, state, goal_state, exploration_type, max_depth) -> Tuple[bool, bool]:

        is_terminate, is_solution = False, False

        # Check termination condition -- decided by the user state!
        if state.is_terminate(goal_state):
            is_terminate, is_solution = True, True
            self.solution_state = state
            self.total_time = time.perf_counter() - self._start_time
            self._log("Successful termination for state: " + str(state))
            self._log_finish("<<< FINISH SEARCH - SUCCESS - Solution Found!")
            move = state._transition.move if state._transition else None
            self._log_dot(None, move, state, color=Constants.SUCCESS_NODE_COLOR)  # mark it green
            self._log_dot_file()
            return is_terminate, is_solution
        else:
            self._log("Successor is not termination, add alternative moves")

        # If still within max depth bound, insert the successor into open states for exploration
        # Initial state does not have transition, so skip max depth for initial state
        if state._transition:
            if state._transition.depth >= max_depth:
                # Don't terminate the whole search, but don't generate new open nodes
                self._log("Max depth reached, not inserting new open node.")
                self._log_dot(None, state._transition.move, state, color=Constants.LIMIT_NODE_COLOR)
                return is_terminate, is_solution

        # If no termination, add alternative moves to search -- decided by the user state!
        moves = state.get_moves()

        # Reverse moves for depth first search, so the exploration follows user move order
        if isinstance(exploration_type, ExplorationType.DepthFirst):
            moves.reverse()

        # Search for alternatives
        for move in moves:
            self._log("Decision for move: " + str(move))

            # Create a copy successor with next transition
            successor_state = cp.deepcopy(state)
            transition = state._transition
            next_depth = transition.depth + 1 if transition else 1
            next_transition = Transition(previous_state=state, move=move, depth=next_depth)
            successor_state._transition = next_transition

            # Push successor to open storage for execution
            self._log("Add open decision for executing " + str(successor_state._transition.move) + " on state\n" + str(state))
            self._open.insert(successor_state)

        return is_terminate, is_solution

    def _is_search_limit(self, state, start, num_moves, max_runtime, max_moves):
        # Check max_runtime
        stop_cause = None
        current_time = time.perf_counter()
        if max_runtime is not None and current_time - start > max_runtime:
            stop_cause = "Max runtime reached " + str(max_runtime)

        # Check max_moves
        if num_moves >= max_moves:
            stop_cause = "Max number of moves reached " + str(max_moves)

        # If stopped, log, save dot, and return None solution
        if stop_cause:
            self.total_time = current_time - start
            self._log_finish("<<< FINISH SEARCH - STOP - No solution! " + stop_cause)
            self._log_dot(None, state._transition.move, state, color=Constants.LIMIT_NODE_COLOR)  # mark it green
            self._log_dot_file()
            return True
        return False

    def _get_solution_path(self, is_initial_first=False) -> List[BaseState]:
        """
        Returns a list of states representing the order in which the search was performed.

        Args:
            - is_initial_first (bool): Indicates whether to reverse the path (list of states)
            so that the initial state is the first of the list.
            By default, the list has the solution state as the first element of the list
            and traces backwards to the initial state as the last element of the list.

        Returns:
            List[BaseState]: A list of BaseState objects representing the search path.

        """
        # TODO convert recursion to iteration
        state_list = []

        # We can only trace a path if a solution state is found
        if self.solution_state:
            # Start the path from the solution state, and walk backwards
            self._get_path_helper(self.solution_state, state_list)

        return state_list.reverse() if is_initial_first else state_list

    def _get_path_helper(self, state: BaseState, state_list: list):
        """
        This helper recursion traces back explored states explored in reverse order.

        Parameters:
            state (_State): The current state being explored.
            state_list (list): The list to store the explored states.

        Returns:
            list: The list of explored states in reverse order.
        """
        transition = state._transition

        # We reached the initial state, add it and return the path
        if transition is None:
            state_list.append(state)
            return state_list

        # Otherwise, append the base user state to the state list
        state_list.append(state)

        # Continue recursion from the previous internal state
        self._get_path_helper(transition.previous_state, state_list)

    def _log(self, text):
        if self.is_verbose:
            print(text)

    def _log_dot(self, current, move, successor, color):
        if not self._dot_filename:
            return

        if current:
            # If there is no successor, first add a fail node with color so that we can add an edge to it
            if not successor:
                self._dot_text += (str(self.num_decisions) +
                                   " [label=\"Fail: " + str(self.num_failed_decisions) + "\"" +
                                   " shape=triangle style=filled fillcolor="+ str(color) + "];\n")

            # generic nodes with no color
            self._dot_text += "\"" + current.get_dot_label() + "\" -> "
            self._dot_text += "\"" + successor.get_dot_label() + "\"" if successor else str(self.num_decisions)
            self._dot_text += " [label=\"" + move.get_dot_label() + "\"];\n"
        else:
            # decision is taken care of, mark successor with the color
            self._dot_text += "\"" + successor.get_dot_label() + "\" [style=filled fillcolor=" + str(color) + "];\n"

    def _log_dot_file(self):
        if self._dot_filename:
            self._dot_text += "}"
            with open(self._dot_filename, 'w') as dot_file:
                dot_file.write(self._dot_text)

    def _log_start(self, info, max_depth, max_moves, max_runtime):
        self._log("\n" + info +
                  "\nMax Depth: " + str(max_depth) +
                  "\nMax Moves: " + str(max_moves) +
                  "\nMax Time: " + str(max_runtime) + "\n")

    def _log_finish(self, info):
        self._log("\n" + info +
                  "\nTotal Decisions: " + str(self.num_decisions) +
                  "\nTotal Failures: " + str(self.num_failed_decisions) +
                  "\nTotal Time: " + str(round(self.total_time, 3)) + "\n")

    def _reset_search(self, dot_filename):

        # Clean solution states
        self.solution_state = None
        self.solution_path = None

        # Clean state collections
        self._open = None
        self.closed = None

        # Initialize counters
        self._start_time = time.perf_counter()
        self.total_time = 0
        self.num_decisions = 0
        self.num_failed_decisions = 0

        # Dot graph text representation of search, used if dot file given
        self._dot_text = "digraph G {\nspline=line;\n"
        self._dot_filename = dot_filename

    @staticmethod
    def _validate_args(is_verbose) -> None:
        check_true(isinstance(is_verbose, bool),
                   TypeError("is_verbose must be boolean " + str(is_verbose)))

    @staticmethod
    def _validate_search_args(initial_state, goal_state,
                              exploration_type, search_type, is_solution_path,
                              max_depth, max_moves, max_runtime, dot_file_path) -> None:

        check_true(initial_state is not None, ValueError("Initial state cannot be none."))
        check_true(isinstance(initial_state, BaseState),
                   TypeError("Initial state must be BaseState type. Incorrect type: " + str(type(goal_state))))

        if goal_state is not None:
            check_true(isinstance(goal_state, BaseState),
                       TypeError("Goal state must be BaseState type. Incorrect type: " + str(type(goal_state))))

        # Turning off as generic types lead to an error (Python issue)
        # check_true(isinstance(exploration_type, All_Exploration_Types),
        #            TypeError("Exploration type is not allowed " + str(exploration_type)))

        # check_true(isinstance(search_type, All_Search_Types),
        #            TypeError("Search type is not allowed " + str(search_type)))

        check_true(isinstance(is_solution_path, bool),
                   TypeError("is_solution_path must be boolean " + str(is_solution_path)))

        check_true(isinstance(max_depth, int),
                   TypeError("max_depth must be integer number of seconds. Incorrect: " + str(max_depth)))

        check_true(max_depth > 0,
                   ValueError("max_depth must be positive. Incorrect: " + str(max_depth)))

        check_true(isinstance(max_moves, int),
                   TypeError("max_iterations must be integer number of seconds. Incorrect: " + str(max_moves)))

        check_true(max_moves > 0,
                   ValueError("max_moves must be positive. Incorrect: " + str(max_moves)))

        if max_runtime is not None:
            check_true(isinstance(max_runtime, int),
                       TypeError("max_runtime must be integer number of seconds. Incorrect: " + str(max_runtime)))
            check_true(max_runtime > 0,
                       ValueError("max_runtime must be positive. Incorrect: " + str(max_runtime)))

        if dot_file_path is not None:
            check_true(isinstance(dot_file_path, str),
                       TypeError("dot_file_path must be a string. Incorrect type: " + str(type(dot_file_path))))
