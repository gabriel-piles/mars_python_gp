#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rover import Rover

class RoverOutOfGridError(Exception):
    pass

class RoversCollisionError(Exception):
    pass

class RoversController(object):

    def __init__(self, grid):
        self._grid = grid
        self._rovers_list = {}

    @staticmethod
    def _get_rover_name_by_number(number):
        return f'Rover {number}'

    def get_rover_state(self, rover_name):
        state = ()
        if rover_name in self._rovers_list:
            rover = self._rovers_list[rover_name]
            state = (rover.x_position, rover.y_position, rover.orientation)

        return state

    # Check if position out of grid or collision between rovers
    def _rover_position_allowed(self, rover):
        if not self._grid.valid_position(rover.x_position, rover.y_position):
            raise RoverOutOfGridError(f'{rover.name}, {rover.x_position}, {rover.y_position}')

        # Checking if the rover collide with other rover
        for each_rover_name, each_rover in self._rovers_list.items():
            if each_rover_name == rover.name:
                continue

            if each_rover.x_position == rover.x_position:
                if each_rover.y_position == rover.y_position:
                    raise RoversCollisionError()

    def initialize_rover(self, name, x_position, y_position, orientation):
        new_rover = Rover(name)
        new_rover.set_state(x_position, y_position, orientation)
        self._rover_position_allowed(new_rover)
        self._rovers_list[name] = new_rover

    def initialize_rovers_from_list(self, rovers_init_list):
        rover_number = 1

        for rover_init in rovers_init_list:
            x_position = rover_init[0]
            y_position = rover_init[1]
            orientation = rover_init[2]

            rover_name = RoversController._get_rover_name_by_number(rover_number)
            self.initialize_rover(rover_name, x_position, y_position, orientation)

            rover_number += 1

    # Three commands allowed
    # R - turn right
    # L - turn left
    # M - move one position front
    def execute_simple_action(self, rover_name, action):
        if rover_name not in self._rovers_list:
            return

        if action == 'R':
            self._rovers_list[rover_name].turn_right()
        elif action == 'L':
            self._rovers_list[rover_name].turn_left()
        elif action == 'M':
            # Checking if the rover collide with other if it is moved front
            ghost_rover = self._rovers_list[rover_name].get_rover_copy()
            ghost_rover.move_one_position_front()
            self._rover_position_allowed(ghost_rover)
            self._rovers_list[rover_name].move_one_position_front()

    def execute_actions_list(self, actions_list):
        rover_number = 1

        for each_actions_string in actions_list:
            rover_name = RoversController._get_rover_name_by_number(rover_number)
            for each_action in each_actions_string:
                self.execute_simple_action(rover_name, each_action)

            rover_number += 1

    def __repr__(self):
        rovers_states = ''
        for each_rover_index in range(len(self._rovers_list)):
            rover_name = self._get_rover_name_by_number(each_rover_index + 1)
            state = self.get_rover_state(rover_name)
            if rovers_states == '':
                rovers_states += (f'{rover_name}: {state[0]} {state[1]} {state[2]}')
            else:
                rovers_states += (f'\n{rover_name}: {state[0]} {state[1]} {state[2]}')

        return f'Rovers states\n{rovers_states}'
