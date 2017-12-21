#!/usr/bin/env python
# -*- coding: utf-8 -*-
class CommunicationCenter(object):

    def __init__(self, x_limit = 0, y_limit = 0):
        self.set_grid_size(x_limit, y_limit)

    def set_grid_size(self, x_limit = 0, y_limit = 0):
        try:
            if int(x_limit) < 0 or int(y_limit) < 0:
                raise ValueError

            self.x_limit = int(x_limit)
            self.y_limit = int(y_limit)

        except ValueError:
            print('Mission aborted: grid initialization error')
            print(f'Tried to initializate with: {x_limit}, {y_limit}')
            return False

        return True

    def execute_command(self, rover_name, command):
        pass

    def execute_commands_list(self, commands_list):
        pass

    def get_commands_from_file(self, file_path):
        pass

if __name__ == '__main__':
    communications = CommunicationCenter()
    communications.set_grid_size('-1', 'a')
