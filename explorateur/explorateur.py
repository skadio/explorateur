#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import NoReturn
from collections import deque
import numpy as np
import copy as cp



from explorateur.state.base_state import BaseState
from explorateur.utils import check_true, Constants
from explorateur.state.state_with_transition import TransitionState
from explorateur.search.transition import Transition

from enum import Enum

class SearchType(Enum):
    DepthFirst = 1
    BreadthFirst = 2
    BestFirst = 3

# class _StorageType(NamedTuple):
#     class Stack(NamedTuple):
#         param: Num = 0.05

#         def _validate(self):
#             check_true(isinstance(self.param, (int, float)), TypeError("param must be an integer or float."))

#     class Queue(NamedTuple):
#         param: Num = 1.0

#         def _validate(self):
#             check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

#     class Hash(NamedTuple):
#         param: Num = 1.0

#         def _validate(self):
#             check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

#     class PriorityQueue(NamedTuple):
#         param: Num = 1.0

#         def _validate(self):
#             check_true(0 < self.param, ValueError("The value of param must be greater than zero."))


# class ExplorationType(NamedTuple):
#     class DepthFirst(NamedTuple):
#         _storage_type: _StorageType = _StorageType.Stack

#         def _validate(self):
#             check_true(isinstance(self.param, (int, float)), TypeError("param must be an integer or float."))

#     class BestFirst(NamedTuple):
#         _storage_type: _StorageType = _StorageType.PriorityQueue

#         def _validate(self):
#             check_true(0 < self.param, ValueError("The value of param must be greater than zero."))

#     class BreadthFirst(NamedTuple):
#         param: Num = 1.0

#         def _validate(self):
#             check_true(0 < self.param, ValueError("The value of param must be greater than zero."))



class Explorateur:

    def __init__(self, exploration_type: SearchType, seed: int = Constants.default_seed):
        # Validate arguments
        # Explorateur._validate_args(seed)

        self.exploration_type = exploration_type


        # Save the arguments
        self.seed = seed

        # Create the random number generator
        self._rng = np.random.RandomState(seed=self.seed)

    def search(self, initial_state: BaseState, goal_state: BaseState = None) -> BaseState:

        states = deque(TransitionState)
        states.append(curr_transition_state)
        curr_transition_state = TransitionState(initial_state)
        curr_state = initial_state
        while states:
            if self.exploration_type == SearchType.DepthFirst:
                curr_transition_state = states.pop() 
            elif self.exploration_type == SearchType.BreadthFirst:
                curr_transition_state = states.popleft() 
            curr_state = curr_transition_state.base_state

            if curr_state.is_solution():
                return curr_state

            valid_moves = curr_state.get_valid_moves()
            
            for move in valid_moves:
                successor = cp.deepcopy(curr_state)
                if not move.execute(successor):
                    continue
                new_transition = Transition(curr_transition_state, move)
                new_transition_state = TransitionState(successor)
                new_transition_state.set_transition(new_transition)
                states.append(new_transition_state)
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
