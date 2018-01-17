# -*- coding: utf-8 -*-
import pytest
import sys
sys.path.append('../src')
from communication_center import CommunicationCenter

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
    communications.execute_commands_from_file('')
    communications.execute_commands_from_file(commands_file.strpath)
