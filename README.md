# mini-SAT-sudoku-solver
Modeling sudoku in dimacs CNF and solving with minisat.

## Requirements

- python 3.6.x
- minisat http://minisat.se/

## Usage

`python3 solve_sudoku.py input_test/in_25x25_sudoku_1.txt`

## Input

In `input_test` folder is examples of input sudoku represented as nxn matrix with numbers 1-n or 0 for unknown values. `in_nxn_sudoku_k.txt` for n 9, 16, 25.


## Output
- `out_sudoku.cnf` cnf output is input sudoku for minisat in dimacs cnf format
- `sat_sudoku_solution.txt` output of minisat
- `out_sudoku.txt` decoded sat_sudoku_solution.txt. Solved sudoku represented as nxn matrix, if solvable.
