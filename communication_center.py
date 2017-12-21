#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rover import Rover

class CommunicationCenter(object):

    def __init__(self, x_limit = 0, y_limit = 0):
        self.set_grid_size(x_limit, y_limit)
        self._rovers_list = {}

    def set_grid_size(self, x_limit = 0, y_limit = 0):
        try:
            if int(x_limit) < 0 or int(y_limit) < 0:
                raise ValueError

            self._x_limit = int(x_limit)
            self._y_limit = int(y_limit)

        except ValueError:
            print('Mission aborted: grid initialization error')
            print(f'Attempt to initializate with the following parameters')
            print(f'x_limit = {x_limit}')
            print(f'y_limit = {y_limit}')
            return False

        return True

    def _available_position_rover(self, rover):
        correct_position = True

        if rover.x_position > self._x_limit or rover.x_position < 0:
            correct_position = False

        if rover.y_position > self._y_limit or rover.y_position < 0:
            correct_position = False

        for each_rover_name, each_rover in self._rovers_list.items():
            if each_rover_name == rover.name:
                continue

            if each_rover.x_position == rover.x_position:
                if each_rover.y_position == rover.y_position:
                    correct_position = False
                    break

        return correct_position

    def initialize_rover(self, name, x_position, y_position, orientation):
        new_rover = Rover(name)
        correct_init = new_rover.set_state(x_position, y_position, orientation)

        if name in self._rovers_list:
            correct_init = False

        if correct_init and not self._available_position_rover(new_rover):
            correct_init = False

        if correct_init:
            self._rovers_list[name] = new_rover

        return correct_init

    def get_rover_state(self, rover_name):
        state = ()

        if rover_name in self._rovers_list:
            x_position = self._rovers_list[rover_name].x_position
            y_position = self._rovers_list[rover_name].y_position
            orientation = self._rovers_list[rover_name].orientation
            state = (x_position, y_position, orientation)

        return state

    def execute_command(self, rover_name, command):
        command_executed = True

        if command == 'R':
            self._rovers_list[rover_name].turn_right()
        elif command == 'L':
            self._rovers_list[rover_name].turn_left()
        elif command == 'M':
            ghost_rover = self._rovers_list[rover_name].get_copy()
            ghost_rover.move_front()
            if self._available_position_rover(ghost_rover):
                self._rovers_list[rover_name].move_front()
            else:
                command_executed = False
        else:
            command_executed = False

        return command_executed

    def execute_commands_list(self, commands_list):
        commands_executed = True

        return commands_executed

    def get_commands_from_file(self, file_path):
        pass

if __name__ == '__main__':
    communications = CommunicationCenter()
    communications.set_grid_size('-1', 'a')
