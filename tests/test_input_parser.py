#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import sys
sys.path.append('../src')
from input_parser import InputParser
from input_parser import ParseCommandError

def test_parse_grid_size():
    assert InputParser.parse_grid_size('1 2') == (1, 2)

    with pytest.raises(ParseCommandError):
        InputParser.parse_grid_size('a 5')

    with pytest.raises(ParseCommandError):
        InputParser.parse_grid_size('5 5a')

    with pytest.raises(ParseCommandError):
        InputParser.parse_grid_size('1')

def test_parse_rover_init():
    assert InputParser.parse_rover_init('1 1 N') == (1, 1, 'N')
    assert InputParser.parse_rover_init('-1 -1 S') == (-1, -1, 'S')

    with pytest.raises(ParseCommandError):
        InputParser.parse_rover_init('a 1 N')

    with pytest.raises(ParseCommandError):
        InputParser.parse_rover_init('1 a N')

    with pytest.raises(ParseCommandError):
        InputParser.parse_rover_init('1 1')

    with pytest.raises(ParseCommandError):
        InputParser.parse_rover_init('1')

def test_parse_rover_actions():
    assert InputParser.parse_rover_actions('MLRLRLRLRLR') == 'MLRLRLRLRLR'
    assert InputParser.parse_rover_actions('MLRLRLRLRLR\n') == 'MLRLRLRLRLR'
    assert InputParser.parse_rover_actions('MLRLRLRLRLR\n \t') == 'MLRLRLRLRLR'

def test_parse_list_commands():
    with pytest.raises(ParseCommandError):
        InputParser([])

    with pytest.raises(ParseCommandError):
        InputParser(1)

    commands_list = ['5 5', '1 2 N', 'LMLMLMLMM', '3 3 E', 'MMRMMRMRRM']

    input_parser = InputParser(commands_list)
    assert input_parser.grid_size == (5, 5)
    assert input_parser.rovers_init == [(1, 2, 'N'), (3, 3, 'E')]
    assert input_parser.rovers_actions == ['LMLMLMLMM', 'MMRMMRMRRM']

    commands_list = ['5 5', '1 2 N']

    input_parser = InputParser(commands_list)
    assert input_parser.rovers_init == [(1, 2, 'N')]
    assert input_parser.rovers_actions == ['']
