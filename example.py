#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./src/')
from communication_center import CommunicationCenter

if __name__ == '__main__':
    communications = CommunicationCenter()
    path = 'commands_example.txt'
    communications.execute_commands_from_file(path)
