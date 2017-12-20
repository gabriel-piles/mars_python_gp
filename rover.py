#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rover(object):

    def __init__(self, initialitation_string):
        self.position_x = initialitation_string[0]
        self.position_y = initialitation_string[2]
        self.orientation = initialitation_string[4]

    def get_position(self):
        return f'{self.position_x} {self.position_y} {self.orientation}'
