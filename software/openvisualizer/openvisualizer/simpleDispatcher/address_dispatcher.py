import requests
from dispatcher import Dispatcher

class AddressDispatcher(Dispatcher):
    
    def __init__(self,ini_property,url):
        super(AddressDispatcher,self).__init__(ini_property)
        self.server_url = self.settings["host"] + url


    def send(self,hostname,mac):
    	json = {}
        json['hostname'] = hostname
        json['mac'] = mac
        requests.post(self.server_url,json=json)    