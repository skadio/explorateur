# -*- coding: utf-8 -*-


from typing import NoReturn
import copy as cp
import numpy as np
import graphviz
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

    def __init__(self, exploration_type: ExplorationType, seed: int = Constants.default_seed):
        # Validate arguments
        # Explorateur._validate_args(seed)

        self.exploration_type = exploration_type

        # Save the arguments
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.RandomState(seed=self.seed)
        
        self.tree = graphviz.Digraph()

    #stopping criteria
    def search(self, initial_state: BaseState, goal_state: Union[BaseState,None] = None, max_runtime = None, max_iters = None) -> _BaseState:
        counter = 0
        if initial_state is None:
            raise ValueError
        _initial_state = _BaseState(initial_state, str(0))
        self.tree.node(_initial_state.node_label)
        states: BaseStorage[_BaseState] = StorageFactory.create(
            self.exploration_type.storage_type)  # list of internal sta
        states.insert(_initial_state)

        iterations = 0
        start = time.time()
        while not states.is_empty() and iterations < max_iters:
            end = time.time()
            if end - start > max_runtime:
                return None
            iterations += 1
            _current = states.remove()
            logging.debug(f"Current State: {_current}")
            transition = _current.get_transition()
            if transition is not None:
                successful_move = _current.execute(transition.move)
                if not successful_move:
                    self.tree.node(_current.node_label, style='filled', fillcolor='red')
                    continue
                if _current.is_solution():
                    self.tree.node(_current.node_label, style='filled', fillcolor='green')
                    return _current
            moves = _current.get_moves()
            self.tree.node(_current.node_label, style='filled', fillcolor='blue')
            # TODO: DFS, reverse the moves so that when pushed to stack, move order preserved
            # not sure if this is necessary
            # if self.exploration_type == ExplorationType.DepthFirst:
            #     moves.reverse()
            for move in moves:
                counter += 1
                _successor = cp.deepcopy(_current)
                _successor.node_label = str(counter)
                self.tree.node(_successor.node_label)
                self.tree.edge(_current.node_label, _successor.node_label, label=str(move))
                new_transition = Transition(_current, move)
                _successor.set_transition(new_transition)
                states.insert(_successor)
                logging.debug(f"Added State: {_successor}")
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
        self.tree.render(file_path, format='png')

    #   for (int m = 0; m < moves.size(); m++)
    #       {
    #         IMove move = moves.get(m);
    #
    #         if(verbosity > 3)
    #           System.out.println("Apply move: " + move);
    #
    #         // Execute move on a copy since we maintain sets of states
    #         IState successor = state.copy();
    #
    #         // move failed, continue with remaining nodes
    #         if(!move.execute(successor))
    #         {
    #           if(verbosity > 3)
    #             System.out.println("Move failed!");
    #           continue;
    #         }
    #
    #         // In graph search, skip already visited state
    #         if(mSearchType.isGraphSearch() && closed.contains(successor))
    #         {
    #           continue;
    #         }
    #
    #         int depth = (trans == null)? 1 : trans.depth + 1;
    #
    #         // Record previous move for solution trace.
    #         successor.setTransition(new Transition(move, state, depth));
    #
    #         // if still within depth bound, add to the open set
    #         if (depth < mDepthBound)
    #         {
    #           open.insert(successor);
    #         }
    #       }

    #     mNumNodes = 0;
    #
    #     IStateCollection open = StateStorageFactory.create(mOpenStorageType);
    #     IStateCollection closed = (mSearchType.isGraphSearch())? StateStorageFactory.create(StorageType.HASH) : null;
    # #
    #     open.insert(initial.copy());
    #     while (!open.isEmpty())
    #     {
    #       mNumNodes++;
    #
    #       IState state = open.remove();
    #       if(mSearchType.isGraphSearch())
    #         closed.insert(state);
    #
    #       state.setID(String.valueOf(mNumNodes));
    #
    #       Transition trans = state.getTransition();
    #
    #       if(verbosity > 3)
    #         System.out.println("\nCurrent node: " + state.getID() +
    #                            " depth " + ((trans==null)? 0 : trans.depth) + "\n" + state);
    #
    #       if(verbosity == -1)
    #       {
    #         if(trans!=null)
    #         {
    #           dot.append(trans.prev.getID() + " -> " + state.getID() + " [label=\"" + trans.move +"\"]\n");
    #           dot.append(trans.prev.getID() + " [label=" + trans.prev.getLabel() + "]\n");
    #           dot.append(state.getID() + " [label=" + state.getLabel() + "]\n");
    #         }
    #       }
    #
    #       if (state.isSolution(goal))
    #       {
    #         if(verbosity == -1)
    #           dot.append(state.getID() + " [style=filled, fillcolor=green]\n");
    #
    #         // If solution, leave now,
    # 				if(verbosity > 0)
    # 					System.out.println("Solution found! Node: " + state.getID() + "\n" + toDotString());
    #         return new SearchPath(initial, state, true);
    #       }
    #
    #       // All successor moves translate into appended OPEN states.
    #       List<IMove> moves = state.getValidMoves();
    #
    #       // DFS, reverse the moves so that when pushed to stack, move order preserved
    #       if (mExplorationType.isDepthFirst())
    #         Collections.reverse(moves);
    #
    #       for (int m = 0; m < moves.size(); m++)
    #       {
    #         IMove move = moves.get(m);
    #
    #         if(verbosity > 3)
    #           System.out.println("Apply move: " + move);
    #
    #         // Execute move on a copy since we maintain sets of states
    #         IState successor = state.copy();
    #
    #         // move failed, continue with remaining nodes
    #         if(!move.execute(successor))
    #         {
    #           if(verbosity > 3)
    #             System.out.println("Move failed!");
    #           continue;
    #         }
    #
    #         // In graph search, skip already visited state
    #         if(mSearchType.isGraphSearch() && closed.contains(successor))
    #         {
    #           continue;
    #         }
    #
    #         int depth = (trans == null)? 1 : trans.depth + 1;
    #
    #         // Record previous move for solution trace.
    #         successor.setTransition(new Transition(move, state, depth));
    #
    #         // if still within depth bound, add to the open set
    #         if (depth < mDepthBound)
    #         {
    #           open.insert(successor);
    #         }
    #       }
    #     }
    #
    # 		if(verbosity > 0)
    # 			System.out.println("Search Finished\n " + toDotString());
    #     return new SearchPath(initial, goal, false);

    @staticmethod
    def _validate_args(seed) -> NoReturn:
        """
        Validates arguments for the constructor.
        """

        # Seed
        check_true(isinstance(seed, int), TypeError(
            "The seed must be an integer."))
