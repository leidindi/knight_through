# Define constants for the players and empty spaces on the board
WHITE, BLACK, EMPTY = "W", "B", " "


class State:
    # Constructor for the State class that initializes the board and whose turn it is
    def __init__(self, width, height):
        # Create the board as a 2D array of the given width and height
        self.board = [
            # First two rows are filled with WHITE pieces
            [WHITE] * width if i < 2 else
            # Last two rows are filled with BLACK pieces
            [BLACK] * width if i > height - 3 else
            # All other rows are initially empty
            [EMPTY] * width for i in range(height)]

        # Set the turn to be for WHITE to start
        self.white_turn = True

        # Store the width of the board for later use
        self.width = width
        self.height = height

    def __str__(self):
        # Calculate the length of the dashes to use in the string
        dash_count = self.width * 4 - 3
        # Create a line of dashes to use as separators between rows
        line = "\n" + "-" * dash_count + "\n"
        # Join each row with the separator and return the result
        return line.join([" | ".join([cell for cell in row]) for row in self.board[::-1]])