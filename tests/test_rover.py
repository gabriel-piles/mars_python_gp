# -*- coding: utf-8 -*-
import pytest
import sys
sys.path.append('../src')
from rover import Rover
from rover import RoverInitializationError

def test_set_state():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 0, y_position = 0, orientation = 'N')
    rover.set_state(x_position = 1, y_position = 1, orientation = 'E')
    rover.set_state(x_position = 2, y_position = 2, orientation = 'S')
    rover.set_state(x_position = 3, y_position = 3, orientation = 'W')

def test_set_state_fail():
    rover = Rover('Rover 1')
    with pytest.raises(RoverInitializationError):
        rover.set_state(x_position = 0, y_position = 0, orientation = 'NW')

    with pytest.raises(RoverInitializationError):
        rover.set_state(x_position = 0, y_position = 0, orientation = 'n')

def test_get_position():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 1, y_position = 1, orientation = 'N')
    assert rover.x_position == 1
    assert rover.y_position == 1

def test_turn_right():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 0, y_position = 0, orientation = 'N')

    assert rover.turn_right() == 'E'
    assert rover.turn_right() == 'S'
    assert rover.turn_right() == 'W'
    assert rover.turn_right() == 'N'

def test_turn_left():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 0, y_position = 0, orientation = 'N')

    assert rover.turn_left() == 'W'
    assert rover.turn_left() == 'S'
    assert rover.turn_left() == 'E'
    assert rover.turn_left() == 'N'

def test_move_one_position_front():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 1, y_position = 1, orientation = 'N')
    assert rover.move_one_position_front() == (1, 2)

    rover.set_state(x_position = 1, y_position = 1, orientation = 'E')
    assert rover.move_one_position_front() == (2, 1)

    rover.set_state(x_position = 1, y_position = 1, orientation = 'S')
    assert rover.move_one_position_front() == (1, 0)

    rover.set_state(x_position = 1, y_position = 1, orientation = 'W')
    assert rover.move_one_position_front() == (0, 1)

def test_get_rover_copy():
    rover = Rover('Rover 1')
    rover.set_state(x_position = 1, y_position = 1, orientation = 'N')

    rover_copy = rover.get_rover_copy()

    assert rover_copy.x_position == rover.x_position
    assert rover_copy.y_position == rover.y_position
    assert rover_copy.orientation == rover.orientation
