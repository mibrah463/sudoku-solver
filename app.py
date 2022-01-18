from solver import solve_sudoku
import tkinter as tk


class Sudoku:
    """
    A Sudoku class to represent a sudoku solver application.

    ...

    Class Attributes
    ----------------
    PUZZLE_SIZE: int
        The square canvas size that the sudoku puzzle fits in.
    MARGIN: float
        The margin length between the edges of the puzzle board and the window of the app.
    LINE_SPACE: float
        The space between the borders of each cell.

    Attributes
    ----------
    master: Tk
        The tk() object that creates the root window of the app.
    canvas: Tk.Canvas
        The canvas that contains the main sudoku puzzle board.
    solve_button: Tk.Button
        The solve button that exists below the puzzle and solves it.
    reset_button: Tk.Button
        The reset button that exists below the puzzle and resets it.
    puzzle_nums: list(list(int))
        2D list that contains the sudoku puzzle with all its entries.
    fixed_num_locations: dict(int: list[int])
        Dictionary that contains the row numbers as keys, and a list of column numbers as values
        that determine the cells that contain a number that can't be changed.

    Methods
    -------
    draw_cells():
        Draws all the cells of the sudoku board.
    add_buttons():
        Adds the solve and reset buttons below the board.
    reset_puzzle():
        Resets the sudoku puzzle by clearing the board.
    puzzle_is_empty():
        Checks if the entire board is empty (no entries in the puzzle).
    change_cell_num(event):
        Changes the number entered in the cell that is clicked.
    display_cell_change(row_num, col_num, display_num):
        Displays the new number that is entered on a cell after it is clicked on.
    click_solve():
        Solves the sudoku puzzle and displays it on the board.
    """

    PUZZLE_SIZE = 550

    MARGIN = PUZZLE_SIZE / 11
    LINE_SPACE = (PUZZLE_SIZE - MARGIN) / 10

    def __init__(self, master):
        """
        Constructs all the attributes of the Sudoku object, by calling helper methods.

        Arguments
        ----------
        master: Tk
            The tk() object that creates the root window of the app.
        """

        self.master = master

        self.master.resizable(False, False)
        self.master.title("Sudoku Solver")
        self.master.geometry(f"{Sudoku.PUZZLE_SIZE}x{Sudoku.PUZZLE_SIZE + int(Sudoku.MARGIN) * 2}")
        self.master.configure(bg="white")

        self.canvas = tk.Canvas(self.master, width=Sudoku.PUZZLE_SIZE, height=Sudoku.PUZZLE_SIZE)
        self.canvas.pack()

        self.draw_cells()
        self.add_buttons()
        self.reset_puzzle()

        self.canvas.bind("<Button-1>", self.change_cell_num)

    def draw_cells(self):
        """
        Draws all the cells of the sudoku board.

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        for line in range(10):
            new_line_pos = line * Sudoku.LINE_SPACE + Sudoku.MARGIN

            if line % 3 == 0:
                # highlight the grids
                line_width = 3
                color = "navyblue"
            else:
                line_width = 1
                color = "black"

            self.canvas.create_line(
                Sudoku.MARGIN,
                new_line_pos,
                Sudoku.PUZZLE_SIZE - Sudoku.MARGIN,
                new_line_pos,
                width=line_width,
                fill=color,
            )  # horizontal lines
            self.canvas.create_line(
                new_line_pos,
                Sudoku.MARGIN,
                new_line_pos,
                Sudoku.PUZZLE_SIZE - Sudoku.MARGIN,
                width=line_width,
                fill=color,
            )  # vertical lines

    def add_buttons(self):
        """
        Creates and adds the solve and reset buttons below the sudoku board.

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        button_width = Sudoku.PUZZLE_SIZE / Sudoku.MARGIN * 2
        button_height = Sudoku.PUZZLE_SIZE / Sudoku.MARGIN

        self.solve_button = tk.Button(
            self.master,
            text="Solve",
            padx=button_width,
            pady=button_height,
            bg="light blue",
            fg="black",
            borderwidth=3,
            font="sans 16 bold",
            state=tk.DISABLED,
            command=self.click_solve,
        )
        self.solve_button.place(x=Sudoku.PUZZLE_SIZE / 2 - button_width * 7, y=Sudoku.PUZZLE_SIZE + Sudoku.MARGIN / 3)

        self.reset_button = tk.Button(
            self.master,
            text="Reset",
            padx=button_width,
            pady=button_height,
            bg="light blue",
            fg="black",
            borderwidth=3,
            font="sans 16 bold",
            state=tk.DISABLED,
            command=self.reset_puzzle,
        )
        self.reset_button.place(x=Sudoku.PUZZLE_SIZE / 2 + button_width * 2, y=Sudoku.PUZZLE_SIZE + Sudoku.MARGIN / 3)

    def reset_puzzle(self):
        """
        Resets the sudoku puzzle by:
            1) Clearing all cells of the sudoku puzzle visually.
            2) Setting all entries in puzzle_nums to 0.
            3) Emptying each value list that exists within each key of fixed_num_locations.

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        self.puzzle_nums = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.fixed_num_locations = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
        }

        for row in range(len(self.puzzle_nums)):
            for cell in range(len(self.puzzle_nums[row])):
                self.canvas.delete(f"number{row}{cell}")  # delete all entries within all clots

        self.solve_button["state"] = tk.DISABLED
        self.reset_button["state"] = tk.DISABLED

    def puzzle_is_empty(self):
        """
        Checks if the sudoku puzzle is empty, that is if all values for each key in fixed_num_locations
        are empty lists.

        Arguments
        ---------
        None

        Returns
        -------
        boolean:
            True, if the puzzle is empty, False otherwise.
        """

        is_empty = True

        for key in self.fixed_num_locations:
            if self.fixed_num_locations[key] != []:  # if we have any slot within any row that has a number
                is_empty = False
                break

        return is_empty

    def change_cell_num(self, event):
        """
        Changes the number of the cell that was clicked on,
        as well as modifies the puzzle list and its fixed_num_locations.

        Arguments
        ---------
        event: Tk.Event
            A mouse click event that reprsents where on the canvas/board the mouse was clicked.

        Returns
        -------
        None
        """

        mouse_x = event.x
        mouse_y = event.y

        # if we clicked somewhere within the sudoku board/canvas
        if Sudoku.MARGIN < mouse_x < (Sudoku.PUZZLE_SIZE - Sudoku.MARGIN) and Sudoku.MARGIN < mouse_y < (
            Sudoku.PUZZLE_SIZE - Sudoku.MARGIN
        ):
            row = int((mouse_y - Sudoku.MARGIN) // Sudoku.LINE_SPACE)
            col = int((mouse_x - Sudoku.MARGIN) // Sudoku.LINE_SPACE)

            new_cell_num = (self.puzzle_nums[row][col] + 1) % 10  # next number can't be greater than 9
            self.puzzle_nums[row][col] = new_cell_num

            if col in self.fixed_num_locations[row]:
                self.fixed_num_locations[row].remove(col)  # Don't repeat values within that list

            if new_cell_num != 0:
                self.fixed_num_locations[row].append(col)

            self.display_cell_change(row, col, new_cell_num)

    def display_cell_change(self, row_num, col_num, display_num):
        """
        Displays the change in a cell by showing its new number entry.

        Arguments
        ---------
        row_num: int
            The row number of the cell that needs displaying.
        col_num: int
            The column number of the cell that needs displaying.
        display_num: int
            The new entry number to be displayed

        Returns
        -------
        None
        """

        self.canvas.delete(f"number{row_num}{col_num}")

        if display_num != 0:
            # calculate the center (x, y) coordinates of the slot that needs to display the number
            text_pos_x = col_num * Sudoku.LINE_SPACE + Sudoku.MARGIN + (Sudoku.LINE_SPACE / 2)
            text_pos_y = row_num * Sudoku.LINE_SPACE + Sudoku.MARGIN + (Sudoku.LINE_SPACE / 2)

            self.canvas.create_text(text_pos_x, text_pos_y, text=str(display_num), font="arial", tags=f"number{row_num}{col_num}")
            self.solve_button["state"] = tk.NORMAL
            self.reset_button["state"] = tk.NORMAL
        else:
            if self.puzzle_is_empty():  # if changing the cell number makes the whole board empty
                self.solve_button["state"] = tk.DISABLED
                self.reset_button["state"] = tk.DISABLED

    def click_solve(self):
        """
        Solves the sudoku puzzle, as well as displaying it visually
        by entering appropriate values within each cell.

        Arguments
        ---------
        None

        Returns
        -------
        None
        """

        solve_sudoku(self.puzzle_nums, self.fixed_num_locations)

        for row in range(len(self.puzzle_nums)):
            for col in range(len(self.puzzle_nums[row])):
                self.display_cell_change(row, col, self.puzzle_nums[row][col])

        self.solve_button["state"] = tk.DISABLED


if __name__ == "__main__":
    window = tk.Tk()
    sudoku_solver = Sudoku(window)
    window.mainloop()
