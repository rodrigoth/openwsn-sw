import ConfigParser
import logging
from abc import ABCMeta, abstractmethod
import os.path

class Dispatcher():
    __metaclass__ = ABCMeta
    settings_file = os.path.abspath(os.path.dirname(__file__))+"/settings.ini"

    def __init__(self,ini_property):
        self.config = ConfigParser.ConfigParser()
        self.settings = self.__read(ini_property)

    def __read(self,section):
        self.config.read(self.settings_file)
        dic = {}
        options = self.config.options(section)
        for option in options:
            try:
                dic[option] = self.config.get(section, option)
            except:
                logging.error("Property not found (%s)!" % option)
                dic[option] = None
        return dic

    @abstractmethod
    def send(self,input,node):
        pass