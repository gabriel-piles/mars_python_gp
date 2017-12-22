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
            print(f'x limit = {x_limit}')
            print(f'y limit = {y_limit}')
            return False

        return True

    def _available_position_rover(self, rover):
        correct_position = True

        if rover.x_position > self._x_limit or rover.x_position < 0\
        or rover.y_position > self._y_limit or rover.y_position < 0:
            correct_position = False
            print('Mission aborted: Rover out of grid error')
            print(f'Rover: {rover.name}')

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

    def _subtract_grid_size_from_command(self, grid_size_string):

        try:
            limits_list = grid_size_string.split()
            correct_size = self.set_grid_size(limits_list[0], limits_list[1])
        except IndexError:
            correct_size = self.set_grid_size(grid_size_string, '')

        return correct_size

    @staticmethod
    def _get_rover_name_by_index(index):
        return f'Rover {index}'

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
                    correct_init = False
                    break

        return correct_init

    def _execute_rovers_commands(self, rovers_commands_list):
        correct_execution = True
        rover_index = 1

        for each_rover_commands in rovers_commands_list:
            rover_name = self._get_rover_name_by_index(rover_index)
            print('Executing rover commands:')
            print(f'Rover: {rover_name}')

            clean_commands = each_rover_commands.strip()
            print(f'Commands: {clean_commands}')
            
            for each_command in clean_commands:
                if not self.execute_command(rover_name, each_command):
                    correct_execution = False
                    break

            if correct_execution:
                rover_index += 1
            else:
                break

        return correct_execution

    def execute_commands_list(self, commands_list):
        self._rovers_list = {}

        correct_execution = True

        if len(commands_list) == 0:
            print('No commands for execute')
            return False

        print('Configuring grid size..')

        if not self._subtract_grid_size_from_command(commands_list[0]):
            correct_execution = False
        else:
            del commands_list[0]
            if not self._initialize_rovers_by_commands(commands_list[::2]):
                correct_execution = False
            else:
                if not self._execute_rovers_commands(commands_list[1::2]):
                    correct_execution = False

        return correct_execution

    def execute_commands_from_file(self, file_path):
        commands_list = []
        with open(file_path) as commands_lines:
            for each_line in commands_lines:
                commands_list.append(each_line)

        self.execute_commands_list(commands_list)

    # def __repr__(self):
    #     for each_rover_index in range(len(self._rovers_list)):
    #         rover_name = self._get_rover_name_by_index(each_rover_index + 1)
    #         state = self.get_rover_state(rover_name)
    #         print(f'{state[0]} {state[1]} {state[2]}')

if __name__ == '__main__':
    communications = CommunicationCenter()
    communications.set_grid_size('-1', 'a')
