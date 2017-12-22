#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from communication_center import CommunicationCenter

def test_set_grid_size():
    communications = CommunicationCenter()
    communications.set_grid_size('5', '5')

def test_set_grid_size_fail():
    communications = CommunicationCenter()
    assert not communications.set_grid_size('-1', '0')
    assert not communications.set_grid_size('0', '-1')
    assert not communications.set_grid_size('a', '0')
    assert not communications.set_grid_size('0', 'a')

def test_initialize_rover():
    communications = CommunicationCenter()
    assert communications.initialize_rover('Rover 1', 0, 0, 'N')

    communications = CommunicationCenter(x_limit = 5, y_limit = 5)
    assert communications.initialize_rover('Rover 1', 5, 5, 'N')

def test_initialize_rover_fail():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover', 0, 0, 'N')
    assert not communications.initialize_rover('Rover', 0, 0, 'N')
    assert not communications.initialize_rover('Rover 1', 1, 0, 'N')
    assert not communications.initialize_rover('Rover 2', 0, 1, 'N')
    assert not communications.initialize_rover('Rover 3', -1, 0, 'N')
    assert not communications.initialize_rover('Rover 4', 0, -1, 'N')
    assert not communications.initialize_rover('Rover 4', 'a', 0, 'N')
    assert not communications.initialize_rover('Rover 4', 0, 'a', 'N')

    communications = CommunicationCenter(x_limit = 5, y_limit = 5)
    assert not communications.initialize_rover('Rover 5', 6, 0, 'N')
    assert not communications.initialize_rover('Rover 6', 0, 6, 'N')

def test_get_rover_state():
    communications = CommunicationCenter(x_limit = 2, y_limit = 2)
    communications.initialize_rover('Rover 1', 1, 1, 'N')
    assert communications.get_rover_state('Rover 1') == (1, 1, 'N')

def test_execute_simple_command():
    communications = CommunicationCenter(x_limit = 2, y_limit = 2)
    communications.initialize_rover('Rover 1', 0, 0, 'N')
    assert communications.execute_simple_command('Rover 1', 'L')
    assert communications.execute_simple_command('Rover 1', 'R')
    assert communications.execute_simple_command('Rover 1', 'M')

    communications = CommunicationCenter(x_limit = 1, y_limit = 1)
    communications.initialize_rover('Rover N', 1, 1, 'N')
    assert not communications.execute_simple_command('Rover N', 'M')

    communications.initialize_rover('Rover E', 1, 0, 'E')
    assert not communications.execute_simple_command('Rover E', 'M')

    communications.initialize_rover('Rover S', 0, 0, 'S')
    assert not communications.execute_simple_command('Rover S', 'M')

    communications.initialize_rover('Rover W', 0, 1, 'W')
    assert not communications.execute_simple_command('Rover W', 'M')

def test_execute_commands_list():
    communications = CommunicationCenter(x_limit = 2, y_limit = 2)
    assert communications.execute_commands_list([])
    assert communications.execute_commands_list(['2 2', '0 0 N'])
    assert communications.get_rover_state('Rover 1') == (0, 0, 'N')

    assert communications.execute_commands_list(['2 2', '0 0 N', 'M', '0 2 E', 'R'])
    assert communications.get_rover_state('Rover 1') == (0, 1, 'N')
    assert communications.get_rover_state('Rover 2') == (0, 2, 'S')

def test_execute_commands_list_fail():
    communications = CommunicationCenter()

    assert not communications.execute_commands_list(['2 2', '0 0 N', 'M', '0 1 N'])
    assert not communications.execute_commands_list(['2 2', '0 0 N', '', '1 1 N', 'LMLM'])

def write_commands_file(tmpdir, commands_list):
    temporal_file = tmpdir.join('commands.txt')
    with open(temporal_file.strpath, 'w') as fp:
        for each_command in commands_list:
            fp.write(f'{each_command}\n')

    return temporal_file

def test_execute_commands_from_file(tmpdir):
    commands = ['5 5', '1 2 N', 'LMLMLMLMM', '3 3 E', 'MMRMMRMRRM']
    commands_file = write_commands_file(tmpdir, commands)

    communications = CommunicationCenter()
    assert not communications.execute_commands_from_file('')
    assert communications.execute_commands_from_file(commands_file.strpath)
    assert communications.get_rover_state('Rover 1') == (1, 3, 'N')
    assert communications.get_rover_state('Rover 2') == (5, 1, 'E')

def test_execute_commands_from_file_fail(tmpdir):
    commands = ['0']
    commands_file = write_commands_file(tmpdir, commands)
    communications = CommunicationCenter()
    assert not communications.execute_commands_from_file(commands_file.strpath)

    commands = ['5 5', 'a 1 N']
    commands_file = write_commands_file(tmpdir, commands)
    communications = CommunicationCenter()
    assert not communications.execute_commands_from_file(commands_file.strpath)

    commands = ['5 5', '1 1 N', 'P']
    commands_file = write_commands_file(tmpdir, commands)
    communications = CommunicationCenter()
    assert not communications.execute_commands_from_file(commands_file.strpath)
