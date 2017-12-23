#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ErrorMessage(object):
    
    @staticmethod
    def message(reason, command):
        message = f'Mission aborted: {reason}\n'
        message += f'Attempted command: {command}'
        return message
