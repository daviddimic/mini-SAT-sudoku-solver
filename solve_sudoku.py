#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, math

def read_sudoku_from_file():
    args = sys.argv
    if len(args) != 2:
        sys.exit(f"usage: python3 ./{args[0]} input_sudoku_file.txt")

    try:
        with open(args[1], "r") as f:
            sudoku_in = []
            for line in f.readlines():
                #converting string line from file to integer list
                int_line = list(map(lambda t: int(t), line.replace('\n', '').split()))
                sudoku_in.append(int_line)
            return sudoku_in
    except Exception as e:
        sys.exit(e)


def num_to_cnf(cnf_var, num, invert):
    """
    convert number to cnf clause
    num: 5 -> 0101
    cnf_var: 1 2 3 4
    ----------------
    new_clause: -1 2 -3 4
    if invert = True -> 1 -2 3 -4 (replace all 0 with 1)
    """
    s = -1 if invert else 1
    #list of binary digits from num, same length as cnf_var
    bin_list = map(lambda t: int(t), bin(num)[2:].zfill(len(cnf_var)))
    new_clause = [*map(lambda t: s*t[0] if t[1] else -s*t[0], zip(cnf_var, bin_list))]
    return new_clause


#add constraint: p and q must be different
def print_different_num_cnf(fp, p, q, n):
    for num in range(1, n+1):
        for p1 in num_to_cnf(p, num, True):
            fp.write(f"{p1} ")
        for q1 in num_to_cnf(q, num, True):
            fp.write(f"{q1} ")
        fp.write("0\n")


#write at the beginning of file
def insert(originalfile, string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string + '\n')
            f2.write(f.read())
    os.rename('newfile.txt', originalfile)


def make_cnf_dimacs(sudoku_in, out_file):
    clauses_number = 0
    #dimension of puzzle and minimal number of bits to represent one number
    n = len(sudoku_in[0])
    block = int(math.sqrt(n))
    num_of_bits = len(bin(n)[2:])

    with open(out_file, "w") as f:
        for i in range(1, n*n+1):
            #LOG CODING: each number is represented with n-bits (num_of_bits) pn pn-1 ... p1
            p = [num_of_bits*i - (num_of_bits-1) + offset for offset in range(num_of_bits)]

            #NOTE: CONSTRAINT 1
            #valid numbers in sudoku: from 1 to n
            #restrict all other numbers that can be produced with our coding
            forbidden_numbers = [*range(n+1, 1 << num_of_bits)]
            forbidden_numbers.append(0)
            for num in forbidden_numbers:
                for j in num_to_cnf(p, num, True):
                    f.write(f"{j} ")
                clauses_number += 1
                f.write("0\n")

            #NOTE: CONSTRAINT 2
            #add numbers from given input sudoku
            #converting serial number (1-n*n) to index (i, j)
            curr_num = sudoku_in[(i-1)//n][(i-1)%n]
            if curr_num != 0:
                #add all non-zero numbers
                for j in num_to_cnf(p, curr_num, False):
                    f.write(f"{j} 0\n")
                    clauses_number += 1

            #NOTE: CONSTRAINT 3
            #in each row, column and block different numbers from 1 to n
            for j in range(i+1, n*n+1):
                #LOG CODING
                q = [num_of_bits*j - (num_of_bits-1) + offset for offset in range(num_of_bits)]

                #row
                if (i-1)//n == (j-1)//n:
                    print_different_num_cnf(f, p, q, n)
                    clauses_number += n
                #column
                elif (i-1)%n == (j-1)%n:
                    print_different_num_cnf(f, p, q, n)
                    clauses_number += n
                #block
                elif (((i-1)//n)//block, ((i-1)%n)//block) == (((j-1)//n)//block, ((j-1)%n)//block):
                    print_different_num_cnf(f, p, q, n)
                    clauses_number += n

    insert(out_file, f"p cnf {n*n*num_of_bits} {clauses_number}")
    return n


def ksplit(line, sep, k):
    """
    Split string at every k occurrence of sep,
    using sep as the delimiter string.
    """
    line = line.split(sep)
    return [line[i:i+k] for i in range(0, len(line), k)]


def cnf_to_num(cnf_clause):
    """
    Inverse of `num_to_cnf` function
    convert cnf clause to number
    from [-1 2 -3 4] to 5
    """
    str_bin = [*map(lambda digit: '1' if int(digit) > 0 else '0' , cnf_clause)]
    return int(''.join(str_bin),2)


def decode_output(sat_output, n):
    num_of_bits = len(bin(n)[2:])

    #open output file with minisat solution
    with open(sat_output, "r") as f:
        solution = f.read()
    if solution[:3] != 'SAT':
        sys.exit(0)

    #clean string solution
    solution = solution.replace(' 0\n', '').replace('SAT\n', '')
    #decode and write sa matrix
    out_sudoku = "out_sudoku.txt"
    with open(out_sudoku, "w") as g:
        for i, cnf_num in enumerate(ksplit(solution, ' ', num_of_bits)):
            num = cnf_to_num(cnf_num)
            g.write(f"{num} ")
            if (i+1) % n == 0:
                g.write("\n")


def main():
    sudoku_in = read_sudoku_from_file()
    out_file = "out_sudoku.cnf"

    #NOTE: modeling solution
    n = make_cnf_dimacs(sudoku_in, out_file)

    #NOTE: solving
    #call sat-solver `minisat`
    sat_output = "sat_sudoku_solution.txt"
    os.system(f"minisat {out_file} {sat_output}")

    #NOTE: decode and print to file
    decode_output(sat_output, n)


if __name__ == "__main__":
    main()
