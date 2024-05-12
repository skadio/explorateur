import copy as cp
import logging
import sys
import time
from typing import Optional, List

import numpy as np
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
from explorateur.utils import check_true, Constants, All_Exploration_Types, All_Search_Types

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

    def __init__(self, seed: int = Constants.default_seed):
        """
        Initialize an Explorateur object.

        Arguments:
            - exploration_type (ExplorationType): Specifies the type of search such as
            ExplorationType.BestFirst(), ExplorationType.BreadthFirst(), ExplorationType.DepthFirst()
            - seed (int): Seed to control randomness.

        Attributes:
            - seed (int): The seed used for randomness.
            - _rng (numpy.random.RandomState): Random number generator.
            - tree (Tree or None): The tree structure used during the search.
            - _solution_state (State or None): The solution state found during the search.
        """

        # TODO add logger

        # Validate arguments
        Explorateur._validate_args(seed)

        # Set seed
        self.seed: int = seed

        # Create the random number generator with given seed
        self._rng = np.random.default_rng(seed=self.seed)

        # State collections open and closed (for graph search only)
        self.open_decisions: BaseStorage
        self.closed_decisions: Optional[BaseStorage] = None

        # Solution state
        self._solution_state: Optional[_State] = None

        # Dot graph representation of search
        self.dot_graph: Optional[Dot] = None
        self.dot_file_path: Optional[str] = None

        # Statistics
        self.start_time: float = 0
        self.total_time: float = 0
        self.num_decisions: int = 0
        self.num_failed_decisions: int = 0

    def search(self,
               initial_state: BaseState,
               goal_state: Optional[BaseState] = None,
               exploration_type: All_Exploration_Types = ExplorationType.DepthFirst(),
               search_type: All_Search_Types = SearchType.TreeSearch(),
               max_depth: int = sys.maxsize,
               max_moves: int = sys.maxsize,
               max_runtime: int = None,
               dot_file_path: str = None) -> Optional[BaseState]:
        """
        This function performs search from the initial_state until:
            - a solution found, or
            - goal_state reached if given, or
            - termination criteria, in terms of number of seconds or iterations, is reached.

        Arguments:
            - initial_state (BaseState): The initial state where the search will begin.
            - goal_state Optional(BaseState): Optional argument used for graph search to reach termination state.
                                              By default, none.
            - max_runtime Optional(int): Optional argument for the number of seconds the search should go on for.
                                         By default, none (no limit).
            - max_moves Optional(int): Optional argument for the maximum number of moves to stop search.
                                       By default, maxsize (no limit).
            - max_depth Optional(int): Optional argument for the maximum depth to stop search.
                                       By default, maxsize (no limit).
            - search_type Optional(SearchType): The search method to decide whether to store visited states.
                                                By default, SearchType.TreeSearch().
            - exploration_type Optional(ExplorationType): The exploration method.
                                                          By default, ExplorationType.DepthFirst().
            - dot_file_path (str): Optional argument to write a graph dot representation of search iterations.
                                   By default, none (no dot file saved).
        Returns:
            Solution state if a solution found, None if no solution exists or hit stopping criteria.
        """

        logging.info(">>> START SEARCH ")

        # Check arguments
        Explorateur._validate_search_args(initial_state, goal_state,
                                          exploration_type, search_type,
                                          max_depth, max_moves, max_runtime, dot_file_path)

        # Reset rng, _solution_state, dot graph, counters, time
        self._reset_search(dot_file_path)

        # Create storage for open states, and optionally, for closed states in graph search to avoid duplicate visits
        self.open_decisions = StorageFactory.create(exploration_type)
        self.closed_decisions = StorageFactory.create(search_type)

        # Convert initial BaseState to internal _BaseState so that we can attach transitions
        initial_state_ = _State(initial_state)
        current_decision = cp.deepcopy(Decision(initial_state_, move=None))

        # Check termination, else expand current state with possible moves as open decisions for execution within depth
        self._terminate_or_expand(current_decision, goal_state, exploration_type, max_depth, dot_file_path)

        # START SEARCH
        while not self.open_decisions.is_empty():
            self.num_decisions += 1
            logging.info("\nDecision %s", self.num_decisions)
            logging.info("\nOpen states size: %s", self.open_decisions.size())

            # Check stopping conditions
            self._check_stopping_criteria(self.start_time, self.num_decisions, max_runtime, max_moves, dot_file_path)

            # Pop the current decision from open decisions for execution
            current_decision = self.open_decisions.remove()
            logging.info("Current decision: %s", current_decision)

            # Add to the dot graph
            if self.dot_graph: self._add_dot(current_decision)

            # Transition of the current state (there is no transition for initial moves)
            transition = current_decision.state_.transition
            logging.info("Current transition: %s", transition)

            # Mark the decision as visited, if graph search
            if self.closed_decisions:
                logging.info("Mark current decision as visited in closed decisions %s#", self.closed_decisions.size())
                self.closed_decisions.insert(current_decision)

            # Execute the move (important: current decision is already a copy version when added as search move)
            if current_decision.state_.execute(current_decision.move):
                logging.info("Move is successful.")

                # Set next depth and attach next transition to successor so that we can trace solution path
                next_depth = transition.depth + 1 if transition else 1
                next_transition = Transition(previous_state_=current_decision.state_, move=current_decision.move, depth=next_depth)
                logging.info("Create next transition %s ", next_transition)
                current_decision.state_.transition = next_transition

                # Check termination, else expand current state with possible moves as open decisions for execution within depth
                self._terminate_or_expand(current_decision, goal_state, exploration_type, max_depth, dot_file_path)
            else:
                # Skip failed move and infeasible successor
                logging.info("Skip infeasible successor.")

        # No more open decisions left, search finished, save the dot
        self.total_time = time.perf_counter() - self.start_time
        self._log_stats("<<< FINISH SEARCH - FAILURE - No solution! ")
        if self.dot_graph: self.dot_graph.write(dot_file_path)
        return None

    def _terminate_or_expand(self, current_decision, goal_state, exploration_type, max_depth, dot_file_path):

        # Check termination condition -- decided by the user state!
        if current_decision.state_.is_terminate(goal_state):
            self.total_time = time.perf_counter() - self.start_time
            logging.info("Successful termination for state: " + str(current_decision))
            self._log_stats("<<< FINISH SEARCH - SUCCESS - Solution Found!")
            if self.dot_graph:
                # Remark this node with green color to indicate solution state
                self.dot_graph.add_node(Node(str(current_decision), fillcolor="green"))
                self.dot_graph.write(dot_file_path)

            # Return user state on termination
            return current_decision.state_.base
        else:
            logging.info("Continue with alternate moves, not a termination state")

        # If still within max depth bound, insert the successor into open states for exploration
        if current_decision.state_.transition.depth > max_depth:
            logging.info("Max depth reached, not inserting new open node.")
            return

        # If not a termination state, add alternative moves to search -- decided by the user state!
        moves = current_decision.state_.get_moves()

        # Reverse moves for depth first search, so the exploration follows user move order
        if isinstance(exploration_type, ExplorationType.DepthFirst):
            moves.reverse()

        # Search for alternatives
        for move in moves:
            logging.info("Adding move ", move)

            # Create a copy state_ with this move
            successor_ = cp.deepcopy(current_decision)
            successor_.move = move

            # Skip already visited successor, if graph search
            if self.closed_decisions and self.closed_decisions.contains(successor_):
                logging.info("Skip adding already visited successor.")
                continue

            # Push successor to open storage for execution
            logging.info("Add successor for execution")
            self.open_decisions.insert(successor_)

    def get_path(self, reverse=False) -> List[BaseState]:
        """
        Returns a list of states representing the order in which the search was performed.

        Args:
            - reverse (bool): Indicates whether to reverse the path (list of states).
            By default, the list will have the end state at the beginning and trace backwards.

        Returns:
            List[BaseState]: A list of BaseState objects representing the search path.

        """
        state_list = []

        # We can only trace a path if a solution state is found
        if self._solution_state:
            # Start the path from the solution state, and walk backwards
            self._get_path_helper(self._solution_state, state_list)

        return state_list.reverse() if reverse else state_list

    def _get_path_helper(self, _state: _State, state_list: list):
        """
        This helper recursion traces back explored states explored in reverse order.

        Parameters:
            _state (_State): The current state being explored.
            state_list (list): The list to store the explored states.

        Returns:
            list: The list of explored states in reverse order.
        """
        transition = _state.get_transition()

        # We reached the initial state, return the collected list
        if transition is None:
            return state_list

        # Otherwise, append the base user state to the state list
        state_list.append(_state.base)

        # Continue recursion from the previous internal state
        self._get_path_helper(transition.previous_state_, state_list)

    def _reset_search(self, dot_file_path):
        # Create the random number generator with given seed
        self._rng = np.random.default_rng(seed=self.seed)

        # Solution state
        self._solution_state = None

        # Clean state collections
        self.open_decisions = None
        self.closed_decisions = None

        # Dot graph representation of search, if dot file given
        self.dot_graph = Dot(graph_type="digraph", rankdir="LR", splines="line") if dot_file_path else None

        # Initialize counters
        self.num_decisions = 0
        self.num_failed_decisions = 0
        self.start_time: time.perf_counter()

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

    def _add_dot(self, current_decision):
        previous = current_decision.state_.transition.previous_state_
        current = current_decision.state_
        move = current_decision.state_.transition.move
        depth = current_decision.state_.transition.depth
        self._add_dot_node(previous, self.num_decisions, depth)
        self._add_dot_node(current, self.num_decisions, depth)
        self._add_dot_edge(previous, move, current, self.num_decisions, depth)

    def _add_dot_node(self, _state, num_moves, depth, style: str = None, fillcolor: str = None):

        # Add the dot node label to the _state. The node label comes from user defined base state.
        _state.dot_node_label = _state.get_dot_label(num_moves, depth)

        # Add the dot node to the _state
        _state.dot_node = Node(_state.dot_node_label)
        if style:
            _state.dot_node = Node(_state.dot_node_label, style=style, fillcolor=fillcolor)

        # Add the dot note to the graph
        self.dot_graph.add_node(_state.dot_node)

    def _add_dot_edge(self, current_, move, successor_, num_moves, depth):
        edge_label = move.get_dot_label(num_moves, depth)
        edge = Edge(current_.dot_node, successor_.dot_node, label=edge_label)
        self.dot_graph.add_edge(edge)

    def _log_stats(self, info):
        logging.info(info +
                     "\nTotal Decisions: " + str(self.num_decisions) +
                     "\nTotal Failures: " + str(self.num_failed_decisions) +
                     "\nTotal Time: " + str(self.total_time))

    @staticmethod
    def _validate_args(seed: int) -> None:
        """
        Validates arguments for the constructor.
        """

        # Check integer seed
        check_true(isinstance(seed, int), TypeError("The seed must be an integer."))

    @staticmethod
    def _validate_search_args(initial_state, goal_state,
                              exploration_type, search_type,
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

        check_true(isinstance(max_depth, int),
                   TypeError("Max iterations must be integer number of seconds. Incorrect: " + str(max_iterations)))

        check_true(max_iterations > 0,
                   TypeError("Max iterations must be positive. Incorrect: " + str(max_iterations)))

        check_true(isinstance(max_iterations, int),
                   TypeError("Max iterations must be integer number of seconds. Incorrect: " + str(max_iterations)))

        check_true(max_iterations > 0,
                   TypeError("Max iterations must be positive. Incorrect: " + str(max_iterations)))

        if max_runtime is not None:
            check_true(isinstance(max_runtime, int),
                       TypeError("Max runtime must be integer number of seconds. Incorrect: " + str(max_runtime)))
            check_true(max_runtime > 0,
                       TypeError("Max runtime must be positive. Incorrect: " + str(max_runtime)))

        if dot_file_path is not None:
            check_true(isinstance(dot_file_path, str),
                       TypeError("dot_file_path must be a string. Incorrect type: " + str(type(dot_file_path))))
