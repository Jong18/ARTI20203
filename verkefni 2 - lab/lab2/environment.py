import math
from enum import IntEnum
import random
import itertools


##############

class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # this allows things like: Orientation.NORTH + 1 == Orientation.EAST
    def __add__(self, i):
        orientations = list(Orientation)
        return orientations[(int(self) + i) % 4]

    def __sub__(self, i):
        orientations = list(Orientation)
        return orientations[(int(self) - i) % 4]


##############

class State:
    # Note, that you do not necessarily have to use this class if you find a
    # different data structure more useful as state representation.
    def __init__(self, turned_on=False, position=(0, 0), dirts_left=(), orientation=Orientation.NORTH):
        self.turned_on = turned_on
        self.position = position
        self.dirts_left = dirts_left
        self.orientation = orientation

    def __str__(self):
        return f"State: ({str(self.turned_on)}, {self.position}, {self.dirts_left}, {self.orientation})"

    def __hash__(self):
        # im splicing the static elements off of the string, they don't contribute anything to the quality of the hash
        # I chose to use the inbuilt functions for simplicity, I know good hash functions are difficult. So i decided
        # to keep it simple
        return hash(str(self)[7:-1])

    def __eq__(self, other):
        return str(self) == str(other)


##############

class Environment:
    def __init__(self, width=0, height=0, nb_dirts=0):
        self._width = width
        self._height = height
        # That is, the starting position, orientation and position of the dirty cells should be (somewhat) random.
        # for example as shown here:
        # generate all possible positions
        self.all_positions = list(itertools.product(range(1, self._width + 1), range(1, self._height + 1)))
        # randomly choose a home location
        self.home = random.choice(self.all_positions)
        # randomly choose locations for dirt
        self.dirts = random.sample(self.all_positions, nb_dirts)

    def get_initial_state(self):
        return State(False, self.home, tuple(self.dirts), Orientation.NORTH)

    def get_legal_actions(self, state):
        actions = []
        if not state.turned_on:
            actions.append("TURN_ON")
        else:
            if state.position == self.home:  # should be only possible when agent has returned home
                actions.append("TURN_OFF")
            if state.position in state.dirts_left:  # should be only possible if there is dirt in the current position
                actions.append("SUCK")

            # this is to make a fake "go" command beforehand and check if its valid
            nextposition = list(state.position)
            if state.orientation == Orientation.NORTH:
                nextposition[1] += 1
            elif state.orientation == Orientation.SOUTH:
                nextposition[1] -= 1
            elif state.orientation == Orientation.EAST:
                nextposition[0] += 1
            elif state.orientation == Orientation.WEST:
                nextposition[0] -= 1
            nextposition = tuple(nextposition)

            if nextposition in self.all_positions:
                # if its valid I'll allow the action
                actions.append("GO")

            # always allowed
            actions.append("TURN_LEFT")
            actions.append("TURN_RIGHT")
        return actions

    def get_next_state(self, state, action):
        if action == "TURN_ON":
            return State(True, state.position, state.dirts_left, state.orientation)
        elif action == "TURN_OFF":
            return State(False, state.position, state.dirts_left, state.orientation)
        elif action == "TURN_LEFT":
            return State(state.turned_on, state.position, state.dirts_left, state.orientation - 1)
        elif action == "TURN_RIGHT":
            return State(state.turned_on, state.position, state.dirts_left, state.orientation + 1)
        elif action == "GO":
            nextposition = list(state.position)
            if state.orientation == Orientation.NORTH:
                nextposition[1] += 1
            elif state.orientation == Orientation.SOUTH:
                nextposition[1] -= 1
            elif state.orientation == Orientation.EAST:
                nextposition[0] += 1
            elif state.orientation == Orientation.WEST:
                nextposition[0] -= 1
            nextposition = tuple(nextposition)
            return State(state.turned_on, nextposition, state.dirts_left, state.orientation)
        elif action == "SUCK":
            try:
                dirtlist = list(state.dirts_left)
                dirtlist.pop(dirtlist.index(state.position))
                dirttuple = tuple(dirtlist)
            except ValueError:
                # I had errors regarding "suck", that's why it's here.
                # but this error catcher is not necessary, but it could be in the future so I want to leave it in just
                # in case.
                print()
                print("----------------------------------------------------")
                print("THERE WAS NO DIRT WHEN TRYING TO SUCK")
                print("dirtlisti:" + str(dirtlist))
                print("position nuna:" + str(state.position))
                print("----------------------------------------------------")
                print()
                dirttuple = state.dirts_left
            return State(state.turned_on, state.position, dirttuple, state.orientation + 1)

        else:
            raise Exception("Unknown action %s" % str(action))

    def get_cost(self, state, action):
        # the scores as described
        if action == "TURN_OFF" and state.position == self.home:
            return 1 + 50 * len(state.dirts_left)
        elif action == "TURN_OFF" and state.position != self.home:
            return 100 + 50 * len(state.dirts_left)
        elif action == "SUCK" and not (state.position in self.dirts):
            return 5
        elif action == "SUCK" and state.position in self.dirts:
            return 1
        else:
            return 1

    def is_goal_state(self, state):
        if state.position == self.home and len(state.dirts_left) == 0 and state.orientation == Orientation.NORTH:
            return True
        else:
            return False


##############

def expected_number_of_states(width, height, nb_dirts):
    # state_basic is the position the agent can be positioned in on the grid, multiplied by the possible orientations,
    # multiplied with the on or off possibility.
    orientiations = 4
    onoroff = 2
    state_basic = width * height * orientiations * onoroff

    # this tries to take into account all the possible different setups the pieces of dirt could randomly be placed on
    # our grid structure
    combinatorics = math.factorial(width * height) / (
                math.factorial(nb_dirts) * math.factorial(width * height - nb_dirts))

    ive_over_complicated_this = True
    if ive_over_complicated_this:
        # states depending on how many pieces of dirt are left
        combinatorics = math.pow(2, nb_dirts)
    return state_basic * combinatorics
