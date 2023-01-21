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

  # TODO: add other attributes that store necessary information about a state of the environment
  #       Only information that can change over time should be kept here.
  def __init__(self, turned_on = False, position=(0,0),dirts_left=(),orientation=Orientation.NORTH):
  # TODO: add other attributes that store necessary information about a state of the environment
    self.turned_on = turned_on
    self.position = position
    self.dirts_left = dirts_left
    self.orientation = orientation

  def __str__(self):
    # TODO: modify as needed
    return f"State: ({str(self.turned_on)}, {self.position}, {self.dirts_left}, {self.orientation})"

  def __hash__(self):
    # TODO: modify as needed
   return hash(str(self))

  def __eq__(self, other):
    # TODO: modify as needed
    return str(self) == str(other)

##############

class Environment:
  # TODO: add other attributes that store necessary information about the environment
  #       Information that is independent of the state of the environment should be here.
  def __init__(self, width = 0, height = 0, nb_dirts= 0):
    self._width = width
    self._height = height
    # TODO: randomly initialize an environment of the given size
    # That is, the starting position, orientation and position of the dirty cells should be (somewhat) random.
    # for example as shown here:
    # generate all possible positions
    all_positions = list(itertools.product(range(1, self._width+1), range(1, self._height+1)))
    # randomly choose a home location
    self.home = random.choice(all_positions)
    # randomly choose locations for dirt
    self.dirts = random.sample(all_positions, nb_dirts)
    return

  def get_initial_state(self):
    # TODO: return the initial state of the environment
    return State(False, self.home, tuple(self.dirts), Orientation.NORTH)

  def get_legal_actions(self, state):
    actions = []
    # TODO: check conditions to avoid useless actions
    if not state.turned_on:
      actions.append("TURN_ON")
    else:
      if True: # should be only possible when agent has returned home
        actions.append("TURN_OFF")
      if True: # should be only possible if there is dirt in the current position
        actions.append("SUCK")
      if True: # should be only possible when next position is inside the grid (avoid bumping in walls)
        actions.append("GO")
      actions.append("TURN_LEFT")
      actions.append("TURN_RIGHT")
    return actions

  def get_next_state(self, state, action):
    # TODO: add missing actions
    if action == "TURN_ON":
      return State(True)
    elif action == "TURN_OFF":
      return State(False)
    elif action == "TURN_LEFT":
      return State(state.turned_on, state.position, state.dirts_left, state.orientation - 1)
    elif action == "TURN RIGHT":
      return State(state.turned_on, state.position, state.dirts_left, state.orientation + 1)
    else:
      raise Exception("Unknown action %s" % str(action))

  def get_cost(self, state, action):
    # TODO: return correct cost of each action
    return 1

  def is_goal_state(self, state):
    # TODO: correctly implement the goal test
    return not state.turned_on

##############

def expected_number_of_states(width, height, nb_dirts):
  # TODO: return a reasonable upper bound on number of possible states
  return 2