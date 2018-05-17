# mini-SAT-sudoku-solver
Modeling sudoku in dimacs CNF and solving with minisat.

## Requirements

- python 3
- minisat http://minisat.se/

## Usage

`python3 solve_sudoku.py in_sudoku.txt`

## Input

In `in_sudoku.txt` is matrix 9x9: with numbers 1-9 or 0 for unknown values.

## Output
- `out_sudoku.cnf` input sudoku in dimacs cnf format
- `sat_sudoku_solution.txt` output of minisat
- `out_sudoku.txt` solved sudoku represented as 9x9 matrix, if solvable.
