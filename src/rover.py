#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RoverInitializationError(Exception):
    pass

class Rover(object):

    # Allowed orientation values in order to do the turns
    ORIENTATION_VALUES = 'NESW'

    # Advance 1 position front is different depending of the rover orientation
    # this variable has the front move implications per orientation
    MOVE_FRONT = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

    def __init__(self, name):
        self._name = name

    @property
    def x_position(self):
        return self._x_position

    @property
    def y_position(self):
        return self._y_position

    @property
    def orientation(self):
        return self._orientation

    @property
    def name(self):
        return self._name

    def set_state(self, x_position, y_position, orientation):
        try:
            if len(orientation) != 1:
                raise ValueError

            if orientation not in Rover.ORIENTATION_VALUES:
                raise ValueError

            self._x_position = int(x_position)
            self._y_position = int(y_position)
            self._orientation = orientation

        except ValueError:
            message = 'Mission aborted: Rover initialization error\n'
            raise RoverInitializationError(message)

    def turn_right(self):
        # Next element in the ORIENTATION_VALUES variable
        actual_index = Rover.ORIENTATION_VALUES.index(self._orientation)
        next_index = (actual_index + 1) % len(Rover.ORIENTATION_VALUES)
        self._orientation = Rover.ORIENTATION_VALUES[next_index]
        return self._orientation

    def turn_left(self):
        # Previous element in the ORIENTATION_VALUES variable
        actual_index = Rover.ORIENTATION_VALUES.index(self._orientation)
        next_index = (actual_index - 1) % len(Rover.ORIENTATION_VALUES)
        self._orientation = Rover.ORIENTATION_VALUES[next_index]
        return self._orientation

    def move_one_position_front(self):
        step = Rover.MOVE_FRONT[self._orientation]
        self._x_position += step[0]
        self._y_position += step[1]
        return (self._x_position, self._y_position)

    # Return a new rover instance with the same position and orientation than this one
    def get_rover_copy(self):
        rover_copy = Rover(f'{self.name} Copy')
        rover_copy.set_state(self._x_position, self._y_position, self._orientation)
        return rover_copy
