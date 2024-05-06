# Explorateur

Explorateur is a library written in Python to solve problems that require searching over a collection of states. The algorithm begins with an initial state then makes 'moves' until a stopping criteria is met (number of iterations, runtime, user-defined termination). Explorateur follows a scikit-learn style public interface, adheres to 
[PEP-8 standards](https://www.python.org/dev/peps/pep-0008/), and is tested heavily. 

This package allows a search to happen by implementing an instance of ```BaseMove``` and ```BaseState``` .

The user needs to provide at least an initial state (inherited from BaseState) and one of the following in the constructor:
- Depth First Search: uses a stack to keep track of the states
- Breadth-First Search: uses a queue to keep track of the states to be explored. 
- Best-First Search: uses a Priority Queue, which requires ```objective_function()``` to be implemented in ```BaseState``` as a given state is inserted into the Priority Queue based on the result of this function call. 

There is an example of each type of search in the file test_exploration_type. 

There is also the option to use a Graph Search: in order for this to work, the user must design the ```is_terminate()``` function to check for equality between the current state and some goal state. Note, a simple "==" wil not suffice but rather the user must ensure that each of the relevant attributes that define a state are equal. For example, in the following case we would check that ```val_to_vars``` is the same.

The algorithm stops once a solution is found based on ```is_terminate()```, or all possible states have been explored and no solution has been found or in the case that ```max_runtime``` or ```max_iters``` is defined if one of them are reached.

## Installation

Explorateur can be installed from terminal by doing:
bash
```
pip install explorateur
```

## Quick Start:

```python
# Example that will search for an assignment of values for a group of variables

# Imports from Explorateur
import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState

# Setting up Move class which implements BaseMove
class SimpleMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.value = variable_assignment
    
    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"

# Implementing the State class which implements BaseState
class SimpleState(BaseState):

    @override
    def __init__(self, possible_vals):
        self.var_to_val = {}
        self.possible_vals = possible_vals
        self.unassigned_variables = self.generate_vars()


    def generate_vars(self):
        # this function is not necessary for a child of BaseState
        variables = set()
        for v in self.possible_vals.keys():
            variables.add(v)
        return variables

    @override
    def get_moves(self) -> List[SimpleMove]:
        moves_list = []
        for var in self.unassigned_variables:
            for val in self.possible_vals[var]:
                moves_list.append(SimpleMove(var, val))
        return moves_list

    @override
    def is_terminate(self) -> bool:
        if len(self.unassigned_variables) > 0:
            return False
        return True

    @override
    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)
        return True

    def __str__(self) -> str:
        return str(self.var_to_val)

#setting up a simple search by Explorateur
def main():
    seed = random.randint(0, 100000)
    explorer = Explorateur(ExplorationType.DepthFirst(), seed)
    possible_vals = {1: [1,2], 2: [20,10], 3: [100,200]}
    starting_state = SimpleState(possible_vals)
    sol_state = explorer.search(starting_state)
```

The above example just searches for some assignment of variables 1,2,3 where the assignments happen to be those indicated by ```possible_vars```. In ```get_moves()``` we return moves that are "legal" by what is established in ```possible_vars```.


## Support

Please submit bug reports and feature requests as [Issues](https://github.com/explorateur/issues).

## License

Explorateur is licensed under the [Apache License 2.0](LICENSE.md).

## Unit Tests
This command will run **all the tests**.
```
$  python -m unittest discover
```

If you wish to run a specific test from a given test file please run the following commandf.
```
$ python -m unittest -v tests.<file_name>.<class_name>.<function_name>
```
So for example, we could do:
```
$ python -m unittest -v tests.test_exploration_type.ExplorationTypeTests.test_bfs_1
```
## Changelog

| Date | Notes |
|--------|-------------|
| l May, 2024 | Initial release |

<br>

```
Explorateur © Copyright, Explorateur
````

<br>