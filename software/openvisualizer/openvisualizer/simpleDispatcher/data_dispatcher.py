import requests
from dispatcher import Dispatcher

class DataDispatcher(Dispatcher):
    
    def __init__(self,ini_property,url):
        super(DataDispatcher,self).__init__(ini_property)
        self.server_url = self.settings["host"] + url


    def send(self,asn,asn_in,sender,seq):
    	json = {}
        json['sender'] = sender
        json['asn'] = asn
        json['asn_in'] = asn_in
        json['seqnum'] = seq
        requests.post(self.server_url,json=json)    