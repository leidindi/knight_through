import random
import time

#############

"""Agent acting in some environment"""


class Agent(object):

    # this method is called on the start of the new environment
    # override it to initialise the agent
    def start(self, role, width, height, play_clock):
        print("start called")
        return

    # this method is called on each time step of the environment
    # it needs to return the action the agent wants to execute as a string
    def next_action(self, last_move):
        print("next_action called")
        return "NOOP"

    # this method is called when the environment has reached a terminal state
    # override it to reset the agent
    def cleanup(self, last_move):
        print("cleanup called")
        return


#############

"""A random Agent for the KnightThrough game

 RandomAgent sends actions uniformly at random. In particular, it does not check
 whether an action is actually useful or legal in the current state.
 """


class RandomAgent(Agent):
    role = None
    play_clock = None
    my_turn = False
    width = 0
    height = 0

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
        # TODO: add your own initialization code here
        return

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move

            # Here we just construct a random move (that will most likely not even be possible),
            # this needs to be replaced with the actual best move.
            x1 = random.randint(1, self.width)
            x2 = x1 + random.randint(1, 2) * random.choice([-1, 1])
            y1 = random.randint(1, self.height)
            direction = 1
            if self.role == 'black':
                direction = -1
            y2 = y1 + direction * random.randint(1, 2)
            return "(move " + " ".join(map(str, [x1, y1, x2, y2])) + ")"
        else:
            return "noop"


