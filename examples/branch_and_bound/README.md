# Branch and Bound

This is an implementation of the Branch and Bound algorithm using `explorateur` and Google OR-Tools to solve generic Binary/Integer Programming problems. The solver can read standard MPS files and find optimal solutions using an open-source toolchain.

## Installation

### Create virtual environment
```uv venv venv --python 3.9
source venv/bin/activate
uv pip install -r requirements.txt
```

The solver uses Google OR-Tools which is automatically installed with the requirements. No additional setup is needed.

## Usage

To solve an MPS file:
```bash
python main.py <mps_file>
```

Example MPS files can be found online (e.g., MIPLIB) or in the `data` folder:
```bash
python main.py ../data/50v-10.mps
```

The solver will:
1. Load the MPS file using OR-Tools
2. Solve the LP relaxation to get a lower bound
3. Use branch and bound to find the optimal integer solution
4. Output the results in JSON format


