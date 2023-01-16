from typing import Set

from agent import Agent
from enum import IntEnum
from copy import deepcopy

class Orientation(IntEnum):
    NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        """ For debugging """
        return f"Position: ({self.x}, {self.y})"

    def __hash__(self):
        """ To add position to a visited set """
        return hash(str(self))

    def __eq__(self, other):
        """ To check position == home """
        return self.x == other.x and self.y == other.y
    def __sub__(self, other):
        return self.y - other.y
    def move(self, orientation, step=1):
        """ Updates position (use if elif for python < 3.10) """
        match orientation:
            case Orientation.NORTH:
                self.y += step
            case Orientation.EAST:
                self.x += step
            case Orientation.SOUTH:
                self.y -= step
            case Orientation.WEST:
                self.x -= step

class MyAgent(Agent):

    def __init__(self):
        self.position = Point()
        self.home = deepcopy(Point())
        self.orientation = Orientation.NORTH
        self.turned_on = False
        self.ET_go_home = False

        self.visited = {self.home}

        self.turn_bool = False
        self.turn_count = 0
        self.turn_direction = "right"

        self.bump_counter = 0
        self.max_y = None
        self.min_y = None
        self.size = 1000000
        self.turn_occurances = 0





    def start(self):
        pass

    def cleanup(self, percepts):
        self.position = Point()
        self.home = Point()
        self.orientation = Orientation.NORTH
        self.turned_on = False
        self.ET_go_home = False

        self.visited = {self.home}

        self.turn_bool = False
        self.turn_count = 0
        self.turn_direction = "right"

        self.bump_counter = 0
        self.max_y = None
        self.min_y = None
        self.size = 1000000
        self.turn_occurances = 0


    def turn_on(self):
        self.turned_on = True
        return "TURN_ON"

    def turn_off(self):
        self.turned_on = False
        return "TURN_OFF"

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
    def next_action(self, percepts):
        print(f"Percepts: {percepts}")

        if not self.turned_on:
            return self.turn_on()

        if "DIRT" in percepts:
            return "SUCK"

        if ("BUMP" in percepts ) :
            self.undo_move()
            self.bump_counter += 1
            if self.bump_counter == 1:
                self.max_y = deepcopy(self.position)
                return self.turn_right()
            elif self.bump_counter == 2:
                return self.turn_right()
            elif self.bump_counter == 3:
                self.min_y = deepcopy(self.position)
                self.size = self.max_y - self.min_y
            else:
                if self.position.x == self.home.x and self.position.y == self.home.y and self.ET_go_home:
                    self.cleanup(percepts)
                    return self.turn_off()
                self.turn_bool = True

        if self.ET_go_home:
            if self.position.x == self.home.x and self.position.y == self.home.y:
                self.cleanup(percepts)
                return self.turn_off()
            elif self.position.x == self.home.x and self.position.y <= self.home.y:
                if self.orientation != Orientation.NORTH:
                    return self.turn_right()
            elif self.position.x == self.home.x and self.position.y >= self.home.y:
                if self.orientation != Orientation.SOUTH:
                    return self.turn_right()
            elif self.position.x < self.home.x:
                if self.orientation != Orientation.EAST:
                    return self.turn_right()
            elif self.position.x > self.home.x:
                if self.orientation != Orientation.WEST:
                    return self.turn_right()
            return self.go()

        if self.turn_occurances == self.size+1:
            self.turn_bool = False
            self.ET_go_home = True
            return self.go()

        if self.turn_bool and self.turn_count < 3:
            self.turn_count += 1
            if self.turn_direction == "right" and self.turn_count == 1:
                return self.turn_right()
            elif self.turn_direction == "right" and self.turn_count == 2:
                return self.go()
            elif self.turn_direction == "right" and self.turn_count == 3:
                self.turn_direction = "left"
                self.turn_occurances += 1
                return self.turn_right()
            if self.turn_direction == "left" and self.turn_count == 1:
                return self.turn_left()
            elif self.turn_direction == "left" and self.turn_count == 2:
                return self.go()
            elif self.turn_direction == "left" and self.turn_count == 3:
                self.turn_direction = "right"
                self.turn_occurances += 1
                return self.turn_left()
        elif self.turn_count >= 3:
            self.turn_count = 0
            self.turn_bool = False

        return self.go()