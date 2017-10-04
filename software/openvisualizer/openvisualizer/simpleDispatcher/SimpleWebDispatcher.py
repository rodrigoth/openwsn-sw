import requests
from dispatcher import Dispatcher
from openvisualizer.openType import  typeAddr,typeAsn

class SimpleWebDispatcher(Dispatcher):

    def send(self,statusInput,moteId):
    	json = {}

    	node = str(hex(moteId))[4:6] + str(hex(moteId))[2:4]	
    	
    	asn = typeAsn.typeAsn()
        asn.update(statusInput[2],statusInput[1],statusInput[0]) 

        json['asn'] = str(asn)
        json['node'] = node
        requests.post('http://[2001:660:4701:f018:0:82ff:fe4f:3091]:5000/parent_switch',json=json)     	