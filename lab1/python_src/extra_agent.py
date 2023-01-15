from copy import deepcopy
from agent import Agent
from enum import IntEnum

class Orientation(IntEnum):
    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3,

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    """ To debug """
    def __str__(self):
        return f"Point(x={self.x}, y={self.y})"

    """ Check  if position is home """
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    """ Check if position has been visited """
    def __hash__(self):
        return hash((self.x, self.y))
    
    """ Update the position of the agent """
    def move(self, orientation, step=1):
        if orientation == Orientation.NORTH:
            self.y += step
        elif orientation == Orientation.EAST:
            self.x += step
        elif orientation == Orientation.SOUTH:
            self.y -= step
        elif orientation == Orientation.WEST:
            self.x -= step


class VacuumAgent(Agent):
    def __init__(self):
        self.position = Point()
        self.home = Point()
        self.orientation = Orientation.NORTH
        self.turned_on = False
        self.visited = {self.home}
        self.bump_counter = 0
        self.x_min = 0
        self.x_max = 0
        self.y_max = 0
        self.y_min = 0
        self.grid_size = 0

    def turn_off(self):
        self.turned_on = False
        return "TURN_OFF"

    def turn_on(self):
        self.turned_on = True
        return "TURN_ON"

    def cleanup(self, percepts):
        self.orientation = Orientation.NORTH
        self.turned_on = False
        self.visited = {self.home}
        self.bump_counter = 0
        self.x_min = 0
        self.x_max = 0
        self.y_max = 0
        self.y_min = 0
        self.grid_size = 0

    def turn_left(self):
        self.orientation = (self.orientation - 1) % 4
        return "TURN_LEFT"

    def turn_right(self):
        self.orientation = (self.orientation + 1) % 4
        return "TURN_RIGHT"

    def go(self):
        self.position.move(self.orientation)
        self.visited.add(deepcopy(self.position))
        return "GO"

    def undo_move(self):
        self.visited.remove(self.position)
        self.position.move(self.orientation, -1)
    
    """ Do a spiral move around the grid, decreasing the bounds in each iteration """
    def spiral_move(self):
        if self.position.x == self.x_max - 1: 
            self.x_max -= 1
            return self.turn_right()
        elif self.position.x == self.x_min + 1:
            self.x_min += 1
            return self.turn_right()
        elif self.position.y == self.y_min + 1:
            self.y_min += 1
            return self.turn_right()
        elif self.position.y == self.y_max - 1:
            self.y_max -= 1
            return self.turn_right()
        else:
            return self.go()

    """ Brute force to get to home position """
    def go_home(self):
        while self.position != self.home:
            self.go()
            if self.position.x == self.x_max - 1:
                self.turn_left()
            if self.position.x == self.x_min + 1:
                self.turn_right()
            if self.position.y == self.y_max - 1:
                self.turn_left()
            if self.position.y == self.y_min + 1:
                self.turn_right()
        return self.turn_off()


    def next_action(self, percepts):
        print(f"Percepts: {percepts}")

        if not self.turned_on:
            return self.turn_on()

        if "DIRT" in percepts:
            return "SUCK"

        self.finished_cells = 0 < self.grid_size == len(self.visited)

        if self.finished_cells :
            return self.go_home()
        
        if self.bump_counter == 5:
            return self.spiral_move()

        if "BUMP" in percepts:
            self.undo_move()
            self.bump_counter += 1
            if self.bump_counter == 1:
                self.y_max = self.position.y
            if self.bump_counter == 2:
                self.x_max = self.position.x
            if self.bump_counter == 3:
                self.y_min = self.position.y
            if self.bump_counter == 4:
                self.x_min = self.position.x  
            if self.bump_counter == 4:
                self.grid_size = ((self.y_min - self.y_max) - 1) * ((self.x_min - self.x_max) - 1)
                return self.turn_right
            if self.bump_counter < 5:
                return self.turn_right()

        if self.position not in self.visited:
            return self.go()
