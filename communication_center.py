#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rover import Rover

class CommunicationCenter(object):

    def __init__(self, x_limit = 0, y_limit = 0):
        self.set_grid_size(x_limit, y_limit)
        self._rovers_list = {}

    def set_grid_size(self, x_limit = 0, y_limit = 0):
        try:
            # No negative size allowed
            if int(x_limit) < 0 or int(y_limit) < 0:
                raise ValueError

            self._x_grid_limit = int(x_limit)
            self._y_grid_limit = int(y_limit)

        except ValueError:
            print('Mission aborted: grid initialization error')
            print(f'Attempt to initializate with the following parameters')
            print(f'x limit = {x_limit}')
            print(f'y limit = {y_limit}')
            return False

        return True

    def _check_if_position_allowed(self, rover):
        correct_position = True

        # Checking if the rover is inside the gird
        if rover.x_position > self._x_grid_limit or rover.x_position < 0\
        or rover.y_position > self._y_grid_limit or rover.y_position < 0:
            correct_position = False
            print('Mission aborted: Rover out of grid error')
            print(f'Rover: {rover.name}')

        # Checking if the rover collide with other rover
        for each_rover_name, each_rover in self._rovers_list.items():
            if each_rover_name == rover.name:
                continue

            if each_rover.x_position == rover.x_position:
                if each_rover.y_position == rover.y_position:
                    correct_position = False
                    print('Mission aborted: Rover collision error')
                    print(f'Rovers: {rover.name} and {each_rover.name}')
                    break

        if not correct_position:
            print(f'Position attempted:')
            print(f'x position = {rover.x_position}')
            print(f'y position = {rover.y_position}')

        return correct_position

    def initialize_rover(self, name, x_position, y_position, orientation):
        print(f'Initializating rover:')
        print(f'{name}, {x_position}, {y_position}, {orientation}')

        new_rover = Rover(name)
        correct_init = new_rover.set_state(x_position, y_position, orientation)

        # Two rovers with the same name not allowed
        if name in self._rovers_list:
            correct_init = False

        # A rover can't be initializate in other rover place
        if correct_init and not self._check_if_position_allowed(new_rover):
            correct_init = False

        if correct_init:
            self._rovers_list[name] = new_rover

        return correct_init

    # Return the rover position and orientation
    # (x_position, y_position, orientation)
    def get_rover_state(self, rover_name):
        state = ()

        if rover_name in self._rovers_list:
            x_position = self._rovers_list[rover_name].x_position
            y_position = self._rovers_list[rover_name].y_position
            orientation = self._rovers_list[rover_name].orientation
            state = (x_position, y_position, orientation)

        return state

    # Three commands allowed
    # R - turn right
    # L - turn left
    # M - move one position front
    def execute_simple_command(self, rover_name, command):
        command_executed = True

        if command == 'R':
            self._rovers_list[rover_name].turn_right()
        elif command == 'L':
            self._rovers_list[rover_name].turn_left()
        elif command == 'M':
            # Checking if the rover collide with other if it is moved front
            ghost_rover = self._rovers_list[rover_name].get_rover_copy()
            ghost_rover.move_one_position_front()
            if self._check_if_position_allowed(ghost_rover):
                self._rovers_list[rover_name].move_one_position_front()
            else:
                command_executed = False
        else:
            print('Mission aborted: Wrong command error')
            print(f'Command: {command}')
            command_executed = False

        return command_executed

    # The grid is the rovers space and is squared
    # the grid size command is a string with the following format
    # 'x_grid_limit y_grid_limit'
    # examples: '1 1', '2 2', '5 100'
    # '1 2' -> grid with height 1 and width 2
    def _subtract_grid_size_from_command(self, grid_size_command):
        try:
            limits_list = grid_size_command.split()
            correct_size = self.set_grid_size(limits_list[0], limits_list[1])
        except IndexError:
            correct_size = self.set_grid_size(grid_size_command, '')

        return correct_size

    @staticmethod
    def _get_rover_name_by_index(index):
        return f'Rover {index}'

    # The initialization command is a string with the following format
    # 'x_position y_position orientation'
    # examples: '1 1 N', '2 2 E', '5 100 W'
    # '1 2 N' -> Rover in the position (1, 2) facing North
    def _initialize_rovers_by_commands(self, initialization_commands):
        correct_init = True
        rover_index = 1

        for each_command in initialization_commands:
            values = each_command.split()
            if len(values) < 3:
                print('Mission aborted: Rover initialization error')
                print(f'Attempt to initializate with the following command:')
                print(f'{each_command}')
                correct_init = False
                break
            else:
                name = self._get_rover_name_by_index(rover_index)
                if self.initialize_rover(name, values[0], values[1], values[2]):
                    rover_index += 1
                else:
                    # Something wrong happend
                    correct_init = False
                    break

        return correct_init

    # Each rover commands is a string with the commands allowed
    # example = 'MMLRRRLLRLRLM'
    # 'MMR' -> move front, move front, turn right
    def _execute_rovers_commands(self, all_rovers_commands_list):
        correct_execution = True
        rover_index = 1

        for each_rover_commands in all_rovers_commands_list:
            rover_name = self._get_rover_name_by_index(rover_index)
            print('Executing rover commands..')
            print(f'Rover: {rover_name}')

            # Removing spaces and '\n' from the rovers commands string
            # for a correct execution
            each_rover_commands_cleared = str(each_rover_commands.strip())
            print(f'Commands: {each_rover_commands_cleared}')

            for each_command in each_rover_commands_cleared:
                if not self.execute_simple_command(rover_name, each_command):
                    correct_execution = False
                    break

            rover_index += 1

            if not correct_execution:
                break

        return correct_execution

    # The list of commands has the following format:
    # First element: grid initialization string
    # Each rover has two elements in a row
    #   1 initialization command like '1 1 N'
    #   2 actions command like 'MLMMMLRLMMRL'
    def execute_commands_list(self, commands_list):
        self._rovers_list = {}

        correct_execution = True

        if len(commands_list) == 0:
            print('No commands for execute')
            return True

        print('Configuring grid size..')

        # The first command is for fixing the grid size
        if not self._subtract_grid_size_from_command(commands_list[0]):
            correct_execution = False
        else:
            del commands_list[0]
            # Each rover has two commands in a row in the commands_list
            # It is necessary to initialize all the rovers before executing the
            # actions avoiding this way for unwanted rovers collisions
            if not self._initialize_rovers_by_commands(commands_list[::2]):
                correct_execution = False
            else:
                if not self._execute_rovers_commands(commands_list[1::2]):
                    correct_execution = False

        return correct_execution

    # Convert the lines of the file in a list of commands for the
    # function execute_commands_list
    def execute_commands_from_file(self, file_path):
        file_executed = True
        commands_list = []
        try:
            with open(file_path) as commands_lines:
                for each_line in commands_lines:
                    commands_list.append(each_line)

            if not self.execute_commands_list(commands_list):
                file_executed = False

        except FileNotFoundError:
            file_executed = False
            print('No mission: File not found')

        return file_executed

    def __repr__(self):
        rovers_states = ''
        for each_rover_index in range(len(self._rovers_list)):
            rover_name = self._get_rover_name_by_index(each_rover_index + 1)
            state = self.get_rover_state(rover_name)
            if rovers_states == '':
                rovers_states += (f'{rover_name}: {state[0]} {state[1]} {state[2]}')
            else:
                rovers_states += (f'\n{rover_name}: {state[0]} {state[1]} {state[2]}')

        return f'Rovers states:\n{rovers_states}'

if __name__ == '__main__':
    communications = CommunicationCenter()
    path = input("Commands file path: ")
    if communications.execute_commands_from_file(path):
        print(communications)
