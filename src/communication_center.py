# -*- coding: utf-8 -*-
from input_parser import InputParser
from input_parser import ParseCommandError
from grid import Grid
from grid import GridInitializationError
from rovers_controller import RoversController
from rovers_controller import RoverOutOfGridError
from rovers_controller import RoversCollisionError
from rovers_controller import RoversActionError
from rover import Rover
from rover import RoverInitializationError

class CommunicationCenterError(Exception):
    pass

class CommunicationCenter(object):
    def _initialize_rovers_from_list(self, rovers_init_list):
        try:
            rover_number = 0
            for rover_init in rovers_init_list:
                rover_name = RoversController._get_rover_name_by_number(rover_number)

                x_position = rover_init[0]
                y_position = rover_init[1]
                orientation = rover_init[2]

                print(f'Initializing {rover_name}:')
                print(f'  X position = {x_position}')
                print(f'  Y position = {y_position}')
                print(f'  Orientation = {orientation}')
                self.rovers_controller.initialize_rover(rover_name, x_position, y_position, orientation)

                rover_number += 1
        except RoverInitializationError as e:
            raise CommunicationCenterError(e)
        except RoverOutOfGridError as e:
            raise CommunicationCenterError(e)
        except RoversCollisionError as e:
            raise CommunicationCenterError(e)

    def _execute_actions_list(self, actions_list):
        try:
            rover_number = 0

            for each_actions in actions_list:
                rover_name = RoversController._get_rover_name_by_number(rover_number)

                print(f'Executing {rover_name} actions:')
                print(f'  Actions = {each_actions}')

                state = self.rovers_controller.execute_rover_actions(rover_name, each_actions)

                print(f'  Final state = {state}')

                rover_number += 1

        except RoversActionError as e:
            raise CommunicationCenterError(e)
        except RoverOutOfGridError as e:
            raise CommunicationCenterError(e)
        except RoversCollisionError as e:
            raise CommunicationCenterError(e)

    def execute_commands_list(self, commands_list):
        try:
            input_parser = InputParser(commands_list)
            grid = Grid(input_parser.grid_size[0],input_parser.grid_size[1])
            self.rovers_controller = RoversController(grid)
            self._initialize_rovers_from_list(input_parser.rovers_init)
            self._execute_actions_list(input_parser.rovers_actions)

        except GridInitializationError as e:
            raise CommunicationCenterError(e)
        except ParseCommandError as e:
            raise CommunicationCenterError(e)

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
        except CommunicationCenterError as e:
            print(e)
