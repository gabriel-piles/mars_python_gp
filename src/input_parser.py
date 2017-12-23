#!/usr/bin/env python
# -*- coding: utf-8 -*-
from error_message import ErrorMessage

class ParseCommandError(Exception):
    pass

class InputParser(object):

    def __init__(self, commands_list):
        self._grid_size = ()
        self._rovers_init = []
        self._rovers_actions = []

        self.parse_list_commands(commands_list)

    @property
    def grid_size(self):
        return self._grid_size[0], self._grid_size[1]

    @property
    def rovers_init(self):
        return self._rovers_init

    @property
    def rovers_actions(self):
        return self._rovers_actions

    # The grid is the rovers space and is squared
    # the grid size command is a string with the following format
    # 'x_grid_limit y_grid_limit'
    # examples: '1 1', '2 2', '5 100'
    # '1 2' -> grid with height 1 and width 2
    @staticmethod
    def parse_grid_size(grid_size_command):
        try:
            limits_list = grid_size_command.split()
            x_limit = int(limits_list[0])
            y_limit = int(limits_list[1])
        except IndexError:
            message = ErrorMessage.message('Wrong grid size command', grid_size_command)
            raise ParseCommandError(message)
        except ValueError:
            message = ErrorMessage.message('Wrong grid size command', grid_size_command)
            raise ParseCommandError(message)

        return (x_limit, y_limit)

    # The initialization command is a string with the following format
    # 'x_position y_position orientation'
    # examples: '1 1 N', '2 2 E', '5 100 W'
    # '1 2 N' -> Rover in the position (1, 2) facing North
    @staticmethod
    def parse_rover_init(rover_init_command):
        try:
            values = rover_init_command.split()
            x_position = int(values[0])
            y_position = int(values[1])
            orientation = values[2]
        except IndexError:
            message = ErrorMessage.message('Wrong rover initialization command', rover_init_command)
            raise ParseCommandError(message)
        except ValueError:
            message = ErrorMessage.message('Wrong rover initialization command', rover_init_command)
            raise ParseCommandError(message)

        return x_position, y_position, orientation

    @staticmethod
    def parse_rover_actions(rover_actions_command):
        try:
            rover_actions_safe = rover_actions_command.strip()
        except SyntaxError:
            message = ErrorMessage.message('Wrong actions command', rover_actions_command)
            raise ParseCommandError(message)

        return rover_actions_safe

    def _parse_rovers_init_list(self, rovers_init_list):
        for each_rover_init in rovers_init_list:
            rover_init = InputParser.parse_rover_init(each_rover_init)
            self._rovers_init.append(rover_init)

    def _parse_rovers_actions_list(self, rovers_actions_list):
        for each_rover_action in rovers_actions_list:
            rover_actions = InputParser.parse_rover_actions(each_rover_action)
            self._rovers_actions.append(rover_actions)

    # The list of commands has the following format:
    # First element: grid initialization string
    # Each rover has two elements in a row
    #   1 initialization command like '1 1 N'
    #   2 actions command like 'MLMMMLRLMMRL'
    def parse_list_commands(self, commands_list):
        try:
            if len(commands_list) != 0:
                self._grid_size = InputParser.parse_grid_size(commands_list[0])
                del commands_list[0]

            rovers_init_list = commands_list[::2]
            rovers_actions_list = commands_list[1::2]

            # For getting the same number of initializations and actions
            if len(rovers_actions_list) < len(rovers_init_list):
                rovers_actions_list.append('')

            self._parse_rovers_init_list(rovers_init_list)
            self._parse_rovers_actions_list(rovers_actions_list)
        except TypeError:
            raise ParseCommandError(f'Wrong input commands: {commands_list}')
