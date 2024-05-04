''' Module for the Explorateur class, used to perform search. '''

import time
import logging
import sys
import copy as cp
from typing import NoReturn, Union, List
import numpy as np
import pydot

from explorateur.state.base_state import BaseState
from explorateur.utils import check_true, Constants
from explorateur.state._base_state import _BaseState
from explorateur.search.transition import Transition
from explorateur.state.storage.factory import StorageFactory
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.search.exploration_type import ExplorationType


class Explorateur:
    """ Explorateur class, used to perform search. """

    def __init__(self, exploration_type: Union = [ExplorationType.BestFirst(), ExplorationType.DepthFirst(),
                                                  ExplorationType.BreadthFirst()], seed: int = Constants.default_seed):
        """
        Initializes an Explorateur object.

        Args: exploration_type (ExplorationType): Specifies the type of search (ExplorationType.BreadthFirst(),
        ExplorationType.DepthFirst(), ExplorationType.BestFirst()). seed (int): Seed for the randomness.

        Attributes:
            exploration_type (ExplorationType): The type of search being performed.
            seed (int): The seed used for randomness.
            _rng (numpy.random.RandomState): Random number generator.
            tree (None or Tree): The tree structure used during the search.
            _solution_state (None or State): The solution state found during the search.
        """

        Explorateur._validate_args(seed)

        self.exploration_type = exploration_type
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.default_rng(seed=self.seed)

        # Internal variables to be used later in determining whether or not the user wants to build a tree during the
        # search
        self.tree = None
        self._solution_state = None

    def search(self, start_state: BaseState, end_state: BaseState = None, max_runtime: int = None,
               max_iterations: int = sys.maxsize, file_path: str = None) -> BaseState:
        """
        This function carries out the search starting at start_state until either a solution is found or it has to
        terminate.

        - Args: start_state (BaseState): The initial state where the search will begin.
        - end_state (BaseState,None): Optional argument but needed for graph search to know where to terminate the
          search.
        - max_runtime (int): Optional argument for the number of seconds the search should go on for.
        - max_iterations (int): Optional argument for the maximum number of nodes that can be explored before
          terminating the search if no solution has been found yet.
        - file_path (str): Optional argument that can be None, but if it is a string, a tree will be written while
          doing the exploration and written to the file in the filepath provided.

        Returns:
            None if no solution state has been found or if it was a Best-First search; solution state otherwise.
        """

        # validate start state
        if start_state is None:
            raise ValueError

        # construct the start state as a _BaseState object
        _start_state = _BaseState(start_state, str(0))

        # if the user wants to build a tree, we initialize the tree
        if file_path is not None:
            self.tree = pydot.Dot(graph_type="digraph")
            _start_state.node = pydot.Node(_start_state.node_label)
            self.tree.add_node(_start_state.node)

        # initialize the states storage
        states: BaseStorage[_BaseState] = StorageFactory.create(self.exploration_type.storage_type)
        states.insert(_start_state)

        # initialize the counter and iterations, start the timer
        counter = 0
        iterations = 0
        start = time.time()

        while not states.is_empty() and iterations < max_iterations:
            logging.debug("Iteration: %s", iterations)
            logging.debug("States Size: %s", states.get_size())

            # check if the search has been running for too long
            end = time.time()
            if max_runtime is not None:
                if end - start > max_runtime:
                    self.visualize_tree(file_path)
                    return None

            # pop the current state from the storage
            iterations += 1
            _current = states.remove()
            transition = _current.get_transition()
            logging.debug("Current State: %s", _current)

            # if not a start state, check if the move is valid
            if transition is not None:
                successful_move = _current.is_valid()
                logging.debug("State: %s, Move: %s, Valid: %s", _current, transition.move, successful_move)
                # if the move is not valid, we do not want to explore the state further, color it red
                if not successful_move:
                    if self.tree:
                        _current.node = pydot.Node(
                            _current.node_label, style='filled', fillcolor='red')
                        self.tree.add_node(_current.node)
                    continue
                # if the move is valid, we need to check if the state is a termination state
                if _current.is_terminate(end_state):
                    if self.tree:
                        _current.node = pydot.Node(
                            _current.node_label, style='filled', fillcolor='green')
                        self.tree.add_node(_current.node)
                        self.visualize_tree(file_path)
                    if isinstance(self.exploration_type, ExplorationType.BestFirst):
                        # if a best-first search, we want to keep exploring
                        continue
                    # if not a best-first search, we have found the solution state
                    self._solution_state = _current
                    return _current.user_state

            # if not a termination state, we need to explore the move from this state
            moves = _current.get_moves()

            if self.tree:
                # if the state has moves
                _current.node = pydot.Node(_current.node_label, style='filled', fillcolor='blue')
                self.tree.add_node(_current.node)
            for move in moves:
                counter += 1
                logging.debug("Move: %s, Counter: %d", move, counter)

                # create a new state to execute the move on
                _successor = cp.deepcopy(_current)

                if self.tree:
                    # add the successor to the tree
                    _successor.node_label = _successor.make_node_label(counter)
                    _successor.node = pydot.Node(_successor.node_label)
                    self.tree.add_node(_successor.node)
                    self.tree.add_edge(pydot.Edge(_current.node, _successor.node, label=str(move)))

                # create a new transition (to track path) and execute the move
                new_transition = Transition(_current, move)
                _successor.set_transition(new_transition)
                _successor.execute(new_transition.move)

                # insert the new state into the storage
                states.insert(_successor)
        if self.tree:
            # if the search has terminated, we want to visualize the tree
            self.visualize_tree(file_path)
        return None

    def get_path(self, reverse=False) -> List[BaseState]:
        """
        Returns a list of states representing the order in which the search was performed.

        Args:
            reverse (bool): Indicates whether or not the user wants the list to be reversed.
                By default, the list will have the end state at the beginning and go backwards.

        Returns:
            List[BaseState]: A list of BaseState objects representing the search path.

        """
        state_list = []
        # We pass in self._solution_state as the starting point for our search.
        # We can only trace a path if a solution has been set.
        self.get_path_helper(self._solution_state, state_list)

        if reverse:
            return state_list.reverse()

        return state_list

    def get_path_helper(self, state: _BaseState, state_list: list):
        """
        This helper function for get_path() traces back the states that were explored in reverse order (starting at
        the end).

        Parameters:
            state (_BaseState): The current state being explored.
            state_list (list): The list to store the explored states.

        Returns:
            list: The list of explored states in reverse order.
        """
        if state is None:
            raise ValueError
        transition = state.get_transition()
        if transition is None:
            # We are at the beginning state
            return state_list
        state_list.append(state.user_state)
        self.get_path_helper(transition.previous_state, state_list)

    def visualize_tree(self, file_path) -> NoReturn:
        """
        Writes the constructed tree to a file.

        This method writes the tree that has been constructed during the search to the file specified by the
        `file_path` parameter.

        Parameters:
        - file_path (str): The path of the file to write the tree to.
        """
        self.tree.write(file_path)

    @staticmethod
    def _validate_args(seed) -> NoReturn:
        """
        Validates arguments for the constructor.
        """

        # Seed
        check_true(isinstance(seed, int), TypeError(
            "The seed must be an integer."))
