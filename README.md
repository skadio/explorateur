[![PyPI version fury.io](https://badge.fury.io/py/explorateur.svg)](https://pypi.python.org/pypi/explorateur/) [![PyPI license](https://img.shields.io/pypi/l/explorateur.svg)](https://pypi.python.org/pypi/explorateur/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Downloads](https://static.pepy.tech/personalized-badge/explorateur?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/explorateur)

---

<div align="center"><a name="menu"></a>
  <h3>
    <a href="https://github.com/skadio/explorateur?tab=readme-ov-file#quick-start">Quick Start</a> •
    <a href="https://github.com/skadio/explorateur?tab=readme-ov-file#examples">Examples</a> •
    <a href="https://github.com/skadio/explorateur?tab=readme-ov-file#installation">Installation</a>
  </h3>
</div>

---

# Explorateur

Explorateur is a Python library to conduct [State-Space-Search (SSS)](https://en.wikipedia.org/wiki/State_space_search), a powerful framework for solving problems that require search over a collection of states. 

Explorateur performs **generic state-space-search** over **problem-specific states and moves**. The user defines the `BaseState` and `BaseMove` and the library drives the search for solutions. 

The behavior of the search is controlled by the built-in _Search Strategy_ and the _Exploration Strategy_ and user-defined _moves_. Given an initial user state, Explorateur performs search moves iteratively until a stopping condition is reached.

 ### Search Strategy
- `TreeSearch` over open states,
- `GraphSearch` over open states while also storing the closed states to avoid visiting duplicates. 

### Exploration Strategy 
- `BreadthFirst` in an uninformed fashion,
- `DepthFirst` in an uninformed fashion,
- `BestFirst` in an informed fashion with an objective function that evaluates the quality of a state. By default, the best first search is set to minimize. To maximize, multiply your objective function by -1.

### Stopping Conditions 
- A termination state is found,
- The search space is exhausted, 
- A stopping criterion such as max iterations, runtime limit, or max depth has been reached, 
- (Optionally) The given goal state is encountered.

## Quick Start

To use Explorateur, you must define `BaseState` and `BaseMove` as in the template below.  

```python
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType


# Implement your Search Moves
class MyMove(BaseMove):

    def __init__(self):
        # TODO Your move object
        pass

    def __str__(self) -> str:
        # TODO Your move string, also used for node labels in DOT graph
        pass


# Implement your own Search State 
class MyState(BaseState):

    def __init__(self):
        # TODO Your problem-specific state representation
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

## Examples

* **Backtracking Tree-Search:** A toy [Constraint Satisfaction Problem](examples/backtrack_tree_search/main.py) to find a solution via backtracking tree search as depicted in [search visualization](https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20%3D%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%203%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%204%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%206%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%207%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20!%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2010%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2011%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2013%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2014%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%7D).
* **Graph Search:** The classical [Romanian Graph Problem](examples/graph_search/main.py) solved with a goal state as depicted in [search visualization](https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%221%0D%0AZerind%22%20%5Blabel%3D%22Zerind%22%5D%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%222%0D%0ASibiu%22%20%5Blabel%3D%22Sibiu%22%5D%3B%0D%0A%220%0D%0AArad%22%20-%3E%20%223%0D%0ATimisoara%22%20%5Blabel%3D%22Timisoara%22%5D%3B%0D%0A%221%0D%0AZerind%22%20-%3E%20%224%0D%0AOradea%22%20%5Blabel%3D%22Oradea%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%225%0D%0AFagaras%22%20%5Blabel%3D%22Fagaras%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%226%0D%0AOradea%22%20%5Blabel%3D%22Oradea%22%5D%3B%0D%0A%222%0D%0ASibiu%22%20-%3E%20%227%0D%0ARimnicu%22%20%5Blabel%3D%22Rimnicu%22%5D%3B%0D%0A%223%0D%0ATimisoara%22%20-%3E%20%228%0D%0ALugoj%22%20%5Blabel%3D%22Lugoj%22%5D%3B%0D%0A%225%0D%0AFagaras%22%20-%3E%20%229%0D%0ABucharest%22%20%5Blabel%3D%22Bucharest%22%5D%3B%0D%0A%229%0D%0ABucharest%22%20%5Bstyle%3Dfilled%20fillcolor%3Dgreen%5D%3B%0D%0A%7D). Note the use of `__eq__` and `__hash__` to enable graph-based search to handle state comparison and hashing.
* **A\* Search:** The classical [A* Search](examples/a_star/main.py) between an initial and goal state using an admissible heuristic solved with best-first search to minimize the total cost as depicted in [search visualization](https://dreampuf.github.io/GraphvizOnline/?engine=dot#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%220%0D%0AArad%0D%0ABackward%20Cost%200%0D%0AForward%20Cost%20366%0D%0ATotal%20Cost%20366%22%20-%3E%20%221%0D%0AZerind%0D%0ABackward%20Cost%2075%0D%0AForward%20Cost%20374%0D%0ATotal%20Cost%20449%22%20%5Blabel%3D%22Zerind%22%5D%3B%0D%0A%220%0D%0AArad%0D%0ABackward%20Cost%200%0D%0AForward%20Cost%20366%0D%0ATotal%20Cost%20366%22%20-%3E%20%222%0D%0ASibiu%0D%0ABackward%20Cost%20140%0D%0AForward%20Cost%20253%0D%0ATotal%20Cost%20393%22%20%5Blabel%3D%22Sibiu%22%5D%3B%0D%0A%220%0D%0AArad%0D%0ABackward%20Cost%200%0D%0AForward%20Cost%20366%0D%0ATotal%20Cost%20366%22%20-%3E%20%223%0D%0ATimisoara%0D%0ABackward%20Cost%20118%0D%0AForward%20Cost%20329%0D%0ATotal%20Cost%20447%22%20%5Blabel%3D%22Timisoara%22%5D%3B%0D%0A%222%0D%0ASibiu%0D%0ABackward%20Cost%20140%0D%0AForward%20Cost%20253%0D%0ATotal%20Cost%20393%22%20-%3E%20%224%0D%0AOradea%0D%0ABackward%20Cost%20291%0D%0AForward%20Cost%20380%0D%0ATotal%20Cost%20671%22%20%5Blabel%3D%22Oradea%22%5D%3B%0D%0A%222%0D%0ASibiu%0D%0ABackward%20Cost%20140%0D%0AForward%20Cost%20253%0D%0ATotal%20Cost%20393%22%20-%3E%20%225%0D%0ARimnicu%0D%0ABackward%20Cost%20220%0D%0AForward%20Cost%20193%0D%0ATotal%20Cost%20413%22%20%5Blabel%3D%22Rimnicu%22%5D%3B%0D%0A%222%0D%0ASibiu%0D%0ABackward%20Cost%20140%0D%0AForward%20Cost%20253%0D%0ATotal%20Cost%20393%22%20-%3E%20%226%0D%0AFagaras%0D%0ABackward%20Cost%20239%0D%0AForward%20Cost%20176%0D%0ATotal%20Cost%20415%22%20%5Blabel%3D%22Fagaras%22%5D%3B%0D%0A%225%0D%0ARimnicu%0D%0ABackward%20Cost%20220%0D%0AForward%20Cost%20193%0D%0ATotal%20Cost%20413%22%20-%3E%20%227%0D%0ACraiova%0D%0ABackward%20Cost%20366%0D%0AForward%20Cost%20160%0D%0ATotal%20Cost%20526%22%20%5Blabel%3D%22Craiova%22%5D%3B%0D%0A%225%0D%0ARimnicu%0D%0ABackward%20Cost%20220%0D%0AForward%20Cost%20193%0D%0ATotal%20Cost%20413%22%20-%3E%20%228%0D%0APitesti%0D%0ABackward%20Cost%20317%0D%0AForward%20Cost%20100%0D%0ATotal%20Cost%20417%22%20%5Blabel%3D%22Pitesti%22%5D%3B%0D%0A%226%0D%0AFagaras%0D%0ABackward%20Cost%20239%0D%0AForward%20Cost%20176%0D%0ATotal%20Cost%20415%22%20-%3E%20%229%0D%0ABucharest%0D%0ABackward%20Cost%20450%0D%0AForward%20Cost%200%0D%0ATotal%20Cost%20450%22%20%5Blabel%3D%22Bucharest%22%5D%3B%0D%0A%229%0D%0ABucharest%0D%0ABackward%20Cost%20450%0D%0AForward%20Cost%200%0D%0ATotal%20Cost%20450%22%20%5Bstyle%3Dfilled%20fillcolor%3Dgreen%5D%3B%0D%0A%7D). Note the use of `get_objective` function for optimization.


## Installation 
Explorateur can be installed from PyPI using `pip install explorateur`

<details>
<summary><b> Install from source</b></summary> <br>
Alternatively, you can build a wheel package on your platform from scratch using the source code:

```bash
git clone https://github.com/skadio/explorateur.git
cd explorateur
pip install setuptools wheel # if wheel is not installed
python setup.py sdist bdist_wheel
pip install dist/explorateur-X.X.X-py3-none-any.whl
```
</details>

<details>
<summary><b> Test your setup</b></summary> <br>
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

To confirm that the installation was successful, try importing Explorateur after `pip install explorateur`

```
import explorateur
print(explorateur.__version__)
```

</details>

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/explorateur/issues).

## License

Explorateur is licensed under the [Apache License 2.0](LICENSE.md).

<br>
