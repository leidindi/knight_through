import time

# import necessary classes
from agent import Agent
from environment import *
from copy import deepcopy
import math
from hashmap import HashMap

# create MyAgent class that extends the Agent class
class MyAgent(Agent):

    # define constructor for MyAgent
    def __init__(self):
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0
        self.env = None
        self.initialtime = 0
        self.timenow = 0
        self.hashmap = HashMap()
        self.hversuoftnotad = 0

    # check if the game has reached a terminal state
    def terminalstate(self, state, number_of_moves):
        if "B" in state.board[0] or "W" in state.board[-1] or number_of_moves == 0:
            return True
        return False

    # perform minimax search to determine the best move
    def minimax(self, state, alpha, beta, depth):

        # check if time limit has been reached
        self.timenow = time.time_ns() - self.initialtime
        self.timenow = self.timenow / math.pow(10, 9)
        if self.timenow >= self.play_clock - 0.1:
            raise TimeoutError

        # get legal moves and check if the current state is a terminal state
        legal_moves = self.env.get_legal_moves(state)
        if self.terminalstate(state, len(legal_moves)) or depth <= 0:
            if len(legal_moves) == 0:
                # making negative incentive for making a draw
                # better than a defeat, but need to make it negatively impact the end result
                return -50
            return self.env.valueFunction(state, self.role)

        # if it's white's turn, maximize the value of the node
        if state.white_turn:
            best_value = -float('inf')
            try:
                stored_state = self.hashmap.get(state=state, role=self.role)
                if stored_state[0] <= depth:
                    best_move, best_value = stored_state[1], stored_state[2]
                    self.hversuoftnotad += 1
                    return best_value
            except KeyError:
                pass
            for move in legal_moves:
                # perform the move, calculate its value, and undo the move
                self.env.move(state, move)
                value = self.minimax(state, alpha, beta, depth - 1)
                self.env.undo_move(state, move)

                # update the best value and alpha
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                # check if beta is less than or equal to alpha and break out of the loop
                if beta <= alpha:
                    break

            return best_value

        # if it's black's turn, minimize the value of the node
        else:
            best_value = float('inf')
            try:
                stored_state = self.hashmap.get(state=state, role=self.role)
                if stored_state[0] <= depth:
                    best_move, best_value = stored_state[1], stored_state[2]
                    self.hversuoftnotad += 1
                    return best_value
            except KeyError:
                pass
            for move in legal_moves:
                # perform the move, calculate its value, and undo the move
                self.env.move(state, move)
                value = self.minimax(state, alpha, beta, depth - 1)
                self.env.undo_move(state, move)

                # update the best value and beta
                best_value = min(best_value, value)
                beta = min(beta, best_value)

                # check if beta is less than or equal to alpha and break out of the loop
                if beta <= alpha:
                    break

            return best_value

    # perform minimax search with iterative deepening and return the best move and its value
    def minimax_root(self, state, alpha, beta, depth):
        best = -float('inf')
        bestmove = "Finnur ekki move"

        # check if the current state and role have already been visited at a deeper depth

        legal_moves = self.env.get_legal_moves(state)
        # Get all legal moves for the current state
        try:
            stored_state = self.hashmap.get(state=state, role=self.role)
            if stored_state[0] == depth:
                best_move, best_value = stored_state[1], stored_state[2]
                self.hversuoftnotad += 1
                return best_move, best_value
        except KeyError:
            pass

        for move in legal_moves:
            # Evaluate each possible move from the current state
            self.env.move(state, move)
            # Make the move on a copy of the current state
            value = self.minimax(state, alpha, beta, depth - 1)
            # Recursively evaluate the next state with the opposite role
            self.env.undo_move(state, move)
            # Undo the move on the copy of the current state

            if not bestmove or value > best:
                # If this move is better than the previous best move, update the best move and value
                best = value
                bestmove = move
            alpha = max(alpha, best)
            # Update the alpha value
            if beta <= alpha:
                # If beta is less than or equal to alpha, prune the search
                break
        self.hashmap.insert(state=state, role=self.role, depth=depth, move=bestmove, value=best)
        # Save the best move and value for this state
        return bestmove, best
        # Return the best move and its value

    def get_best_move(self):
        best_move = "Fann ekki move"
        # This string should in all cases be handled, either given a move or dealt with as an error
        # it has this value so that it is easier to find where the error originated from
        alpha = -float('inf')
        best = alpha
        beta = float('inf')
        depth = 1
        state = deepcopy(self.env.current_state)
        # Copy the current state to avoid modifying it
        self.initialtime = time.time_ns()
        # Set the initial time

        while True:
            try:
                tempobest_move, tempobest = self.minimax_root(state, alpha, beta, depth)
                # Find the best move and its value for the current depth
                if tempobest >= best:
                    # If this move is better than the previous best move, update the best move and value
                    best_move = tempobest_move
                    best = tempobest
                    self.hashmap.insert(state=state, role=self.role, depth=depth, move=best_move, value=best)
                    # Save the best move and value for this state
                #print("D:" + str(depth) + "\tM:" + str(tuple([x + 1 for x in best_move])) + "\tV:" + str(best))
                # Print the depth, move, and value of the best move
                depth += 1
                # Increment the depth for the next search
                if depth > 30 or best >= 200:
                    # If the depth is greater than 30 or the best value is greater than or equal to 200, break the loop
                    # the depth should never reach so deep
                    # if a big map has gone this deep you've either had an error or you've already solved the map

                    # also if the best move has a value above you've solved the map already.
                    break
            except TimeoutError:
                # If the search times out, return the best move found so far

                # this is "belti + axlabönd", this is here incase the terminalstate function fails ( then I send
                # the move of the furthest piece ( this has usually been the victory move final step))
                if best_move == "Fann ekki move":
                    return self.env.get_legal_moves(state)[0]
                break

        if best_move == "Fann ekki move":
            pass
        return best_move

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        self.env = Environment(width, height)

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            self.env.move(self.env.current_state, [i - 1 for i in last_action])
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            move = self.get_best_move()
            #print("Hversu oft notað : " + str(self.hversuoftnotad))
            #print("Stærð hashmaps: " + str(self.hashmap.num_items))

            return "(move " + " ".join(map(str, [i + 1 for i in move])) + ")"
            # send the move first, then update your own world
            # if the move is not legal the game player will give you a random move
        else:
            return "noop"

    # this method is called when the environment has reached a terminal state
    # override it to reset the agent
    def cleanup(self, last_move):
        print("cleanup called")
        return

