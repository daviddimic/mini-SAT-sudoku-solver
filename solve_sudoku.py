#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

def read_sudoku_from_file():
    args = sys.argv
    if len(args) != 2:
        sys.exit(f"usage: python3 ./{args[0]} input_sudoku_file.txt")

    try:
        with open(args[1], "r") as f:
            sudoku_in = []
            for line in f.readlines():
                #converting string line from file to integer list
                int_line = list(map(lambda t: int(t), list(line.replace(' ', '').replace('\n', ''))))
                sudoku_in.append(int_line)
            return sudoku_in
    except Exception as e:
        sys.exit(e)


def num_to_cnf(cnf_var, num, reverse):
    """
    convert number to cnf clause
    num: 5 -> 0101
    cnf_var: 1 2 3 4
    ----------------
    mew_clause: -1 2 -3 4
    if reverse = True -> 1 -2 3 -4 (replace all 0 with 1)
    """
    new_clause = []
    s = -1 if reverse else 1
    new_clause.append(-s*cnf_var[0] if num//8 % 2 == 0 else s*cnf_var[0])
    new_clause.append(-s*cnf_var[1] if num//4 % 2 == 0 else s*cnf_var[1])
    new_clause.append(-s*cnf_var[2] if num//2 % 2 == 0 else s*cnf_var[2])
    new_clause.append(-s*cnf_var[3] if num    % 2 == 0 else s*cnf_var[3])
    return new_clause


#add constraint: p and q must be different
def print_different_num_cnf(f, p, q):
    for num in range(1, 10):
        for p1 in num_to_cnf(p, num, True):
            f.write(f"{p1} ")
        for q1 in num_to_cnf(q, num, True):
            f.write(f"{q1} ")
        f.write("0\n")


def insert(originalfile, string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string + '\n')
            f2.write(f.read())
    os.rename('newfile.txt', originalfile)


def make_cnf_dimacs(sudoku_in, out_file):
    clauses_number = 0
    with open(out_file, "w") as f:
        for i in range(1, 82):
            #CODING: each number is represented with 4-bits p4p3p3p1
            p4 = 4*i - 3
            p3 = p4 + 1
            p2 = p4 + 2
            p1 = p4 + 3
            p = [p4, p3, p2, p1]

            #NOTE: CONSTRAINT 1
            #valid numbers in sudoku: from 1 to 9
            #restrict all other numbers that can be produced with our coding
            forbidden_numbers = [0, 10, 11, 12, 13, 14, 15]
            for num in forbidden_numbers:
                for j in num_to_cnf(p, num, True):
                    f.write(f"{j} ")
                clauses_number += 1
                f.write("0\n")

            #NOTE: CONSTRAINT 2
            #add numbers from given input sudoku
            #converting serial number (1-81) to index (i, j)
            curr_num = sudoku_in[(i-1)//9][(i-1)%9]
            if curr_num != 0:
                #add all none-zero numbers
                for j in num_to_cnf(p, curr_num, False):
                    f.write(f"{j} 0\n")
                    clauses_number += 1

            #NOTE: CONSTRAINT 3
            #in each row, column and 3x3 blok different numbers from 1 to 9
            for j in range(1, 82):
                if i < j:
                    #CODING: same, number2 with 4-bits q4q3q3q1
                    q4 = 4*j - 3
                    q3 = q4 + 1
                    q2 = q4 + 2
                    q1 = q4 + 3
                    q = [q4, q3, q2, q1]

                    #row
                    if (i-1)//9 == (j-1)//9:
                        print_different_num_cnf(f, p, q)
                        clauses_number += 9
                    #column
                    elif (i-1)%9 == (j-1)%9:
                        print_different_num_cnf(f, p, q)
                        clauses_number += 9
                    #3x3 block
                    elif (((i-1)//9)//3, ((i-1)%9)//3) == (((j-1)//9)//3, ((j-1)%9)//3):
                        print_different_num_cnf(f, p, q)
                        clauses_number += 9

    insert(out_file, f"p cnf {81*4} {clauses_number}")


def decode_output(sat_output):
    #open output file with sat-solver solution
    with open(sat_output, "r") as f:
        solution = f.read()
        decoded_solution = []

        if solution[:3] != 'SAT':
            sys.exit(0)

        #decoding solution, for example: convert -a b -c d -> 0101 -> 5
        solution = solution.replace('0\n', '').replace('SAT\n', '').split()
        decoded_num = ''
        for ind, num in enumerate(solution):
            #4 numbers convert to one
            if ind % 4 == 0:
                if decoded_num != '':
                    decoded_solution.append(int(decoded_num, 2))
                decoded_num = ''
            decoded_digit = '0' if int(num) < 0 else '1'
            decoded_num += decoded_digit
        decoded_solution.append(int(decoded_num, 2))

        #print decoded solution as matrix
        out_sudoku = "out_sudoku.txt"
        with open(out_sudoku, "w") as g:
            for i, num in enumerate(decoded_solution):
                g.write(f"{num} ")
                if (i+1) % 9 == 0:
                    g.write("\n")



def main():
    sudoku_in = read_sudoku_from_file()
    out_file = "out_sudoku.cnf"

    #NOTE: modeling solution
    make_cnf_dimacs(sudoku_in, out_file)

    #NOTE: solving
    #call sat-solver `minisat`
    sat_output = "sat_sudoku_solution.txt"
    os.system(f"minisat {out_file} {sat_output}")

    #NOTE: decode and print to file
    decode_output(sat_output)


if __name__ == "__main__":
    main()
