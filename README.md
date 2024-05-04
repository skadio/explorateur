# Explorateur

Explorateur is a library written in Python to solve problems that require searching over a collection of states. 

Explorateur follows a scikit-learn style public interface, adheres to 
[PEP-8 standards](https://www.python.org/dev/peps/pep-0008/), and is tested heavily. 


The user provide at least an initial state (inherited from BaseState) and one of the following in the constructor:
- Depth First Search: uses a stack to keep track of the states
- Breadth-First Search:  uses a queue to keep track of the states to be explored. 
- Best-First Search: this will utilize a Priority Queue but in order for this to work the ```objective_function()``` must be implemented in ```BaseState``` as a given state is inserted into the Priority Queue based on some objective evaluation of "goodness". 

There is also the option to use a Graph Search: in order for this to work, the user must change the ```is_terminate()``` function to check for equality between the current state and some goal state. Note, a simple "==" wil not suffice but rather the user must ensure that each of the relevant attributes that define a state are equal. For example, in the following case we would check that ```val_to_vars``` is the same.

The algorithm stops once a solution is found based on ```is_terminate()```, or all possible states have been explored and no solution has been found or in the case that ```max_runtime``` or ```max_iters``` is defined if one of them are reached.

## Installation

Explorateur can be installed from terminal by doing:
bash
```
pip install explorateur
```
After which please install the requirements by doing
bash
```
pip install -r requirements.txt
```

## Quick Start:

```python
# Example that will search for an assignment of values for a group of variables

# Imports from Explorateur
import random
from tests.test_base import BaseTest
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType

from typing import List, NoReturn
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState

# Setting up Move class which implements BaseMove
class SimpleMove(BaseMove):

    def __init__(self, variable, variable_assignment):
        self.variable = variable
        self.value = variable_assignment
    
    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"

# Implementing the State class which implements Base Move
class SimpleState(BaseState):

    def __init__(self, possible_vals):
        self.var_to_val = {}
        self.possible_vals = possible_vals
        self.unassigned_variables = self.generate_vars(self.possible_vals)

    def generate_vars(self, clauses):
        variables = set()
        for v in self.possible_vals.keys():
            variables.add(v)
        return variables

    def get_moves(self) -> List[SimpleMove]:
        """
        """
        moves_list = []
        for var in self.unassigned_variables:
            for val in self.possible_vals[var]:
                moves_list.append(SimpleMove(var, val))
        return moves_list

    def is_terminate(self) -> bool:
        """
        """
        if len(self.unassigned_variables) > 0:
            return False
        return True

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)
        return True

    
    def objective_function(self):
        return 0.0
    
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
```
$ cd fidtone
$ python -m unittest discover tests
```


## Changelog

| Date | Notes |
|--------|-------------|
| April 1, 2024 | Initial release |

<br>

```
Explorateur © Copyright, Explorateur
````

<br>