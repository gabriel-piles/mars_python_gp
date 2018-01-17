# -*- coding: utf-8 -*-
from rover import Rover

class RoverOutOfGridError(Exception):
    pass

class RoversCollisionError(Exception):
    pass

class RoversActionError(Exception):
    pass

class RoversController(object):

    def __init__(self, grid):
        self._grid = grid
        self._rovers_list = {}

    @staticmethod
    def _get_rover_name_by_number(number):
        return f'Rover {number + 1}'

    def get_rover_state(self, rover_name):
        state = ()
        if rover_name in self._rovers_list:
            rover = self._rovers_list[rover_name]
            state = (rover.x_position, rover.y_position, rover.orientation)

        return state

    # Check if position out of grid or collision between rovers
    def _rover_position_allowed(self, rover):
        if not self._grid.valid_position(rover.x_position, rover.y_position):
            message = 'Mission aborted: Rover out of grid attempted\n'
            message += f'  Rover = {rover.name}\n'
            message += f'  Position = ({rover.x_position}, {rover.y_position})'
            raise RoverOutOfGridError(message)

        # Checking if the rover collide with other rover
        for each_rover_name, each_rover in self._rovers_list.items():
            if each_rover_name == rover.name:
                continue

            if each_rover.x_position == rover.x_position:
                if each_rover.y_position == rover.y_position:
                    message = 'Mission aborted: Two rovers almost collide\n'
                    message += f'  Rovers = {each_rover_name} and {rover.name}\n'
                    message += f'  Position = ({rover.x_position}, {rover.y_position})'
                    raise RoversCollisionError(message)

    def initialize_rover(self, rover_name, x_position, y_position, orientation):
        new_rover = Rover(rover_name)
        new_rover.set_state(x_position, y_position, orientation)
        self._rover_position_allowed(new_rover)
        self._rovers_list[rover_name] = new_rover

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
        else:
            message = 'Mission aborted: Rover action not allowed\n'
            message += f'  Rover = {rover_name}\n'
            message += f'  Action = {action}'
            raise RoversActionError(message)

    def execute_rover_actions(self, rover_name, actions):
        if rover_name in self._rovers_list:
            for each_action in actions:
                self.execute_simple_action(rover_name, each_action)

        return self.get_rover_state(rover_name)
