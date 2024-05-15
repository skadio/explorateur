# Explorateur

Explorateur is a Python library to conduct [State-Space-Search (SSS)](https://en.wikipedia.org/wiki/State_space_search). SSS is useful for solving problems that require searching over a collection of states. Explorateur starts with a given initial state, and then, performs iterative search moves until either a termination state is found, the search space is exhausted, or a stopping criteria, such as the number of iterations, runtime limit, or maximum depth, has been reached. Optionally, a goal state can be given as input to terminate the search when the goal state is found.

Explorateur performs generic state space search over problem-specific `BaseState` and `BaseMove` representations. The behavior of the overall algorithm is controlled by the search strategy and the exploration strategy. The search strategy can be `TreeSearch` over open states, or `GraphSearch` over open states while storing the closed on to avoid visiting duplicate states. The exploration strategy can be uninformed as in `BreadthFirst` and `DepthFirst`, or informed as in `BestFirst` that assumes an objective function to evaluate the solution quality of a state.  

## Quick Start

To use Explorateur, you need to provide problem specific `BaseState` and `BaseMove` representations. 

Here is the template `BaseMove` and `BaseState` ready to implement for your specific case. Once the search terminates, if a solution is found, the solution state and the solution path can be retrieved as well as the dot graph of the search visualization. 

```python
from explorateur import Explorateur, BaseMove, BaseState, ExplorationType, SearchType


# TODO Implement your own search moves
class MyMove(BaseMove):

    def __init__(self):
        # TODO Your move object
        pass

    def __str__(self) -> str:
        # TODO Your mvoe string, also used for node labels in DOT graph
        pass


# TODO Implement your own search state 
class MyState(BaseState):

    def __init__(self):
        # TODO Your problem specific state representation
        super().__init__() # Make sure to initial the base state!
        

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

# Explorateur
explorer = Explorateur()

# Initial state
initial_state = MyState()

# Search for solutions
if explorer.search(initial_state,
                   goal_state=None,  # Optional goal state
                   exploration_type=ExplorationType.DepthFirst(),
                   search_type=SearchType.TreeSearch(),
                   is_solution_path=True,
                   dot_file_path="tree_search_dfs.dot"):
    print("Solution:", explorer.solution_state)
    print("Solution Path:", *explorer.solution_path, sep="\n<-")
else:
    print("No solution found!")

# Search statistics
print("Total Decisions:", explorer.num_decisions)
print("Total Failures:", explorer.num_failed_decisions)
print("Total Time:", explorer.total_time)
```

## Concrete Example

Here is a concrete implementation to solve a toy [Constraint Satisfaction Problem](examples/usage_example.py) with the corresponding [dot graph](examples/usage_example.dot) of the search and [search visualization](https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0D%0Aspline%3Dline%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20%3D%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%203%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%202%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%204%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%201%0D%0AAssignment%3A%20%7B'x'%3A%201%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%206%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%205%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%207%0D%0AAssignment%3A%20%7B'x'%3A%201%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%200%0D%0AAssignment%3A%20%7B%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B1%2C%202%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22x%20!%3D%201%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20%3D%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2010%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%209%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2011%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2010%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%208%0D%0AAssignment%3A%20%7B'x'%3A%202%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B10%2C%2020%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20%5Blabel%3D%22y%20!%3D%2010%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2013%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20100%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%5D%7D%22%20%5Blabel%3D%22z%20%3D%3D%20100%22%5D%3B%0D%0A%22State%20ID%3A%2012%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B100%2C%20200%5D%7D%22%20-%3E%20%22State%20ID%3A%2014%0D%0AAssignment%3A%20%7B'x'%3A%202%2C%20'y'%3A%2020%2C%20'z'%3A%20200%7D%0D%0ADomains%3A%20%7B'x'%3A%20%5B2%5D%2C%20'y'%3A%20%5B20%5D%2C%20'z'%3A%20%5B200%5D%7D%22%20%5Blabel%3D%22z%20!%3D%20100%22%5D%3B%0D%0A%7D).


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

## Changelog

| Date         | Notes           |
|--------------|-----------------|
| 15 May, 2024 | Initial release |

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/explorateur/issues).

## License

Explorateur is licensed under the [Apache License 2.0](LICENSE.md).

<br>
