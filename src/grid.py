#!/usr/bin/env python
# -*- coding: utf-8 -*-
from error_message import ErrorMessage

class GridInitializationError(Exception):
    pass

class Grid(object):

    def __init__(self, x_limit = 0, y_limit = 0):
        try:
            # No negative size allowed
            if int(x_limit) < 0 or int(y_limit) < 0:
                raise ValueError

            self._x_grid_limit = int(x_limit)
            self._y_grid_limit = int(y_limit)

        except ValueError:
            message = 'Mission aborted: grid initialization error\n'
            message += 'Attempt to initializate with the following parameters\n'
            message += f'x limit = {x_limit}\n'
            message += f'y limit = {y_limit}\n'

            raise GridInitializationError(message)

    # Check if the position is inside the gird
    def valid_position(self, x_position, y_position):
        correct_position = True

        if x_position > self._x_grid_limit or x_position < 0:
            correct_position = False

        if y_position > self._y_grid_limit or y_position < 0:
            correct_position = False

        return correct_position
