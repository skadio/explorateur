import os
from typing import Dict, Union, NamedTuple
from explorateur.search.exploration_type import ExplorationType
from explorateur.search.search_type import SearchType


Num = Union[int, float]
"""Num type is defined as integer or float."""

All_Exploration_Types = Union[ExplorationType.BestFirst, ExplorationType.BreadthFirst, ExplorationType.DepthFirst]
"""All possible exploration types"""

All_Search_Types = Union[SearchType.GraphSearch, SearchType.TreeSearch]
"""All possible search types"""


class Constants(NamedTuple):
    """
    Constant values used by the modules.
    """

    default_seed = 123456
    """The default random seed."""

    # Folder names
    _TEST_DIR_NAME = "tests"
    _DATA_DIR_NAME = "data"

    # Data paths
    _FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_DATA_DIR = _FILE_DIR + os.sep + ".." + os.sep + _TEST_DIR_NAME + os.sep + _DATA_DIR_NAME

    SUCCESS_NODE_COLOR = "green"
    FAIL_NODE_COLOR = "red"
    LIMIT_NODE_COLOR = "purple"


def run(explorer, args):

    # Search for solutions
    if explorer.search(initial_state=args["initial_state"],
                       goal_state=args["goal_state"],
                       exploration_type=args["exploration_type"],
                       search_type=args["search_type"],
                       is_solution_path=args["is_solution_path"],
                       max_depth=args["max_depth"],
                       max_moves=args["max_moves"],
                       max_runtime=args["max_runtime"],
                       dot_filename=args["dot_filename"]):

        if args["is_verbose"]:
            print("Solution:", explorer.solution_state)
            print("Solution Path:", *explorer.solution_path, sep="\n<-")
    else:
        if args["is_verbose"]:
            print("No solution found!")

    if args["is_verbose"]:
        # Search statistics
        print("Total Decisions:", explorer.num_decisions)
        print("Total Failures:", explorer.num_failed_decisions)
        print("Total Time:", round(explorer.total_time, 3))


def argmax(dictionary: Dict[Num, Num]) -> Num:
    """
    Returns the first key with the maximum value.
    """
    return max(dictionary, key=dictionary.get)


def check_false(expression: bool, exception: Exception) -> None:
    """
    Checks that given expression is false, otherwise raises the given exception.
    """
    if expression:
        raise exception


def check_true(expression: bool, exception: Exception) -> None:
    """
    Checks that given expression is true, otherwise raises the given exception.
    """
    if not expression:
        raise exception


def reset(dictionary: Dict, value) -> None:
    """
    Maps every key to the given value.
    """
    dictionary.update({}.fromkeys(dictionary, value))
