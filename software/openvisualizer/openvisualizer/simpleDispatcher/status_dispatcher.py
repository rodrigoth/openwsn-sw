import requests
from dispatcher import Dispatcher
from openvisualizer.openType import  typeAddr,typeAsn
from openvisualizer.moteConnector import  status_type

class StatusDispatcher(Dispatcher):

    
    def __init__(self,status_id,ini_property,url):
        super(StatusDispatcher,self).__init__(ini_property)
        self.server_url = self.settings["host"] + url
        self.status_id = status_id

    def send(self,statusInput,hostname,param):
    	json = {}
        asn = typeAsn.typeAsn()
        
        asn.update(statusInput[2],statusInput[1],statusInput[0]) 
        json['asn'] = str(asn)
        json['hostname'] = hostname

        if (self.status_id == status_type.StatusTypes.Request6p):
            json['iana_code'] = statusInput[3]  
        else:
            json['new_parent'] = str(param)

        
        requests.post(self.server_url,json=json)    



