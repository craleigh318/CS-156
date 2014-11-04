__author__ = 'Anthony Ferrero'

import string


NUM_SUDOKU_ROWS = 9
NUM_SUDOKU_COLUMNS = NUM_SUDOKU_ROWS
NUM_BOX_ROWS = 3

EQUAL_STRING = 'eq'
NOT_EQUAL_STRING = 'ne'
LESS_THAN_STRING = 'lt'
GREATER_THAN_STRING = 'gt'

MIN_SUDOKU_CELL_VALUE = 1
MAX_SUDOKU_CELL_VALUE = 9

_last_sudoku_row_letter = 'I'
_last_letter_ind = string.ascii_uppercase.index(_last_sudoku_row_letter)
SUDOKU_ROW_LETTERS = string.ascii_uppercase[:_last_letter_ind + 1]


def cell(cell_letter, cell_number):
    return cell_letter + str(cell_number)


def constraint(left_cell, constraint_str, right_cell_or_num):
    return left_cell + ' ' + constraint_str + ' ' + str(right_cell_or_num)


def equal_constraint(left_cell, num):
    return constraint(left_cell, EQUAL_STRING, num)


def greater_than_constraint(left_cell, right_cell_or_num):
    return constraint(left_cell, GREATER_THAN_STRING, right_cell_or_num)


def less_than_constraint(left_cell, right_cell_or_num):
    return constraint(left_cell, LESS_THAN_STRING, right_cell_or_num)


def diff_constraint(left_cell, right_cell_or_num):
    return constraint(left_cell, NOT_EQUAL_STRING, right_cell_or_num)


def alldiff_list(sudoku_cells):
    alldiff = []
    for static_index in xrange(len(sudoku_cells)):
        cell = sudoku_cells[static_index]
        cell_diff = []
        for changing_index in xrange(static_index + 1, len(sudoku_cells)):
            other_cell = sudoku_cells[changing_index]
            cell_diff.append(diff_constraint(cell, other_cell))
        alldiff.extend(cell_diff)
    return alldiff


def cell_list(letters, numbers):
    l = []
    for letter in letters:
        for number in numbers:
            l.append(cell(letter, number))
    return l


def row_list(row_num):
    letter = string.ascii_uppercase[row_num - 1]
    return cell_list([letter], xrange(1, NUM_SUDOKU_COLUMNS + 1))


def column_list(column_num):
    return cell_list(SUDOKU_ROW_LETTERS, [column_num])


def box_list(box_num):
    box_row_num = ((box_num - 1) // NUM_BOX_ROWS) + 1
    box_letters = SUDOKU_ROW_LETTERS[(box_row_num - 1) * 3: box_row_num * 3]
    box_column_num = (box_num - ((box_row_num - 1) * NUM_BOX_ROWS))
    box_numbers = xrange(((box_column_num - 1) * 3) + 1, (box_column_num * 3) + 1)

    l = []
    for letter in box_letters:
        for number in box_numbers:
            l.append(cell(letter, number))
    return l


def list_2d_to_1d(list_2d):
    return [elem for sublist in list_2d for elem in sublist]


def flat_list(list_maker_function, iterable):
    list_2d = [list_maker_function(elem) for elem in iterable]
    return list_2d_to_1d(list_2d)


def domain_constraints(flat_row_list):
    constraints = [less_than_constraint(cell, MAX_SUDOKU_CELL_VALUE + 1) for cell in flat_row_list]
    constraints.extend([greater_than_constraint(cell, MIN_SUDOKU_CELL_VALUE - 1) for cell in flat_row_list])
    return constraints


def general_constraints():
    rows = [row_list(row_num) for row_num in xrange(1, NUM_SUDOKU_COLUMNS + 1)]
    columns = [column_list(col_num) for col_num in xrange(1, NUM_SUDOKU_ROWS + 1)]
    boxes = [box_list(box_num) for box_num in xrange(1, NUM_BOX_ROWS ** 2 + 1)]

    alldiff_lambda = lambda cells: alldiff_list(cells)
    rows_alldiff = flat_list(alldiff_lambda, rows)
    columns_alldiff = flat_list(alldiff_lambda, columns)
    boxes_alldiff = flat_list(alldiff_lambda, boxes)

    sudoku_diffs = []
    sudoku_diffs.extend(rows_alldiff)
    sudoku_diffs.extend(columns_alldiff)
    sudoku_diffs.extend(boxes_alldiff)

    flat_row_list = list_2d_to_1d(rows)

    result = []
    result.extend(domain_constraints(flat_row_list))
    result.extend(sudoku_diffs)
    return result


# These are taken from the book, page 269, figure 4.
def given_cell_assignments():
    return [
        equal_constraint('A3', 3),
        equal_constraint('A5', 2),
        equal_constraint('A7', 6),

        equal_constraint('B1', 9),
        equal_constraint('B4', 3),
        equal_constraint('B6', 5),
        equal_constraint('B9', 1),

        equal_constraint('C3', 1),
        equal_constraint('C4', 8),
        equal_constraint('C6', 6),
        equal_constraint('C7', 4),

        equal_constraint('D3', 8),
        equal_constraint('D4', 1),
        equal_constraint('D6', 2),
        equal_constraint('D7', 9),

        equal_constraint('E1', 7),
        equal_constraint('E9', 8),

        equal_constraint('F3', 6),
        equal_constraint('F4', 7),
        equal_constraint('F6', 8),
        equal_constraint('F7', 2),

        equal_constraint('G3', 2),
        equal_constraint('G4', 6),
        equal_constraint('G6', 9),
        equal_constraint('G7', 5),

        equal_constraint('H1', 8),
        equal_constraint('H4', 2),
        equal_constraint('H6', 3),
        equal_constraint('H9', 9),

        equal_constraint('I3', 5),
        equal_constraint('I5', 1),
        equal_constraint('I7', 3)
    ]


def generate_sudoku_csp():
    constraints = general_constraints()
    constraints.extend(given_cell_assignments())

    return '\n'.join(constraints)


if __name__ == '__main__':
    sudoku_csp_string = generate_sudoku_csp()
    with open('Test Sudoku.txt', 'w+') as sudoku_csp_file:
        sudoku_csp_file.write(sudoku_csp_string)
