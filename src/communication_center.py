#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rover import Rover
from input_parser import InputParser
from grid import Grid
from grid import GridInitializationError

from rovers_controller import RoversController

class CustomError(Exception):
    pass

class CommunicationCenter(object):

    def __init__(self, x_limit = 0, y_limit = 0):
        pass

    def execute_commands_list(self, commands_list):
        try:
            input_parser = InputParser(commands_list)

            grid = Grid(input_parser.grid_size[0],input_parser.grid_size[1])

            rovers_controller = RoversController(grid)

            rovers_controller.initialize_rovers_from_list(input_parser.rovers_init)
            rovers_controller.execute_actions_list(input_parser.rovers_actions)

        except GridInitializationError:
            pass

    # Convert the lines of the file in a list of commands for the
    # function execute_commands_list
    def execute_commands_from_file(self, file_path):
        file_executed = True
        commands_list = []
        try:
            with open(file_path) as commands_lines:
                for each_line in commands_lines:
                    commands_list.append(each_line)

            self.execute_commands_list(commands_list)

        except FileNotFoundError:
            file_executed = False
            print('No mission: File not found')

        return file_executed
