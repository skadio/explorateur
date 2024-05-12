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
