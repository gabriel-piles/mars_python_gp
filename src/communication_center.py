#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rover import *
from input_parser import *
from grid import *
from rovers_controller import *

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

            print(rovers_controller)

        except GridInitializationError as e:
            print(e)

    # Convert the lines of the file in a list of commands for the
    # function execute_commands_list
    def execute_commands_from_file(self, file_path):
        commands_list = []
        try:
            with open(file_path) as commands_lines:
                for each_line in commands_lines:
                    commands_list.append(each_line)

            self.execute_commands_list(commands_list)

        except FileNotFoundError:
            print('No mission: File not found')
