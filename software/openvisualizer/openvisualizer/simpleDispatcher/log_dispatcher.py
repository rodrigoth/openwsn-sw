import requests
from dispatcher import Dispatcher
from openvisualizer.openType import  typeAddr,typeAsn

class LogDispatcher(Dispatcher):
    
    def __init__(self,ini_property,url):
        super(LogDispatcher,self).__init__(ini_property)
        self.server_url = self.settings["host"] + url


    def send(self,hostname):
    	json = {}
        json['hostname'] = hostname
        requests.post(self.server_url,json=json)    