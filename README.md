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

## Quick Start:

```python
from typing import List
from explorateur.explorateur import Explorateur
from explorateur.search.exploration_type import ExplorationType
from explorateur.state.base_move import BaseMove
from explorateur.state.base_state import BaseState


# Create your custom move
class SimpleMove(BaseMove):

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def get_dot_edge_label(self) -> str:
        return str(self.variable) + "->" + str(self.value)

    def __str__(self) -> str:
        return f"Setting variable: {self.variable} to {self.value}"


# Create your custom state representation
class SimpleState(BaseState):

    def __init__(self, var_to_domain):
        self.var_to_domain = var_to_domain

        self.var_to_value = {}
        self.unassigned_vars = set(var_to_domain.keys())

    def get_moves(self) -> List[SimpleMove]:
        moves = []
        for var in self.unassigned_vars:
            for val in self.var_to_domain[var]:
                moves.append(SimpleMove(var, val))
        return moves

    def is_terminate(self, end_state=None) -> bool:
        if len(self.unassigned_vars) > 0:
            return False
        return True

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_value[move.variable] = move.value
        self.unassigned_vars.remove(move.variable)
        return True

    def get_state_label(self, iterations: int):
        return str(iterations)

    def __str__(self) -> str:
        return str(self.var_to_value)


# Explorateur with choice of exploration
explorer = Explorateur(ExplorationType.DepthFirst())

# Initial state with variables and their possible domains 
initial_state = SimpleState({"x": [1, 2], "y": [20, 10], "z": [100, 200]})

# Find a solution via search 
solution = explorer.search(initial_state)
print(solution)
```

The above example just searches for some assignment of variables 1,2,3 where the assignments happen to be those indicated by ```possible_vars```. In ```get_moves()``` we return moves that are "legal" by what is established in ```possible_vars```.


## Install from PyPI

Explorateur can be installed from PyPI using `pip install explorateur`

## Install from Source
Alternatively, you can build a wheel package on your platform from scratch using the source code:

```bash
git clone https://github.com/skadio/explorateur.git
cd explorateur
pip install setuptools wheel # if wheel is not installed
python setup.py sdist bdist_wheel
pip install dist/explorateur-X.X.X-py3-none-any.whl
```

## Test your setup 
This command will run **all the tests**.
```
$  cd explorateur
$  python -m unittest discover tests
```

To run a specific test from a given test file:
```
$ python -m unittest -v tests.<file_name>.<class_name>.<function_name>
```

For example: 
```
$ python -m unittest -v tests.test_exploration_type.ExplorationTypeTests.test_bfs_1
```

## Changelog

| Date         | Notes           |
|--------------|-----------------|
| 15 May, 2024 | Initial release |

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/explorateur/issues).

## License

Explorateur is licensed under the [Apache License 2.0](LICENSE.md).

<br>
