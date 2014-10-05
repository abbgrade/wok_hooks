'''
Created on 21.06.2013

@author: steffen
'''

import logging as log
import json


class Configuration(dict):

    def __init__(self, path, **kwargs):
        dict.__init__(self)
        self.path = path
        self.update(kwargs)
        self.load()

    def load(self):
        try:
            with open(self.path, 'rb') as file_handler:
                self.update(json.loads(file_handler.read()))
                file_handler.close()
        except IOError:
            log.debug('No such configuration file: %s' % self.path)

    def save(self):
        with open(self.path, 'wb+') as file_handler:
            file_handler.write(json.dumps(self))
            file_handler.close()