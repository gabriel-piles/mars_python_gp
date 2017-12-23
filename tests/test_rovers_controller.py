#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import sys
sys.path.append('../src')
from rovers_controller import RoversController
from rovers_controller import RoversCollisionError
from rovers_controller import RoverOutOfGridError

from grid import Grid
from rover import Rover

def test_get_rover_state():
    grid = Grid(5, 5)
    rovers_controller = RoversController(grid)
    assert rovers_controller.get_rover_state('Rover 1') == ()

def test_initialize_rover():
    grid = Grid(5, 5)
    rovers_controller = RoversController(grid)
    rovers_controller.initialize_rover('Rover 1', 5, 5, 'N')
    assert rovers_controller.get_rover_state('Rover 1') == (5, 5, 'N')

def test_initialize_rovers_fail():
    grid = Grid(0, 0)
    rovers_controller = RoversController(grid)

    with pytest.raises(RoverOutOfGridError):
        rovers_controller.initialize_rover('Rover 1', 1, 0, 'N')

    with pytest.raises(RoverOutOfGridError):
        rovers_controller.initialize_rover('Rover 1', 0, 1, 'N')

    grid = Grid(5, 5)
    rovers_controller = RoversController(grid)
    with pytest.raises(RoverOutOfGridError):
        rovers_controller.initialize_rover('Rover 1', -1, 0, 'N')

    with pytest.raises(RoverOutOfGridError):
        rovers_controller.initialize_rover('Rover 1', 0, -1, 'N')

    rovers_controller.initialize_rover('Rover 1', 5, 5, 'N')
    with pytest.raises(RoversCollisionError):
        rovers_controller.initialize_rover('Rover 2', 5, 5, 'E')

def test_initialize_rovers_from_list():
    grid = Grid(5, 5)
    rovers_controller = RoversController(grid)

    rovers_controller.initialize_rovers_from_list([(5, 5, 'N'), (1, 2, 'E')])

    rover_name = RoversController._get_rover_name_by_number(1)
    assert rovers_controller.get_rover_state(rover_name) == (5, 5, 'N')

    rover_name = RoversController._get_rover_name_by_number(2)
    assert rovers_controller.get_rover_state(rover_name) == (1, 2, 'E')

def test_execute_simple_action():
    grid = Grid(0, 1)
    rovers_controller = RoversController(grid)
    rovers_controller.initialize_rover('Rover 1', 0, 0, 'N')

    rovers_controller.execute_simple_action('Rover 1', 'L')
    assert rovers_controller.get_rover_state('Rover 1') == (0, 0, 'W')

    rovers_controller.execute_simple_action('Rover 1', 'R')
    assert rovers_controller.get_rover_state('Rover 1') == (0, 0, 'N')

    rovers_controller.execute_simple_action('Rover 1', 'M')
    assert rovers_controller.get_rover_state('Rover 1') == (0, 1, 'N')

    grid = Grid(1, 1)
    rovers_controller = RoversController(grid)
    rovers_controller.initialize_rover('Rover N', 1, 1, 'N')
    with pytest.raises(RoverOutOfGridError):
        rovers_controller.execute_simple_action('Rover N', 'M')

    rovers_controller.initialize_rover('Rover E', 1, 0, 'E')
    with pytest.raises(RoverOutOfGridError):
        rovers_controller.execute_simple_action('Rover E', 'M')

    rovers_controller.initialize_rover('Rover S', 0, 0, 'S')
    with pytest.raises(RoverOutOfGridError):
        rovers_controller.execute_simple_action('Rover S', 'M')

    rovers_controller.initialize_rover('Rover W', 0, 1, 'W')
    with pytest.raises(RoverOutOfGridError):
        rovers_controller.execute_simple_action('Rover W', 'M')

def test_execute_actions_list():
    grid = Grid(2, 2)
    rovers_controller = RoversController(grid)
    rovers_controller.execute_actions_list([])

    rovers_controller.initialize_rover('Rover 1', 0, 0, 'N')
    rovers_controller.initialize_rover('Rover 2', 0, 2, 'E')

    rovers_controller.execute_actions_list(['M','R'])

    assert rovers_controller.get_rover_state('Rover 1') == (0, 1, 'N')
    assert rovers_controller.get_rover_state('Rover 2') == (0, 2, 'S')

    with pytest.raises(RoversCollisionError):
        rovers_controller.execute_actions_list(['RM','LMRM'])
