#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rover import Rover

def test_rover():
    rover_1 = Rover('0 0 N')
    assert rover_1.get_position() == '0 0 N'
