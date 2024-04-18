# Explorateur

Explorateur is a library written in Python to solve problems that require some sort of search

Explorateur follows a scikit-learn style public interface, adheres to 
[PEP-8 standards](https://www.python.org/dev/peps/pep-0008/), and is tested heavily. 

Documentation is available at 
[github.io/XXX](https://github.io/XXX).

The user provide at least an initial state (inherited from BaseState) and one of the following in the constructor:
- Depth First Search: uses a stack to keep track of the states
- Breadth-First Search:  uses a queue to keep track of the states to be explored. 
- Best-First Search: this will utilize a Priority Queue but in order for this to work the ```objective_function()``` must be implemented in ```BaseState``` as a given state is inserted into the Priority Queue based on some objective evaluation of "goodness". 

There is also the option to use a Graph Search: in order for this to work, the user must change the ```is_terminate()``` function to check for equality between the current state and some goal state. Note, a simple "==" wil not suffice btu rather the user must ensure that each of the relevant attributes that define a state are equal. For example, in the following case we would check that ```val_to_vars``` is the same.

## Quick Start:

```python
# Example that will search for an assignment of values for a group of variables

# Imports from Explorateur
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


    def get_data(self) -> dict:
        return self.var_to_val

    def set_data(self) -> NoReturn:
        """
        """
        pass

    def execute(self, move: SimpleMove) -> bool:
        self.var_to_val[move.variable] = move.value  # don't need the absolute
        self.unassigned_variables.remove(move.variable)
        return True

    
    def objective_function(self):
        return 0.0
    
    def __str__(self) -> str:
        return str(self.var_to_val)

#setting up a simple search by Explorateur
    seed = random.randint(0, 100000)
    explorer = Explorateur(ExplorationType.DepthFirst(), self.seed)
    possible_vals = {1: [1,2], 2: [20,10], 3: [100,200]}
    starting_state = SimpleState(possible_vals)
    sol_state = explorer.search(starting_state)
```
Other parameters into the search that can be set bu do not have to are not needed: 


## Installation

XXX can be installed from the wheel file or building from source by following the instructions in 
our [documentation](https://github.io/XXX/installation.html).

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/XXX/issues).

## License

XXX is licensed under the [Apache License 2.0](LICENSE.md).

## Installation
xxx requires Python 3.6+ and can be installed from the provided wheel file.  

1) Clone the repository (you can discard folders other than fidtone)
2) Go to the fidtone directory
3) Install from the wheel file

```
$ git clone https://xxx   
$ cd xxx
$ pip install dist/xxx-X.X.X-py3-none-any.whl
```

The wheel file automatically installs `requirements.txt`, downloads and installs `en_core_web_lg` language model (~700 MB) from `spacy`, 
and downloads `punkt` tokenizer (~50 MB) from `nltk`.


## Running Unit Tests

```
$ cd fidtone
$ python -m unittest discover tests
```


## Changelog

| Date | Notes |
|--------|-------------|
| Jan 1, 2021 | Initial release |

<br>

```
xxx © Copyright, xxx
````

<br>