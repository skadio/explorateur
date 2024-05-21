[![PyPI version fury.io](https://badge.fury.io/py/explorateur.svg)](https://pypi.python.org/pypi/explorateur/) [![PyPI license](https://img.shields.io/pypi/l/explorateur.svg)](https://pypi.python.org/pypi/explorateur/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Downloads](https://static.pepy.tech/personalized-badge/explorateur?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/explorateur)

# Explorateur

Explorateur is a Python library to conduct [State-Space-Search (SSS)](https://en.wikipedia.org/wiki/State_space_search), a powerful framework for solving problems that require search over a collection of states. 

Explorateur performs **generic state-space-search** over **problem-specific states and moves**. The user defines the `BaseState` and `BaseMove` and the library drives the search for solutions.

Given an initial user state, Explorateur performs search moves iteratively until a stopping condition is reached: 
- A termination state is found. 
- The search space is exhausted. 
- Hit stopping criteria such as max iterations, runtime limit, max depth. 
- Optionally, given a goal state, a goal state is encountered.

The behavior of the overall algorithm is controlled by the _Search Strategy_ and the _Exploration Strategy_. 

### Search Strategy
- `TreeSearch` over open states
- `GraphSearch` over open states while also storing the closed states to avoid visiting duplicates. 

### Exploration Strategy 
- `BreadthFirst` in uninformed fashion 
- `DepthFirst` in uninformed fashion
- `BestFirst` in informed fashion with an objective function that evaluates the quality of a state.

## Quick Start

To use Explorateur, you need to define `BaseState` and `BaseMove` as in the template below.  

```python
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType


# TODO Implement your own Search Moves
class MyMove(BaseMove):

    def __init__(self):
        # TODO Your move object
        pass

    def __str__(self) -> str:
        # TODO Your move string, also used for node labels in DOT graph
        pass


# TODO Implement your own Search State 
class MyState(BaseState):

    def __init__(self):
        # TODO Your problem specific state representation
        super().__init__() # Make sure to initialize the base state!

    def get_moves(self) -> List[MyMove]:
        # TODO Your branching decisions as a list of moves
        pass

    def is_terminate(self, goal_state=None) -> bool:
        # TODO Is the current state a solution/termination?
        pass

    def execute(self, move: MyMove) -> bool:
        # TODO Execute the move on the state and return success flag
        pass

    def __str__(self) -> str:
        # TODO Your state string, also used for node labels in DOT graph
        pass

# Explarateur
explorer = Explorateur()

# Initial state
initial_state = MyState()

# Search for solutions
if explorer.search(initial_state,
                   goal_state=None,  # Optional goal state
                   exploration_type=ExplorationType.DepthFirst(),
                   search_type=SearchType.TreeSearch(),
                   is_solution_path=True,
                   dot_filename="tree_search_dfs.dot"):
    
    # Retrieve the solution state and the solution path
    # Dot graph file is also available for visualizing the search 
    print("Solution:", explorer.solution_state)
    print("Solution Path:", *explorer.solution_path, sep="\n<-")
else:
    print("No solution found!")

# Search statistics
print("Total Decisions:", explorer.num_decisions)
print("Total Failures:", explorer.num_failed_decisions)
print("Total Time:", explorer.total_time)
```

## Concrete Examples

* **Backtracking Tree-Search:** Implementation to solve a toy [Constraint Satisfaction Problem](examples/backtrack_tree_search/main.py) using backtracking tree search, with the corresponding [search dot graph](examples/backtrack_tree_search/output.dot)  and [search visualization](https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20%3D%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%203%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%204%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%206%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%207%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20!%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2010%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2011%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2013%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2014%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%7D).
* **Graph Search: ** Implementation to solve the classical [Romanian Graph Problem][examples/graph_search/main.py] using a goal stat with the corresponding [search dot graph](examples/graph_search/output.dot)  and [search visualization](https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%221%0D%0AZerind%22%20%5Blabel%3D%22Zerind%22%5D%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%222%0D%0ASibiu%22%20%5Blabel%3D%22Sibiu%22%5D%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%223%0D%0ATimisoara%22%20%5Blabel%3D%22Timisoara%22%5D%3B%0D%0A%221%0D%0AZerind%22%20-%3E%20%224%0D%0AOradea%22%20%5Blabel%3D%22Oradea%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%225%0D%0AFagaras%22%20%5Blabel%3D%22Fagaras%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%226%0D%0AOradea%22%20%5Blabel%3D%22Oradea%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%227%0D%0ARimnicu%22%20%5Blabel%3D%22Rimnicu%22%5D%3B%0D%0A%223%0D%0ATimisoara%22%20-%3E%20%228%0D%0ALugoj%22%20%5Blabel%3D%22Lugoj%22%5D%3B%0D%0A%225%0D%0AFagaras%22%20-%3E%20%229%0D%0ABucharest%22%20%5Blabel%3D%22Bucharest%22%5D%3B%0D%0A%229%0D%0ABucharest%22%20%5Bstyle%3Dfilled%20fillcolor%3Dgreen%5D%3B%0D%0A%7D).

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
To confirm that cloning was successful, run the tests included in the project. All tests should pass.

```
git clone https://github.com/skadio/explorateur.git
cd explorateur
python -m unittest discover tests
```

To run a specific test from a given test file:
```
$ python -m unittest -v tests.<file_name>.<class_name>.<function_name>
```

For example: 
```
$ python -m unittest -v tests.test_usage_example.UsageExampleTest.test_usage_example
```

To confirm that installation was successful, try importing Explorateur after `pip install explorateur`

```
import explorateur
print(explorateur.__version__)
```

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/explorateur/issues).

## License

Explorateur is licensed under the [Apache License 2.0](LICENSE.md).

<br>
