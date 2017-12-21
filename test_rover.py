#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from rover import Rover

def test_set_grid_size():
    communications = CommunicationCenter()
    communications.set_grid_size('5', '5')

def test_set_grid_size_exception():
    communications = CommunicationCenter()
    assert not communications.set_grid_size('-1', '0')
    assert not communications.set_grid_size('0', '-1')
    assert not communications.set_grid_size('a', '0')
    assert not communications.set_grid_size('0', 'a')

def test_initialize_rover():
    communications = CommunicationCenter()
    communications.initialize_rover('Rover 1', 0, 0, 'N')

    communications = CommunicationCenter(x_limit = 5, y_limit = 5)
    communications.initialize_rover('Rover 1', 5, 5, 'N')
    assert True
