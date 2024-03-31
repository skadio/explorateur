# -*- coding: utf-8 -*-


from typing import NoReturn, NamedTuple
import numpy as np
import copy as cp

from explorateur.state.base_state import BaseState
from explorateur.utils import check_true, Constants
from explorateur.state._base_state import _BaseState
from explorateur.search.transition import Transition, TransitionState
from explorateur.state.storage.factory import StorageFactory
from explorateur.state.storage.base_storage import BaseStorage


class _StorageType(NamedTuple):
    class Stack(NamedTuple):
        """Stack type"""
        param: float = 0.05

        def _validate(self):
            check_true(isinstance(self.param, (int, float)),
                       TypeError("param must be an integer or float."))

    class Queue(NamedTuple):
        """Queue type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

    class Hash(NamedTuple):
        """Hash type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

    class PriorityQueue(NamedTuple):
        """PQ type"""
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

class ExplorationType(NamedTuple):
    """Exploration Type"""
    class DepthFirst(NamedTuple):
        "DepthFirst Type"
        _storage_type: _StorageType = _StorageType.Stack
        param: float = 1.0

        def _validate(self):
            check_true(isinstance(self.param, (int, float)),
                       TypeError("param must be an integer or float."))

    class BestFirst(NamedTuple):
        "BestFirst Type"
        _storage_type: _StorageType = _StorageType.PriorityQueue
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

    class BreadthFirst(NamedTuple):
        "BreadthFirst Type"
        _storage_type: _StorageType = _StorageType.Queue
        param: float = 1.0

        def _validate(self):
            check_true(0 < self.param, ValueError("The value of param must be greater than zero."))



#USE: PEP-8
class Explorateur:

    def __init__(self, exploration_type: ExplorationType, seed: int = Constants.default_seed):
        # Validate arguments
        # Explorateur._validate_args(seed)

        self.exploration_type = exploration_type


        # Save the arguments
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.RandomState(seed=self.seed)

    def search(self, initial_state: BaseState, goal_state: BaseState = None) -> BaseState:

        _initial_state = _BaseState(initial_state)
        states: BaseStorage[_BaseState] = StorageFactory.create(self.exploration_type._storage_type) #list of internal sta
        states.insert(_initial_state)
        while states:
            _current = states.remove()
            if _current.is_solution():
                return _current.is_solution()

            valid_moves = _current.user_state.get_valid_moves()

            # print("curr_state", curr_state.get_data())
            
            #note -- this is not a binary search
            for move in valid_moves:
                _successor = cp.deepcopy(_current)
                if not _successor.user_state.execute(move):
                    continue
                new_transition = Transition(_current, move)
                _successor.set_transition(new_transition)
                states.append(_successor)
        return None

                

            

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
        check_true(isinstance(seed, int), TypeError("The seed must be an integer."))
