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
import os
from pydispatch import dispatcher

from ParserException import ParserException
import Parser
from openvisualizer.simpleDispatcher import data_dispatcher
from openvisualizer.openType import  typeAddr,typeAsn


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
        
        
        
        #source is elided!!! so it is not there.. check that.
        source = input[15:23]
        

        
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

        if len(input) == 43:
            asn_in_bytes = input[34:39]
            asn_in_bytes = struct.unpack('<HHB',''.join([chr(c) for c in asn_in_bytes]))
            asn_in = typeAsn.typeAsn()
            asn_in.update(asn_in_bytes[0],asn_in_bytes[1],asn_in_bytes[2]) 

            seqnum_bytes = input[39:]
            seqnum  = struct.unpack('>I',''.join([chr(c) for c in seqnum_bytes]))

            sender = input[26:34]
            source_address  = []
            source_address += ['-'.join(["%.2x"%b for b in sender])]
            source_address += [' ({0})'.format('64b')]
            source_address = ''.join(source_address)

            dispatcher = data_dispatcher.DataDispatcher("remote_web_server","received")
            dispatcher.send(str(asn),str(asn_in),str(source_address),seqnum[0])

        if len(input) == 44:
            asn_in_bytes = input[35:40]
            asn_in_bytes = struct.unpack('<HHB',''.join([chr(c) for c in asn_in_bytes]))
            asn_in = typeAsn.typeAsn()
            asn_in.update(asn_in_bytes[0],asn_in_bytes[1],asn_in_bytes[2]) 

            seqnum_bytes = input[40:]
            seqnum  = struct.unpack('>I',''.join([chr(c) for c in seqnum_bytes]))

            sender = input[27:35]
            source_address  = []
            source_address += ['-'.join(["%.2x"%b for b in sender])]
            source_address += [' ({0})'.format('64b')]
            source_address = ''.join(source_address)            


            dispatcher = data_dispatcher.DataDispatcher("remote_web_server","received")
            dispatcher.send(str(asn),str(asn_in),str(source_address),seqnum[0])



        
        if log.isEnabledFor(logging.DEBUG):
            log.debug("packet without source,dest and asn {0}".format(input))

        #print "packet without source,dest and asn {0}".format(input)
        
        # when the packet goes to internet it comes with the asn at the beginning as timestamp.
         
        # cross layer trick here. capture UDP packet from udpLatency and get ASN to compute latency.
        # then notify a latency component that will plot that information.
        # port 61001==0xee,0x49
       
       
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