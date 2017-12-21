#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from communication_center import *

def test_set_grid_limits():
    communications = CommunicationCenter()
    communications.set_grid_size(x_limit = 5, y_limit = 5)
    assert True

def test_initialize_rover():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover 1', 0, 0, 'N')
    assert True

    with pytest.raises(WrongRoverInitialization):
        communications.initialize_rover('Rover 1', 0, 0, 'N')

    with pytest.raises(WrongRoverInitialization):
        communications.initialize_rover('Rover 2', 1, 0, 'N')

def test_get_rover_state():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover 1', 0, 0, 'N')
    assert communications.get_rover_state('Rover 1') == (0, 0, 'N')

def test_execute_command_movement():
    communications = CommunicationCenter()
    communications.set_grid_size(x_limit = 2, y_limit = 2)

    communications.initialize_rover('Rover N', 1, 1, 'N')
    assert communications.execute_command('Rover N', 'M') == (1, 2, 'N')

    communications.initialize_rover('Rover E', 1, 1, 'E')
    assert communications.execute_command('Rover E', 'M') == (2, 1, 'N')

    communications.initialize_rover('Rover S', 1, 1, 'S')
    assert communications.execute_command('Rover S', 'M') == (1, 0, 'N')

    communications.initialize_rover('Rover W', 1, 1, 'W')
    assert communications.execute_command('Rover W', 'M') == (0, 1, 'N')

def test_execute_command_rotation():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover 1', 0, 0, 'N')

    assert communications.execute_command('Rover 1', 'L') == (0, 0, 'W')
    assert communications.execute_command('Rover 1', 'L') == (0, 0, 'S')
    assert communications.execute_command('Rover 1', 'L') == (0, 0, 'E')
    assert communications.execute_command('Rover 1', 'L') == (0, 0, 'N')

    assert communications.execute_command('Rover 1', 'R') == (0, 0, 'E')
    assert communications.execute_command('Rover 1', 'R') == (0, 0, 'S')
    assert communications.execute_command('Rover 1', 'R') == (0, 0, 'W')
    assert communications.execute_command('Rover 1', 'R') == (0, 0, 'N')

def test_rover_wrong_initialization():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover 1', 3, 3, 'N')
    with pytest.raises(InvalidMove):
        communications.execute_commands()

def test_rover_out_of_grid():
    communications = CommunicationCenter()

    communications.set_commands(['5 5', '5 0 N', 'M'])
    with pytest.raises(InvalidMove):
        communications.execute_commands()

    communications.set_commands(['2 2', '5 5 N', 'M'])
    with pytest.raises(InvalidMove):
        communications.execute_commands()

    communications.set_commands(['5 5', '5 0 N', 'M'])
    with pytest.raises(InvalidMove):
        communications.execute_commands()

def write_commands_file(tmpdir, commands_list):
    temporal_file = tmpdir.join('commands.txt')
    with open(temporal_file.strpath, 'w') as fp:
        for each_command in commands_list:
            fp.write(f'{each_command}\n')

    return temporal_file

def test_write_commands_file(tmpdir):
    pass

def test_integration(tmpdir):
    commands = ['5 5', '1 2 N', 'LMLMLMLMM', '3 3 E', 'MMRMMRMRRM']
    commands_file = write_commands_file(tmpdir, commands)

    communications = CommunicationCenter()
    communications.get_commands_from_file(commands_file_path = commands_file.strpath)
    communications.execute_commands()

    assert print(communications) == '1 3 N\n5 1 E'
