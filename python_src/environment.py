import math

from state import *


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_state = State(width, height)

    def can_move_n_steps_forward(self, state, y, max_height_black, max_height_white):
        if state.white_turn and y <= max_height_white: return True
        if not state.white_turn and y >= max_height_black: return True
        return False

    def get_moves(self, state, moves, captures, y, x):
        opponent = BLACK if state.white_turn else WHITE
        one_step = 1 if state.white_turn else -1
        two_steps = 2 if state.white_turn else -2

        # two steps forward and one step left/right

        if self.can_move_n_steps_forward(state=state, y=y, max_height_black=2, max_height_white=self.height - 3):
            if x > 0 and state.board[y + two_steps][x - 1] == EMPTY:
                moves.append((x, y, x - 1, y + two_steps))

            if x < self.width - 1 and state.board[y + two_steps][x + 1] == EMPTY:
                moves.append((x, y, x + 1, y + two_steps))

        # one step forward and two steps left/right
        # and also captures
        if self.can_move_n_steps_forward(state=state, y=y, max_height_black=1, max_height_white=self.height - 2):
            if x > 1 and state.board[y + one_step][x - 2] == EMPTY:
                moves.append((x, y, x - 2, y + one_step))

            if x < self.width - 2 and state.board[y + one_step][x + 2] == EMPTY:
                moves.append((x, y, x + 2, y + one_step))

            if x > 0 and state.board[y + one_step][x - 1] == opponent:
                captures.append((x, y, x - 1, y + one_step))

            if x < self.width - 1 and state.board[y + one_step][x + 1] == opponent:
                captures.append((x, y, x + 1, y + one_step))


    def get_legal_moves(self, state):
        moves = []
        captures = []
        friendly = WHITE if state.white_turn else BLACK

        start_index = self.height-1 if state.white_turn else 0
        end_index = -1 if state.white_turn else self.height
        step = -1 if state.white_turn else 1

        for y in range(start_index, end_index, step):
            for x in range(self.width):
                if state.board[y][x] == friendly:
                    self.get_moves(state, moves, captures, y, x)
        return captures + moves

    def move(self, state, move):
        try:
            x1, y1, x2, y2 = move
            state.board[y2][x2], state.board[y1][x1] = state.board[y1][x1], EMPTY
            state.white_turn = not state.white_turn
        except:
            raise IndexError

    def was_diagonal_move(self, move):
        x1, y1, x2, y2 = move

        if y2 - 1 == y1 and x2 - 1 == x1:
            return True

        if y2 - 1 == y1 and x2 + 1 == x1:
            return True

        if y2 + 1 == y1 and x2 - 1 == x1:
            return True

        if y2 + 1 == y1 and x2 + 1 == x1:
            return True
        return False

    def undo_move(self, state, move):
        x1, y1, x2, y2 = move

        if self.was_diagonal_move(move):
            if state.white_turn:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], WHITE
            else:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], BLACK
        else:
            state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], state.board[y1][x1]

        state.white_turn = not state.white_turn

    def valueFunction(self, state, role):
        """
        # given heuristic
        if "W" in state.board[-1]:
            return 100
        if "B" in state.board[0]:
            return -100
        if len(self.get_legal_moves(state)) == 0:
            return 0

        white_dist = 0
        black_dist = 0

        for i in range(self.height):
            for j in range(self.width):
                if state.board[i][j] == "W":
                    white_dist = max(white_dist, i)
                elif state.board[i][j] == "B":
                    black_dist = max(black_dist, self.height - 1 - i)

        return black_dist - white_dist
        """
        val = 0

        if "W" in state.board[-1]:
            val += 1000
            
        if "B" in state.board[0]:
            val -= 1000

        # reward for positions in the middle of the board like in real chess
        for row in state.board[2:self.height - 2]:
            midja = row[math.floor(self.width / 2)-1:math.ceil(self.width / 2)+1]
            if self.width == 3:
                midja = [row[1]]
            elif self.width < 3:
                break

            if "W" in midja:
                val += 10
            if "B" in midja:
                val -= 10

        #correct the values for different roles
        if role == 'black':
            return -val
        return val

