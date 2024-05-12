import copy as cp
import logging
import sys
import time
from typing import Optional, List, Tuple, Union

from pydot import Dot, Node, Edge

from explorateur._version import __version__
from explorateur.search.decision import Decision
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType
from explorateur.search.transition import Transition
from explorateur.state.base_state import BaseState
from explorateur.state.state import _State
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.state.storage.factory import StorageFactory
from explorateur.utils import check_true, All_Exploration_Types, All_Search_Types

__version__ = __version__


class Explorateur:
    """
    The Explorateur library is designed to search for solutions.

    The search starts from a given initial state (as in Tree Search),
    and optionally, toward a given goal state (as in Graph Search).

    The exploration strategy is controlled by the exploration type parameter.
    The exploration types include best-first, breadth-first, and depth-first search.

    Explorateur implements a generic search functionality that operates on custom defined state and move.
    The custom state inherits from BaseState and custom move inherits from BaseMove.

    NB: Best-first search requires the custom state to also implement an objective function
        to evaluate the quality of the state.
    """

    def __init__(self):
        """ Initialize an Explorateur object. """

        # TODO add logger

        # Validate arguments
        Explorateur._validate_args()

        # State collections open and closed (for graph search only)
        self._open_decisions: BaseStorage
        self._closed_decisions: Optional[BaseStorage] = None

        # Solution state and internal version with transition
        self.solution_state: Optional[BaseState] = None
        self._solution_state_: Optional[_State] = None

        # Dot graph representation of search
        self.dot_graph: Optional[Dot] = None

        # Statistics
        self._start_time: float = 0
        self.total_time: float = 0
        self.num_decisions: int = 0
        self.num_failed_decisions: int = 0

    def search(self,
               initial_state: BaseState,
               goal_state: Optional[BaseState] = None,
               exploration_type: All_Exploration_Types = ExplorationType.DepthFirst(),
               search_type: All_Search_Types = SearchType.TreeSearch(),
               is_solution_path: bool = True,
               max_depth: int = sys.maxsize,
               max_moves: int = sys.maxsize,
               max_runtime: int = None,
               dot_file_path: str = None) -> Union[BaseState, List[BaseState], None]:
        """
        This function performs search from the initial_state until:
            - a solution found, or
            - goal_state reached if given, or
            - termination criteria, in terms of number of seconds or iterations, is reached.

        Arguments:
            - initial_state (BaseState): The initial state where the search will begin.
            - goal_state Optional(BaseState): Optional argument used for graph search to reach termination state.
                                              Default, None.
            - exploration_type Optional(ExplorationType): The exploration method.
                                                          Default, ExplorationType.DepthFirst().
            - search_type Optional(SearchType): The search method to decide whether to store visited states.
                                                Default, SearchType.TreeSearch().
            - is_solution_path (bool): If True, the path starting from the solution state back to the initial_state is returned.
                                       If False, the solution state is returned.
                                       Default, True.
            - max_depth Optional(int): Optional argument for the maximum depth to stop search.
                                       Default, maxsize (no limit).
            - max_moves Optional(int): Optional argument for the maximum number of moves to stop search.
                                       Default, maxsize (no limit).
            - max_runtime Optional(int): Optional argument for the number of seconds the search should go on for.
                                         Default, None (no limit).
            - dot_file_path (str): Optional argument to write a graph dot representation of search iterations.
                                   Default, None (no dot file saved).
                                   Example dot graph visualizer: https://dreampuf.github.io/GraphvizOnline/
        Returns:
            - If no solution found or the search hits one of the stopping criteria,
            returns None.
            - if a solution is found and is_solution_path is set to False,
            returns the solution state.
            - If a solution is found, and is_solution_path is set to True,
            returns a list of solution states, denoting the path starting from the solution state back to the initial_state.
        """

        self.start = time.perf_counter()
        logging.info(">>> START SEARCH ")

        # Check arguments
        Explorateur._validate_search_args(initial_state, goal_state,
                                          exploration_type, search_type, is_solution_path,
                                          max_depth, max_moves, max_runtime, dot_file_path)

        # Reset rng, solution_states, collections, dot graph, start time, stats
        self._reset_search(dot_file_path)

        # Create storage for open states, and optionally, for closed states in graph search to avoid duplicate visits
        self._open_decisions = StorageFactory.create(exploration_type)
        self._closed_decisions = StorageFactory.create(search_type)

        # Convert initial BaseState to internal _BaseState so that we can attach transitions
        initial_state = _State(initial_state)

        # Check termination, else expand current state with possible moves as open decisions for execution within depth
        is_terminate, is_solution = self._is_terminate_or_expand(initial_state, goal_state, exploration_type, max_depth, dot_file_path)
        if is_solution:
            return self._get_solution_path() if is_solution_path else self.solution_state
        if is_terminate:
            return None

        # START SEARCH
        while not self._open_decisions.is_empty():
            self.num_decisions += 1
            logging.info("\nDecision %s", self.num_decisions)
            logging.info("Open decisions: %s", self._open_decisions.size())

            # Check stopping conditions
            self._check_stopping_criteria(self._start_time, self.num_decisions, max_runtime, max_moves, dot_file_path)

            # Pop the current decision from open decisions for execution
            current_decision = self._open_decisions.remove()
            logging.info("Current decision: %s", current_decision)

            # Transition of the current state (there is no transition for initial moves)
            transition = current_decision.state_.transition
            next_depth = transition.depth + 1 if transition else 1
            logging.info("Current transition: %s", transition)

            # Mark the decision as visited, if graph search
            if self._closed_decisions:
                logging.info("Mark current decision as visited in closed decisions %s#", self._closed_decisions.size())
                self._closed_decisions.insert(current_decision)

            # Execute the move (important: current decision is already a copy version when added as search move)
            successor_ = cp.deepcopy(current_decision.state_)
            if successor_.execute(current_decision.move):
                logging.info("Move is successful.")

                # Set next depth and attach next transition to successor so that we can trace solution path
                next_transition = Transition(previous_state_=current_decision.state_, move=current_decision.move, depth=next_depth)
                logging.info("Create next transition %s ", next_transition)
                successor_.transition = next_transition

                if self.dot_graph:
                    from_node = Node(name=current_decision.state_.get_dot_label())
                    to_node = Node(name=successor_.get_dot_label())
                    # self.dot_graph.add_node(from_node)
                    # self.dot_graph.add_node(to_node)
                    edge_label = current_decision.move.get_dot_label()
                    self.dot_graph.add_edge(Edge(src=from_node, dst=to_node, label=edge_label))

                # Check termination, else expand current state with possible moves as open decisions for execution within depth
                is_terminate, is_solution = self._is_terminate_or_expand(successor_, goal_state, exploration_type, max_depth, dot_file_path)
                if is_solution:
                    return self._get_solution_path() if is_solution_path else self.solution_state
                if is_terminate:
                    return None
            else:
                self.num_failed_decisions += 1
                # Skip failed move and infeasible successor
                logging.info("Skip infeasible successor. Num fails: %s", str(self.num_failed_decisions))

                if self.dot_graph:
                    from_node = Node(name=current_decision.state_.get_dot_label())
                    fail_node = Node(self.num_decisions,
                                     label="Fail: " + str(self.num_failed_decisions), shape="triangle", style="filled", fillcolor="red")
                    # self.dot_graph.add_node(from_node)
                    self.dot_graph.add_node(fail_node)
                    edge_label = current_decision.move.get_dot_label()
                    self.dot_graph.add_edge(Edge(src=from_node, dst=fail_node, label=edge_label))

        # No more open decisions left, search finished, save the dot
        self.total_time = time.perf_counter() - self._start_time
        self._log_stats("<<< FINISH SEARCH - FAILURE - No solution! ")
        if self.dot_graph: self.dot_graph.write(dot_file_path)
        return None

    def _is_terminate_or_expand(self, state_, goal_state, exploration_type, max_depth, dot_file_path) -> Tuple[bool, bool]:

        is_terminate, is_solution = False, False

        # Check termination condition -- decided by the user state!
        if state_.is_terminate(goal_state):
            is_terminate, is_solution = True, True
            self._solution_state_ = state_
            self.solution_state = state_.base
            self.total_time = time.perf_counter() - self._start_time
            logging.info("Successful termination for state: " + str(state_))
            self._log_stats("<<< FINISH SEARCH - SUCCESS - Solution Found!")
            if self.dot_graph:
                # Recolor final node with green
                self.dot_graph.add_node(Node(state_.get_dot_label(), style="filled", fillcolor="green"))
                self.dot_graph.write(dot_file_path)
            return is_terminate, is_solution
        else:
            logging.info("No termination, continue with alternative moves")

        # If still within max depth bound, insert the successor into open states for exploration
        # Initial state does not have transition, so skip max depth for initial state
        if state_.transition:
            if state_.transition.depth > max_depth:
                # Don't terminate the whole search, but don't generate new open nodes
                logging.info("Max depth reached, not inserting new open node.")
                return is_terminate, is_solution

        # If no termination, add alternative moves to search -- decided by the user state!
        moves = state_.get_moves()

        # Reverse moves for depth first search, so the exploration follows user move order
        if isinstance(exploration_type, ExplorationType.DepthFirst):
            moves.reverse()

        # Search for alternatives
        for move in moves:
            logging.info("Decision from move: %s", move)

            # Create new decision
            decision = Decision(state_, move)

            # Skip already visited successor, if graph search
            if self._closed_decisions and self._closed_decisions.contains(decision):
                logging.info("Skip adding already visited successor.")
                continue

            # Push successor to open storage for execution
            logging.info("Add open decision for execution %s", decision)
            self._open_decisions.insert(decision)

        return is_terminate, is_solution

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
        if self._solution_state_:
            # Start the path from the solution state, and walk backwards
            self._get_path_helper(self._solution_state_, state_list)

        return state_list.reverse() if is_initial_first else state_list

    def _get_path_helper(self, state_: _State, state_list: list):
        """
        This helper recursion traces back explored states explored in reverse order.

        Parameters:
            _state (_State): The current state being explored.
            state_list (list): The list to store the explored states.

        Returns:
            list: The list of explored states in reverse order.
        """
        transition = state_.transition

        # We reached the initial state, add it and return the path
        if transition is None:
            state_list.append(state_.base)
            return state_list

        # Otherwise, append the base user state to the state list
        state_list.append(state_.base)

        # Continue recursion from the previous internal state
        self._get_path_helper(transition.previous_state_, state_list)

    def _reset_search(self, dot_file_path):
        # Clean state collections
        self._open_decisions = None
        self._closed_decisions = None

        # Clean solution states
        self.solution_state = None
        self._solution_state_ = None

        # Dot graph representation of search, if dot file given
        self.dot_graph = Dot(graph_type="digraph", splines="line") if dot_file_path else None

        # Initialize counters
        self._start_time = time.perf_counter()
        self.total_time = 0
        self.num_decisions = 0
        self.num_failed_decisions = 0

    def _check_stopping_criteria(self, start, num_moves, max_runtime, max_moves, dot_file_path):
        stop_cause = ""

        # Check stopping criteria: max_runtime
        current_time = time.perf_counter()
        if max_runtime is not None and current_time - start > max_runtime:
            stop_cause = "Max runtime reached"

        # Check stopping criteria: max_moves
        if num_moves > max_moves:
            stop_cause = "Max number of moves reached"

        # If stopped, log, save dot, and return None solution
        if stop_cause:
            self.total_time = current_time - start
            self._log_stats("<<< FINISH SEARCH - STOP - No solution! " + stop_cause)
            if self.dot_graph: self.dot_graph.write(dot_file_path)
            return None

    def _log_stats(self, info):
        logging.info(info +
                     "\nTotal Decisions: " + str(self.num_decisions) +
                     "\nTotal Failures: " + str(self.num_failed_decisions) +
                     "\nTotal Time: " + str(round(self.total_time,3)))

    @staticmethod
    def _validate_args() -> None:
        pass

    @staticmethod
    def _validate_search_args(initial_state, goal_state,
                              exploration_type, search_type, is_solution_path,
                              max_depth, max_iterations, max_runtime, dot_file_path) -> None:

        check_true(initial_state is not None, TypeError("Initial state cannot be none."))
        check_true(isinstance(initial_state, BaseState),
                   TypeError("Initial state must be BaseState type. Incorrect type: " + str(type(goal_state))))

        if goal_state is not None:
            check_true(isinstance(goal_state, BaseState),
                       TypeError("Goal state must be BaseState type. Incorrect type: " + str(type(goal_state))))

        check_true(isinstance(exploration_type, All_Exploration_Types),
                   TypeError("Exploration type is not allowed " + str(exploration_type)))

        check_true(isinstance(search_type, All_Search_Types),
                   TypeError("Search type is not allowed " + str(search_type)))

        check_true(isinstance(is_solution_path, bool),
                   TypeError("is_solution_path must be boolean " + str(is_solution_path)))

        check_true(isinstance(max_depth, int),
                   TypeError("max_depth must be integer number of seconds. Incorrect: " + str(max_depth)))

        check_true(max_depth > 0,
                   TypeError("max_depth must be positive. Incorrect: " + str(max_depth)))

        check_true(isinstance(max_iterations, int),
                   TypeError("max_iterations must be integer number of seconds. Incorrect: " + str(max_iterations)))

        check_true(max_iterations > 0,
                   TypeError("max_iterations must be positive. Incorrect: " + str(max_iterations)))

        if max_runtime is not None:
            check_true(isinstance(max_runtime, int),
                       TypeError("max_runtime must be integer number of seconds. Incorrect: " + str(max_runtime)))
            check_true(max_runtime > 0,
                       TypeError("max_runtime must be positive. Incorrect: " + str(max_runtime)))

        if dot_file_path is not None:
            check_true(isinstance(dot_file_path, str),
                       TypeError("dot_file_path must be a string. Incorrect type: " + str(type(dot_file_path))))
