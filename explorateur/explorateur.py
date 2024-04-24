# -*- coding: utf-8 -*-


from typing import NoReturn
import copy as cp
import numpy as np
import pydot
import logging
import time

from explorateur.state.base_state import BaseState
from explorateur.utils import check_true, Constants
from explorateur.state._base_state import _BaseState
from explorateur.search.transition import Transition
from explorateur.state.storage.factory import StorageFactory
from explorateur.state.storage.base_storage import BaseStorage
from explorateur.search.exploration_type import ExplorationType

from typing import Union


class Explorateur:

    def __init__(self, exploration_type: ExplorationType, seed: int = Constants.default_seed):
        # Explorateur._validate_args(seed)
        """
        Initializes an Explorateur object with:
        Args:
            exploration_type (ExplorationType): needs to specify the type of search (ExplorationType.BreadthFirst(), ExplorationType.DepthFirst(), ExplorationType.BestFirst())
            seed (int) = seed for the randomness
        """

        self.exploration_type = exploration_type

        # Save the arguments
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.RandomState(seed=self.seed)

        #internal variables to be used later in determining whether or not the user wants to build a tree during the search
        self.tree = None
        self.build_tree = False
        self._solution_state = None

    # should we specify max run_time in seconds
    def search(self, start_state: BaseState, end_state: BaseState = None, max_runtime=None, max_iterations=None, file_path=None) -> _BaseState:
        """
        This function carries out the search starting at start_state until either a solution is found or it has to terminate.s
        Args:
            start_state (BaseState): initial state where the search will begin
            end_state (BaseState, None): optional argument but needed for graph search to know where to terminate the search
            max_runtime (int): optional arg for number of seconds the search should go on for
            max_iterations (int): optional arg for maximum number of nodes that can be explored before termianting the search if no solution has been found yet
            file_path (str): optional arg that can be None but if it is a string a tree will be written while doing the exploration and written to the file in the filepath provided
        Returns:
            None if no solution state has been found or if it was a Best-First search ; solution state otherwise.
        """
        
        if file_path is not None:
            self.tree = pydot.Dot(graph_type="digraph")
            self.build_tree = True
        counter = 0
        if start_state is None:
            raise ValueError
        _start_state = _BaseState(start_state, str(0))
        if self.build_tree:
            _start_state.node = pydot.Node(_start_state.node_label)
            self.tree.add_node(_start_state.node)
        states: BaseStorage[_BaseState] = StorageFactory.create(
            self.exploration_type.storage_type)  # list of internal sta
        states.insert(_start_state)

        iterations = 0
        if max_iterations is None:
            # if not max_iterations provided by the user we set it to infinity
            max_iterations = float('inf')
        start = time.time()
        while not states.is_empty() and iterations < max_iterations:
            # print(f"Iteration: {iterations}")
            # print(f"States Size: {states.get_size()}")
            end = time.time()
            if max_runtime is not None:
                if end - start > max_runtime:
                    self.visualize_tree(file_path)
                    return None
            iterations += 1
            # logging.debug(states)
            _current = states.remove()
            # logging.debug(f"Current State: {_current}")
            transition = _current.get_transition()
            if transition is not None:
                # logging.debug(_current.objective_function())
                # logging.debug(transition.move)
                successful_move = _current.is_valid()
                if not successful_move:
                    if self.build_tree:
                        _current.node = pydot.Node(
                            _current.node_label, style='filled', fillcolor='red')
                        self.tree.add_node(_current.node)
                    continue
                if _current.is_terminate(end_state):
                    if self.build_tree:
                        _current.node = pydot.Node(
                            _current.node_label, style='filled', fillcolor='green')
                        self.tree.add_node(_current.node)
                        self.visualize_tree(file_path)
                    #if it is a best-first search we do not want to return upon the first solution but care more
                    # about the order nodes are epxlored in 
                    if isinstance(self.exploration_type, ExplorationType.BestFirst):
                        continue
                    else:
                        # return _current
                        self._solution_state = _current
                        return _current.user_state
            moves = _current.get_moves()
            # print(f"Current State: {_current}")
            # print(f"Moves: {moves}")
            if self.build_tree:
                _current.node = pydot.Node(
                    _current.node_label, style='filled', fillcolor='blue')
                self.tree.add_node(_current.node)
            for move in moves:
                counter += 1
                _successor = cp.deepcopy(_current)
                if self.build_tree:
                    _successor.node_label = _successor.make_node_label(counter)
                    _successor.node = pydot.Node(_successor.node_label)
                    self.tree.add_node(_successor.node)
                    self.tree.add_edge(pydot.Edge(
                        _current.node, _successor.node, label=str(move)))
                new_transition = Transition(_current, move)
                _successor.set_transition(new_transition)
                _successor.execute(new_transition.move) #executing the move so that the states actually reflect the potential changes 
                states.insert(_successor)
                # logging.debug(f"Added State: {_successor}")
        if self.build_tree:
            self.visualize_tree(file_path)
        return None

    def print_path(self, path: _BaseState):
        # get_transitions, just return list of transitions
        # add parameter for reversing this list
        transition = path.get_transition()
        if transition is None:
            print("Begin Path")
            print("State:", path)
            return
        self.print_path(transition.previous_state)
        print("State:", path)
        print("Move:", transition.move)
    
    def get_path(self,  reverse = False):
        """
        This function will return a list of the states  so they can see the order in which the search was done.
        Args:
            reverse(Boolean): indicate whether or not the user wishes for the list to be reversed, right now the list
            will have the end state at the beginning and go backwards
        """
        state_list = []
        #we pass in self._solution_state as the _BaseState form where to start our search, we can only trace a path if a solution
        #has been set
        self.get_path_helper(self._solution_state, state_list)
        if reverse:
            return state_list.reverse()
        return state_list
    
    def get_path_helper(self,state: _BaseState, state_list: list):
        """
        This helper function for get_path() traces back the states that were explored in reverse order (starting at the end)
        """
        if state is None:
            raise ValueError
        transition = state.get_transition()
        if transition is None: #we are at the beginning state
            return state_list
        state_list.append(state)
        self.get_path_helper(transition.previous_state, state_list)

    def visualize_tree(self, file_path):
        """
        This function writes the tree that has been constructed during the searach (if desired) to the file in the file path provided.
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
