#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rover(object):

    ORIENTATION_VALUES = 'NESW'
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
            if int(x_position) < 0 or int(y_position) <0:
                raise ValueError

            if len(orientation) != 1:
                raise ValueError

            if orientation not in Rover.ORIENTATION_VALUES:
                raise ValueError

            self._x_position = int(x_position)
            self._y_position = int(y_position)
            self._orientation = orientation

        except ValueError:
            print('Mission aborted: Rover initialization error')
            print(f'Attempt to initializate with the following parameters')
            print(f'name = {self.name}')
            print(f'x_position = {x_position}')
            print(f'y_position = {y_position}')
            print(f'orientation = {orientation}')
            return False

        return True

    def turn_right(self):
        actual_index = Rover.ORIENTATION_VALUES.index(self._orientation)
        next_index = (actual_index + 1) % len(Rover.ORIENTATION_VALUES)
        self._orientation = Rover.ORIENTATION_VALUES[next_index]
        return self._orientation

    def turn_left(self):
        actual_index = Rover.ORIENTATION_VALUES.index(self._orientation)
        next_index = (actual_index - 1) % len(Rover.ORIENTATION_VALUES)
        self._orientation = Rover.ORIENTATION_VALUES[next_index]
        return self._orientation

    def move_front(self):
        step = Rover.MOVE_FRONT[self._orientation]
        self._x_position += step[0]
        self._y_position += step[1]
        return (self._x_position, self._y_position)

    def get_copy(self):
        rover_copy = Rover(f'{self.name} Copy')
        rover_copy.set_state(self._x_position, self._y_position, self._orientation)
        return rover_copy
