# Anubhav Parbhakar
# CISC 481 - 010
# Project 2
import ast
import copy
import math
from sqlite3 import complete_statement
from flask import Blueprint, Flask, render_template, redirect, url_for

with open("sudoku_constraints.py") as constraints_file:
    nineBynine = ast.literal_eval(constraints_file.read())

# part 1 constraints
fourByfour = {("C11", "C12"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C13"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C14"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C21"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C31"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C41"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C11", "C22"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C21", "C22"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C21", "C23"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C21", "C24"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C21", "C31"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C21", "C41"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C31", "C32"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C31", "C33"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C31", "C34"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C31", "C41"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C31", "C42"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C41", "C42"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C41", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C41", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C13"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C14"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C22"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C21"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C32"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C12", "C42"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C22", "C23"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C22", "C24"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C22", "C32"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C22", "C42"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C32", "C33"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C32", "C41"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C32", "C34"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C32", "C42"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C42", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C42", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C13", "C14"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C13", "C23"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C13", "C33"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C13", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C13", "C24"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C23", "C24"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C23", "C33"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C23", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C33", "C34"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C33", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C33", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C43", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C14", "C23"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C14", "C24"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C14", "C34"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C14", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C24", "C34"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C24", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C34", "C44"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              ("C34", "C43"): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
              }


def domain_generator(board: list) -> dict:
    # assume: that each  list in the board will be of size n
    # and that there are n lists in the board
    # each element will be a value, or a "nil", to represent a square in the init board
    x = len(board)
    y = len(board[0])
    domain = {}

    for i in range(0, x):
        for j in range(0, y):
            string = "C" + str(i+1) + str(j+1)
            if(board[i][j] == "nil"):
                domain[string] = [a+1 for a in range(0, y)]
            else:
                domain[string] = [board[i][j]]
    return domain


def complete_board_generator(assignments: list) -> list:
    for assignment in assignments:
        for i in range(1, 10):
            for j in range(1, 10):
                string = "C" + str(i) + str(j)
                try:
                    assignment[string]
                except KeyError:
                    assignment[string] = [k for k in range(1, 10)]
    return assignments


def revise(var1: str, var2: str, csp: dict, domain: dict) -> bool:
    revised = False
    for x in domain[var1]:
        counter = 0
        for y in domain[var2]:
            for constraint in csp[var1, var2]:
                if(constraint != [x, y]):
                    counter += 1
        if(counter == len(csp[var1, var2])):
            domain[var1].remove(x)
            revised = True
    return revised


def ac_3(csp: dict, domain: dict) -> bool:
    queue = create_arcs(csp)
    arc_list = create_arcs(csp)
    while(len(queue) != 0):
        arc = queue.pop(0)
        if(revise(arc[0], arc[1], csp, domain)):
            if(len(domain[arc[0]]) == 0):
                return False
            for double in arc_list:
                if(double[1] == arc[0]):
                    queue.append(double)
    return True


def create_arcs(csp: dict) -> list:
    keys = list(csp.keys())

    arc_list = []
    for double in keys:
        csp[double[1], double[0]] = csp[double[0], double[1]]
        arc_list.append(double)
        arc_list.append((double[1], double[0]))

    return arc_list


def minimum_remaining_values(vars: list, domain: dict) -> str:
    low_var = ""
    # sqrt(x^2) = x, i.e. a square in a n * n sudoku board will have a max of n choices
    max_len = math.sqrt(len(vars))
    for var in vars:
        if(len(domain[var]) <= max_len and len(domain[var]) != 1):
            low_var = var
    return low_var


def backtracking_search(csp: dict, problem: dict):
    assignment = {}
    for value in problem:
        if(len(problem[value]) == 1):
            assignment[value] = problem[value]

    return backtrack(csp, problem, [assignment, [], []])


def unassigned_vars(problem: dict) -> dict:
    unassigned_vars = {}
    for value in problem:
        if(len(problem[value]) > 1):
            unassigned_vars[value] = problem[value]
    return unassigned_vars


def is_assignment_complete(problem: dict) -> bool:
    for value in problem.keys():
        if(len(problem[value]) > 1):
            return False
    return True


def check_assignment_var_path(assignments: list) -> bool:
    for assignment in assignments:
        for value in assignment:
            if(assignment):
                if(len(assignment[value]) > 1):
                    return False
            else:
                return False
    return True


def check_unassigned_vars_path(unassigned_vars_path: list) -> bool:
    counter = 0
    for unassigned_vars in unassigned_vars_path:
        if(len(unassigned_vars) == 0):
            counter += 1
        if(counter > 1):
            return False
    return True


# there is a bug where the "assigned var" gets improperly added to the
# assigned_var_path list
# spent hours trying to figure it out but couldn't
def backtrack(csp: dict, problem: dict, state_space: list) -> list:
    assignment = state_space[0]
    # avp[0] - intial board, avp[1] - init board w/ one more value
    assignment_var_path = state_space[1]
    # print(type(assignment_var_path))
    if(len(assignment_var_path) == 0):
        assignment_var_path.append(assignment)
    if(check_assignment_var_path(assignment_var_path)):
        assignment_var_path.append(assignment)
    unassigned_vars_path = state_space[2]
    if(len(unassigned_vars_path) == 0):
        unassigned_vars_path.append(unassigned_vars(problem))
    if(check_unassigned_vars_path(unassigned_vars_path)):
        unassigned_vars_path.append(unassigned_vars(problem))

    if(is_assignment_complete(problem)):
        return [problem, assignment_var_path, unassigned_vars_path]

    mrv = minimum_remaining_values(problem.keys(), problem)

    for x in problem[mrv]:
        new_problem = copy.deepcopy(problem)
        new_assignment = assignment.copy()
        new_problem[mrv] = [x]

        new_assignment[mrv] = new_problem[mrv]
        if(ac_3(csp, new_problem)):
            new_state_space = [new_assignment,
                               assignment_var_path, unassigned_vars_path]
            if(backtrack(csp, new_problem, new_state_space)):
                return backtrack(csp, new_problem, new_state_space)
        new_assignment.pop(mrv)
    return []


app = Flask(__name__)


@ app.route("/reroute/<name>")
# used to handle "favicon" string when accepting the puzzle string
def reroute(name):
    return redirect(url_for("user", name))


@ app.route("/<name>")
def user(name):
    problem = domain_generator(ast.literal_eval(name))
    output = backtracking_search(nineBynine, problem)
    assignments = complete_board_generator(output[1])
    return render_template("index.html", original_puzzle=problem, solution=output[0], variables=list(problem.keys()), assignments=assignments)


if (__name__ == "__main__"):
    app.run()
