def current_col(puzzle, col_num):
    """
    Returns a column of the sudoku puzzle.

    Arguments:
        puzzle (list[list[int]]): 2D List of integers representing a sudoku puzzle.
        col_num (int): A column number from the puzzle.

    Returns:
        list[int]: List of integers that represent a column of the puzzle.
    """
    puzzle_col = []

    for row in range(len(puzzle)):
        puzzle_col.append(puzzle[row][col_num])

    return puzzle_col


def current_grid(puzzle, row_num, col_num):
    """
    Returns a 3x3 grid of the sudoku puzzle.

    Arguments:
        puzzle (list[list[int]]): 2D List of integers representing a sudoku puzzle.
        row_num (int): A row number from the puzzle.
        col_num (int): A column number from the puzzle.

    Returns:
        list[int]: List of integers that represent the numbers in a 3x3 grid of the puzzle.
    """
    grid_nums = []

    start_row = row_num - (row_num % 3)
    start_col = col_num - (col_num % 3)

    for row in range(start_row, start_row + 3):  # loops through 3 consecutive rows
        for col in range(start_col, start_col + 3):  # loops through 3 consecutive columns within each row
            grid_nums.append(puzzle[row][col])

    return grid_nums


def pick_input_num(puzzle, row_num, col_num, chosen_num=1):
    """
    Calculates and returns a number over 0 (ideally 1-9) that can be inputted into a slot of the puzzle.
    This is done by checking if the chosen number to be inputted exists in the same row, column, or grid.

    Arguments:
        puzzle (list[list[int]]): 2D List of integers representing a sudoku puzzle.
        row_num (int): A row number from the puzzle.
        col_num (int): A column number from the puzzle.

    Keyword Arguments:
        chosen_num (int): Next possible value that can be inputted into a slot of the puzzle
        (default = 1).

    Returns:
        int: The number that was chosen to be inputted into a slot of the puzzle.
    """

    """
    Takes in the current row and column of the slot as well as the next possible number that can be
    inputted into the slot (1 by default)."""
    if chosen_num < 10:
        col = current_col(puzzle, col_num)
        grid = current_grid(puzzle, row_num, col_num)

        while chosen_num in puzzle[row_num] or chosen_num in col or chosen_num in grid:
            chosen_num += 1

    return chosen_num


def appears_after(input_row, input_col, target_row, target_col):
    """
    Checks if the input slot appears after the target slot and returns a boolean.

    Arguments:
        input_row (int): The row number of the slot being checked
        input_col (int): The col number of the slot being checked
        target_row (int): The row number of the slot being compared to
        target_col (int): The col number of the slot being compared to

    Returns:
        boolean: True, if the input slot appears after the target slot, False otherwise.
    """
    if input_row > target_row:  # if we are on a row after the target row
        return True
    elif input_row == target_row:  # if we are on the same row as the target row
        if input_col > target_col:  # and, if we are on a column after the target column
            return True
        else:
            return False
    else:  # lastly, if we are on a row before the target row
        return False


def find_previous_slot(fixed_num_locations, row_num, col_num):
    """
    Finds the previous slot of the puzzle from the current one by ensuring:
        - the slot that is found does not contain a fixed number from the beginning of the puzzle.

    Arguments:
        fixed_num_locations (dict(int: list[int])): Key - row number, Value - list of column numbers.
            - these column numbers within each row number represent the locations where there is a number
            that can't be changed, since it was provided from the start.

        row_num (int): A row number from the puzzle.
        col_num (int): A column number from the puzzle.

    Returns:
        dict(str: int): Represents the slot that was found through a key, value pair of a row and column.
            - {"row": row_num, "col": col_num}
    """
    while True:
        col_num = (col_num + 8) % 9  # % 9 restricts the number within the range (0-9)

        if col_num == 8:  # col_num 8 means we are now at the previous row
            row_num -= 1

        if col_num not in fixed_num_locations[row_num]:
            break

    return {"row": row_num, "col": col_num}


def find_next_slot(fixed_num_locations, row_num, col_num):
    """
    Finds the next slot of the puzzle from the current one by ensuring:
        - the slot that is found does not contain a fixed number from the beginning of the puzzle.

    Arguments:
        fixed_num_locations (dict(int: list[int])): Key - row number, Value - list of column numbers.
            - these column numbers within each row number represent the locations where there is a number
            that can't be changed, since it was provided from the start.
        row_num (int): A row number from the puzzle.
        col_num (int): A column number from the puzzle.

    Returns:
        dict(str: int): Represents the slot that was found through key, value pairs of a row and column.
            - {"row": row_num, "col": col_num}
    """
    while True:
        col_num = (col_num + 1) % 9  # % 9 restricts the number within the range (0-9)

        if col_num == 0:  # col_num 0 means we are now at the next row
            row_num += 1

        if col_num not in fixed_num_locations[row_num]:
            break

    return {"row": row_num, "col": col_num}


def modify_previous_slots(puzzle, fixed_num_locations, start_row_num, start_col_num, end_row_num, end_col_num):
    """
    Modifies all slots beginning at a starting slot, and ending either:
        1) When any of the slots were modified incorrectly, that is an invalid number was entered. Or,
        2) When the ending slot was reached succesfully, that is all numbers preceeding it were valid.

    Arguments:
        puzzle (list[list[int]]): 2D List of integers representing a sudoku puzzle.
        fixed_num_locations (dict(int: list[int])): Key - row number, Value - list of column numbers.
            - these column numbers within each row number represent the locations where there is a number
            that can't be changed, since it was provided from the start.
        start_row_num (int): A row number from the puzzle, representing the starting slot.
        start_col_num (int): A column number from the puzzle, representing the starting slot.
        end_row_num (int): A row number from the puzzle, representing the ending slot.
        end_col_num (int): A column number from the puzzle, representing the ending slot.

    Returns:
        dict(str: int): A dictionary with key, value pairs representing the last number that was entered,
        as well as the row and column that it ended on.
            - {"num": current_num, "row": current_row, "col": current_slot}
    """
    current_num = puzzle[start_row_num][start_col_num]
    current_row = start_row_num
    current_slot = start_col_num

    while current_num < 10:  # keep modifying until you enter an invalid number in a slot
        next_slot = find_next_slot(fixed_num_locations, current_row, current_slot)
        current_row = next_slot["row"]
        current_slot = next_slot["col"]

        # make sure that the slot being modified does not appear after the current slot in the main program
        if not appears_after(current_row, current_slot, end_row_num, end_col_num):
            current_num = pick_input_num(puzzle, current_row, current_slot)

            if current_num < 10:
                puzzle[current_row][current_slot] = current_num
        else:  # if it appears after, we know to stop here and continute with solving the rest of the puzzle
            break

    return {"num": current_num, "row": current_row, "col": current_slot}


def solve_sudoku(puzzle, fixed_num_locations):
    """
    Solves the sudoku puzzle that was passed into it, by modifying its entries.

    Arguments:
        puzzle (list[list[int]]): 2D List of integers representing a sudoku puzzle.
        fixed_num_locations (dict(int: list[int])): Key - row number, Value - list of column numbers.
            - these column numbers within each row number represent the locations where there is a number
            that can't be changed, since it was provided from the start.

    Returns:
        None
    """
    for row in range(len(puzzle)):
        for index, slot in enumerate(puzzle[row]):
            if slot == 0:
                puzzle[row][index] = pick_input_num(puzzle, row, index)

            current_row = row
            current_index = index
            current_num = puzzle[current_row][current_index]

            while current_num > 9:  # if we entered an invalid number
                previous_slot = find_previous_slot(fixed_num_locations, current_row, current_index)

                current_row = previous_slot["row"]
                current_index = previous_slot["col"]
                current_num = pick_input_num(puzzle, current_row, current_index, puzzle[current_row][current_index] + 1)

                puzzle[current_row][current_index] = current_num

                if current_num < 10:  # if we could enter a valid number in the previous slot
                    # modify all slots in between that slot and the slot we are currently on in the for loop
                    new_slot = modify_previous_slots(puzzle, fixed_num_locations, current_row, current_index, row, index)

                    current_num = new_slot["num"]
                    current_row = new_slot["row"]
                    current_index = new_slot["col"]
