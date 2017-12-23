#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from grid import Grid
from grid import GridInitializationError


def test_set_grid_size():
    Grid('5', '5')

def test_set_grid_size_fail():
    with pytest.raises(GridInitializationError):
        Grid('-1', '0')

    with pytest.raises(GridInitializationError):
        Grid('1', '-1')

    with pytest.raises(GridInitializationError):
        Grid('a', '0')

    with pytest.raises(GridInitializationError):
        Grid('0', 'a')

def test_valid_position():
    grid = Grid('5', '5')

    assert grid.valid_position(0, 0)
    assert grid.valid_position(4, 4)
    assert grid.valid_position(5, 5)

    assert not grid.valid_position(-1, 5)
    assert not grid.valid_position(5, -1)

    assert not grid.valid_position(6, 1)
    assert not grid.valid_position(1, 6)
