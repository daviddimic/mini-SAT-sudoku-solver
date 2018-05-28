# mini-SAT-sudoku-solver
Modeling sudoku in dimacs CNF and solving with minisat.

## Requirements

- python 3.6.x
- minisat http://minisat.se/

## Usage

`python3 solve_sudoku.py in_sudoku.txt`

## Input

In `in_sudoku.txt` is matrix nxn: with numbers 1-n or 0 for unknown values.

## Output
- `out_sudoku.cnf` cnf output is input sudoku for minisat in dimacs cnf format
- `sat_sudoku_solution.txt` output of minisat
- `out_sudoku.txt` decoded sat_sudoku_solution.txt. Solved sudoku represented as nxn matrix, if solvable.
