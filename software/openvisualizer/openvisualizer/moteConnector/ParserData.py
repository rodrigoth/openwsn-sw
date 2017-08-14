# Copyright (c) 2010-2013, Regents of the University of California. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
log = logging.getLogger('ParserData')
log.setLevel(logging.ERROR)
log.addHandler(logging.NullHandler())

import struct

from pydispatch import dispatcher

from ParserException import ParserException
import Parser
from openvisualizer.openType import  typeAddr,typeAsn
import requests


class ParserData(Parser.Parser):
    
    HEADER_LENGTH  = 2
    MSPERSLOT      = 15 #ms per slot.
    
    IPHC_SAM       = 4
    IPHC_DAM       = 0
    
     
    def __init__(self):
        
        # log
        log.info("create instance")
        
        # initialize parent class
        Parser.Parser.__init__(self,self.HEADER_LENGTH)
        
        self._asn= ['asn_4',                     # B
          'asn_2_3',                   # H
          'asn_0_1',                   # H
         ]
    
    
    #======================== public ==========================================
    
    def parseInput(self,input):
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("received data {0}".format(input))
        
        
        # ensure input not short longer than header
        self._checkLength(input)
   
        headerBytes = input[:2]
        #asn comes in the next 5bytes.  
        
        asnbytes=input[2:7]
        (self._asn) = struct.unpack('<HHB',''.join([chr(c) for c in asnbytes]))
        asn = typeAsn.typeAsn()
        asn.update(self._asn[0],self._asn[1],self._asn[2]) 
        

        
        #source and destination of the message
        dest = input[7:15]
        dest_bytes = struct.unpack('<Q',''.join([chr(c) for c in dest]))
        dest_address = typeAddr.typeAddr()
        dest_address.update(2,dest_bytes[0],0)
        
        
        #source is elided!!! so it is not there.. check that.
        source = input[15:23]
        source_bytes = struct.unpack('<Q',''.join([chr(c) for c in source]))
        source_address = typeAddr.typeAddr()
        source_address.update(2,source_bytes[0],0)
        

        
        if log.isEnabledFor(logging.DEBUG):
            a="".join(hex(c) for c in dest)
            log.debug("destination address of the packet is {0} ".format(a))
        
        if log.isEnabledFor(logging.DEBUG):
            a="".join(hex(c) for c in source)
            log.debug("source address (just previous hop) of the packet is {0} ".format(a))

        
        # remove asn src and dest and mote id at the beginning.
        # this is a hack for latency measurements... TODO, move latency to an app listening on the corresponding port.
        # inject end_asn into the packet as well
        input = input[23:]
        #print input
        #print len(input)

        if len(input) == 36 or len(input) == 37 :
            if len(input) == 36:
              asn_in_bytes = input[26:31]
              asn_in_bytes = struct.unpack('<HHB',''.join([chr(c) for c in asn_in_bytes]))
              asn_in = typeAsn.typeAsn()
              asn_in.update(asn_in_bytes[0],asn_in_bytes[1],asn_in_bytes[2]) 
              track = input[31]
              seqnum_bytes = input[32:]
              seqnum  = struct.unpack('>I',''.join([chr(c) for c in seqnum_bytes]))

            if len(input) == 37:
              asn_in_bytes = input[27:32]
              asn_in_bytes = struct.unpack('<HHB',''.join([chr(c) for c in asn_in_bytes]))
              asn_in = typeAsn.typeAsn()
              asn_in.update(asn_in_bytes[0],asn_in_bytes[1],asn_in_bytes[2]) 
              track = input[32]
              seqnum_bytes = input[33:]
              seqnum  = struct.unpack('>I',''.join([chr(c) for c in seqnum_bytes]))
          
            
            json = {}
            json['dest_address'] = str(dest_address)
            json['source'] = str(source_address)
            json['asn'] = str(asn)
            json['asn_in'] = str(asn_in)
            json['track'] = str(track)
            json['seqnum'] = str(seqnum[0])
            experiment_id = 5
            #print json

            url = 'http://[2001:660:4701:f018:0:82ff:fe4f:3091]:5000/'
            url = url + 'received'
            requests.post(url,json=json)

        
        if log.isEnabledFor(logging.DEBUG):
            log.debug("packet without source,dest and asn {0}".format(input))

        #print "packet without source,dest and asn {0}".format(input)
        
        # when the packet goes to internet it comes with the asn at the beginning as timestamp.
         
        # cross layer trick here. capture UDP packet from udpLatency and get ASN to compute latency.
        # then notify a latency component that will plot that information.
        # port 61001==0xee,0x49
        if len(input) >37:
           if input[36]==238 and input[37]==73:
            # udp port 61001 for udplatency app.
               aux      = input[len(input)-5:]               # last 5 bytes of the packet are the ASN in the UDP latency packet
               diff     = self._asndiference(aux,asnbytes)   # calculate difference 
               timeinus = diff*self.MSPERSLOT                # compute time in ms
               SN       = input[len(input)-23:len(input)-21] # SN sent by mote
               parent   = input[len(input)-21:len(input)-13] # the parent node is the first element (used to know topology)
               node     = input[len(input)-13:len(input)-5]  # the node address
               print timeinus
               
               if timeinus<0xFFFF:
               # notify latency manager component. only if a valid value
                  dispatcher.send(
                     sender        = 'parserData',
                     signal        = 'latency',
                     data          = (node,timeinus,parent,SN),
                  )
               else:
                   # this usually happens when the serial port framing is not correct and more than one message is parsed at the same time. this will be solved with HDLC framing.
                   print "Wrong latency computation {0} = {1} mS".format(str(node),timeinus)
                   print ",".join(hex(c) for c in input)
                   log.warning("Wrong latency computation {0} = {1} mS".format(str(node),timeinus))
                   pass
               # in case we want to send the computed time to internet..
               # computed=struct.pack('<H', timeinus)#to be appended to the pkt
               # for x in computed:
                   #input.append(x)
           else:
               # no udplatency
               # print input
               pass     
        else:
           pass      
       
        eventType='data'
        # notify a tuple including source as one hop away nodes elide SRC address as can be inferred from MAC layer header
        return eventType, (source, input)

 #======================== private =========================================
 
    def _asndiference(self,init,end):
      
       asninit = struct.unpack('<HHB',''.join([chr(c) for c in init]))
       asnend  = struct.unpack('<HHB',''.join([chr(c) for c in end]))
       if asnend[2] != asninit[2]: #'byte4'
          return 0xFFFFFFFF
       else:
           pass
       
       diff = 0
       if asnend[1] == asninit[1]:#'bytes2and3'
          return asnend[0]-asninit[0]#'bytes0and1'
       else:
          if asnend[1]-asninit[1]==1:##'bytes2and3'              diff  = asnend[0]#'bytes0and1'
              diff += 0xffff-asninit[0]#'bytes0and1'
              diff += 1
          else:   
              diff = 0xFFFFFFFF
       
       return diff