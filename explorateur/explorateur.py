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

# USE: PEP-8


class Explorateur:

    def __init__(self, exploration_type: ExplorationType, seed: int = Constants.default_seed, build_tree = False):
        # Validate arguments
        # Explorateur._validate_args(seed)

        self.exploration_type = exploration_type

        # Save the arguments
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.RandomState(seed=self.seed)

        self.build_tree = build_tree
        if self.build_tree: 
            self.tree = pydot.Dot(graph_type="digraph")

    #stopping criteria
    def search(self, initial_state: BaseState, max_runtime = None, max_iters = None) -> _BaseState:

        counter = 0
        if initial_state is None:
            raise ValueError
        _initial_state = _BaseState(initial_state, str(0))
        if self.build_tree:
            _initial_state.node = pydot.Node(_initial_state.node_label)
            self.tree.add_node(_initial_state.node)
        states: BaseStorage[_BaseState] = StorageFactory.create(
            self.exploration_type.storage_type)  # list of internal sta
        states.insert(_initial_state)

        iterations = 0
        if max_iters is None:
            max_iters = float('inf')
        start = time.time()
        while not states.is_empty() and iterations < max_iters:
            end = time.time()
            if max_runtime is not None:
                if end - start > max_runtime:
                    return None
            iterations += 1
            _current = states.remove()
            # logging.debug(f"Current State: {_current}")
            transition = _current.get_transition()
            if transition is not None:
                successful_move = _current.execute(transition.move)
                if not successful_move:
                    if self.build_tree:
                        _current.node = pydot.Node(_current.node_label, style='filled', fillcolor='red')
                        self.tree.add_node(_current.node)
                    continue
                if _current.is_terminate():
                    if self.build_tree:
                        _current.node = pydot.Node(_current.node_label, style='filled', fillcolor='green')
                        self.tree.add_node(_current.node)
                    return _current
            moves = _current.get_moves()
            if self.build_tree:
                _current.node = pydot.Node(_current.node_label, style='filled', fillcolor='blue')
                self.tree.add_node(_current.node)
            for move in moves:
                counter += 1
                _successor = cp.deepcopy(_current)
                if self.build_tree:
                    _successor.node_label = str(counter)
                    _successor.node = pydot.Node(_successor.node_label)
                    self.tree.add_node(_successor.node)
                    self.tree.add_edge(pydot.Edge(_current.node, _successor.node, label=str(move)))
                new_transition = Transition(_current, move)
                _successor.set_transition(new_transition)
                states.insert(_successor)
                # logging.debug(f"Added State: {_successor}")
        return None
    
    def print_path(self, path: _BaseState):
        transition = path.get_transition()
        if transition is None:
            print("Begin Path")
            print("State:", path)
            return
        self.print_path(transition.previous_state) 
        print("State:", path)
        print("Move:", transition.move)
    
    def visualize_tree(self, file_path):
        print("Visualizing Tree")
        self.tree.write(file_path)

    @staticmethod
    def _validate_args(seed) -> NoReturn:
        """
        Validates arguments for the constructor.
        """

        # Seed
        check_true(isinstance(seed, int), TypeError(
            "The seed must be an integer."))
