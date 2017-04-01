# Copyright (c) 2010-2013, Regents of the University of California. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
log = logging.getLogger('ParserStatus')
log.setLevel(logging.ERROR)
log.addHandler(logging.NullHandler())

import collections
import struct

from ParserException import ParserException
import Parser
import openvisualizer.openvisualizer_utils as u
from openvisualizer.openType import  typeAddr,typeAsn
import psycopg2
from datetime import datetime

class FieldParsingKey(object):

    def __init__(self,index,val,name,structure,fields):
        self.index      = index
        self.val        = val
        self.name       = name
        self.structure  = structure
        self.fields     = fields

class ParserStatus(Parser.Parser):
    
    HEADER_LENGTH       = 4
    last_time = datetime.now()
    nodes = {}


    def __init__(self):
        self.last_time = datetime.now()
        
        # log
        log.info("create instance")
        
        # initialize parent class
        Parser.Parser.__init__(self,self.HEADER_LENGTH)
        
        # local variables
        self.fieldsParsingKeys    = []
        
        # register fields
        self._addFieldsParser   (
                                    3,
                                    0,
                                    'IsSync',
                                    '<B',
                                    [
                                        'isSync',                    # B
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    1,
                                    'IdManager',
                                    '<BBBBBBBBBBBBBBBBBBBBB',
                                    [
                                        'isDAGroot',                 # B
                                        'myPANID_0',                 # B
                                        'myPANID_1',                 # B
                                        'my16bID_0',                 # B
                                        'my16bID_1',                 # B
                                        'my64bID_0',                 # B
                                        'my64bID_1',                 # B
                                        'my64bID_2',                 # B
                                        'my64bID_3',                 # B
                                        'my64bID_4',                 # B
                                        'my64bID_5',                 # B
                                        'my64bID_6',                 # B
                                        'my64bID_7',                 # B
                                        'myPrefix_0',                # B
                                        'myPrefix_1',                # B
                                        'myPrefix_2',                # B
                                        'myPrefix_3',                # B
                                        'myPrefix_4',                # B
                                        'myPrefix_5',                # B
                                        'myPrefix_6',                # B
                                        'myPrefix_7',                # B
                                    ],
                                )
        self._addFieldsParser   (   
                                    3,
                                    2,
                                    'MyDagRank',
                                    '<H',
                                    [
                                        'myDAGrank',                 # H
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    3,
                                    'OutputBuffer',
                                    '<HH',
                                    [
                                        'index_write',               # H
                                        'index_read',                # H
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    4,
                                    'Asn',
                                    '<BHH',
                                    [
                                        'asn_4',                     # B
                                        'asn_2_3',                   # H
                                        'asn_0_1',                   # H
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    5,
                                    'MacStats',
                                    '<BBhhBII',
                                    [
                                        'numSyncPkt' ,               # B
                                        'numSyncAck',                # B
                                        'minCorrection',             # h
                                        'maxCorrection',             # h
                                        'numDeSync',                 # B
                                        'numTicsOn',                 # I
                                        'numTicsTotal',              # I
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    6,
                                    'ScheduleRow',
                                    '<BHBBBBQQBBBBHH',
                                    [
                                        'row',                       # B
                                        'slotOffset',                # H 
                                        'type',                      # B
                                        'shared',                    # B
                                        'channelOffset',             # B
                                        'neighbor_type',             # B
                                        'neighbor_bodyH',            # Q
                                        'neighbor_bodyL',            # Q
                                        'numRx',                     # B
                                        'numTx',                     # B
                                        'numTxACK',                  # B
                                        'lastUsedAsn_4',             # B
                                        'lastUsedAsn_2_3',           # H
                                        'lastUsedAsn_0_1',           # H
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    7,
                                    'Backoff',
                                    '<BB',
                                    [
                                        'backoffExponent',           # B
                                        'backoff',                   # B
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    8,
                                    'QueueRow',
                                    '<BBBBBBBBBBBBBBBBBBBB',
                                    [
                                        'creator_0',                 # B
                                        'owner_0',                   # B
                                        'creator_1',                 # B
                                        'owner_1',                   # B
                                        'creator_2',                 # B
                                        'owner_2',                   # B
                                        'creator_3',                 # B
                                        'owner_3',                   # B
                                        'creator_4',                 # B
                                        'owner_4',                   # B
                                        'creator_5',                 # B
                                        'owner_5',                   # B
                                        'creator_6',                 # B
                                        'owner_6',                   # B
                                        'creator_7',                 # B
                                        'owner_7',                   # B
                                        'creator_8',                 # B
                                        'owner_8',                   # B
                                        'creator_9',                 # B
                                        'owner_9',                   # B
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    9,
                                    'NeighborsRow',
                                    '<BBBBBBQQHbBBBBBHHBBB',
                                    [
                                        'row',                       # B
                                        'used',                      # B
                                        'parentPreference',          # B
                                        'stableNeighbor',            # B
                                        'switchStabilityCounter',    # B
                                        'addr_type',                 # B
                                        'addr_bodyH',                # Q
                                        'addr_bodyL',                # Q
                                        'DAGrank',                   # H
                                        'rssi',                      # b
                                        'numRx',                     # B
                                        'numTx',                     # B
                                        'numTxACK',                  # B
                                        'numWraps',                  # B
                                        'asn_4',                     # B
                                        'asn_2_3',                   # H
                                        'asn_0_1',                   # H
                                        'joinPrio',                  # B
                                        'f6PNORES',                   # B
                                        'totalEBReceived',
                                    ],
                                )
        self._addFieldsParser   (   
                                    3,
                                    10,
                                    'kaPeriod',
                                    '<H',
                                    [
                                        'kaPeriod',                  # H
                                    ],
                                )
        self._addFieldsParser   (
                                    3,
                                    12,
                                    'EB',
                                    '<BQQBHH48B',
                                    [
                                        'addr_type',                 # B
                                        'addr_bodyH',                # Q
                                        'addr_bodyL',                # Q
                                        'asn_4',                     # B
                                        'asn_2_3',                   # H
                                        'asn_0_1',                   # H
                                        'eb_channel_11',            # B
                                        'eb_channel_12',            # B
                                        'eb_channel_13',            # B
                                        'eb_channel_14',            # B
                                        'eb_channel_15',            # B
                                        'eb_channel_16',            # B
                                        'eb_channel_17',            # B
                                        'eb_channel_18',            # B
                                        'eb_channel_19',            # B
                                        'eb_channel_20',            # B
                                        'eb_channel_21',            # B
                                        'eb_channel_22',            # B
                                        'eb_channel_23',            # B
                                        'eb_channel_24',            # B
                                        'eb_channel_25',            # B
                                        'eb_channel_26',            # B
                                        'ack_channel_11',           # B
                                        'ack_channel_12',           # B
                                        'ack_channel_13',           # B
                                        'ack_channel_14',           # B
                                        'ack_channel_15',           # B
                                        'ack_channel_16',           # B
                                        'ack_channel_17',           # B
                                        'ack_channel_18',           # B
                                        'ack_channel_19',           # B
                                        'ack_channel_20',           # B
                                        'ack_channel_21',           # B
                                        'ack_channel_22',           # B
                                        'ack_channel_23',           # B
                                        'ack_channel_24',           # B
                                        'ack_channel_25',           # B
                                        'ack_channel_26',           # B
                                        'tx_channel_11',            # B
                                        'tx_channel_12',            # B
                                        'tx_channel_13',            # B
                                        'tx_channel_14',            # B
                                        'tx_channel_15',            # B
                                        'tx_channel_16',            # B
                                        'tx_channel_17',            # B
                                        'tx_channel_18',            # B
                                        'tx_channel_19',            # B
                                        'tx_channel_20',            # B
                                        'tx_channel_21',            # B
                                        'tx_channel_22',            # B
                                        'tx_channel_23',            # B
                                        'tx_channel_24',            # B
                                        'tx_channel_25',            # B
                                        'tx_channel_26',            # B 
                                    ],
                                )
       
    
    #======================== public ==========================================
    
    def parseInput(self,input):
        
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("received input={0}".format(input))
        
        # ensure input not short longer than header
        self._checkLength(input)
        headerBytes = input[:3]
        
        # extract moteId and statusElem
        try:
           (moteId,statusElem) = struct.unpack('<HB',''.join([chr(c) for c in headerBytes]))
        except struct.error:
            raise ParserException(ParserException.DESERIALIZE,"could not extract moteId and statusElem from {0}".format(headerBytes))
        
        # log
        if log.isEnabledFor(logging.DEBUG):
            log.debug("moteId={0} statusElem={1}".format(moteId,statusElem))
        
        # jump the header bytes
        input = input[3:]
        
        # call the next header parser
        for key in self.fieldsParsingKeys:
            if statusElem==key.val:
            
                # log
                if log.isEnabledFor(logging.DEBUG):
                    log.debug("parsing {0}, ({1} bytes) as {2}".format(input,len(input),key.name))
                
                # parse byte array
                try:
                    fields = struct.unpack(key.structure,''.join([chr(c) for c in input]))   
                               
                except struct.error as err:
                    raise ParserException(
                            ParserException.DESERIALIZE,
                            "could not extract tuple {0} by applying {1} to {2}; error: {3}".format(
                                key.name,
                                key.structure,
                                u.formatBuf(input),
                                str(err)
                            )
                        )
                
                # map to name tuple
                returnTuple = self.named_tuple[key.name](*fields)
                if statusElem == 12:                        
                        print returnTuple
                        node =  str(hex(moteId))[4:6] + str(hex(moteId))[2:4]
                        if node in ['9788']:
                            current_time = datetime.now()

                            if (((current_time - self.last_time).total_seconds()/60.0) > 2):
                                 self.asn = typeAsn.typeAsn()
                                 self.asn.update(returnTuple[5],returnTuple[4],returnTuple[3])

                            sender = typeAddr.typeAddr()
                            sender.update(2,returnTuple[1],returnTuple[2])
                          
                            
                            eb_11 = returnTuple[6]
                            eb_12 = returnTuple[7]
                            eb_13 = returnTuple[8]
                            eb_14 = returnTuple[9]
                            eb_15 = returnTuple[10]
                            eb_16 = returnTuple[11]
                            eb_17 = returnTuple[12]
                            eb_18 = returnTuple[13]
                            eb_19 = returnTuple[14]
                            eb_20 = returnTuple[15]
                            eb_21 = returnTuple[16]
                            eb_22 = returnTuple[17]
                            eb_23 = returnTuple[18]
                            eb_24 = returnTuple[19]
                            eb_25 = returnTuple[20]
                            eb_26 = returnTuple[21]
                            
                            ack_11 = returnTuple[22]
                            ack_12 = returnTuple[23]
                            ack_13 = returnTuple[24]
                            ack_14 = returnTuple[25]
                            ack_15 = returnTuple[26]
                            ack_16 = returnTuple[27]
                            ack_17 = returnTuple[28]
                            ack_18 = returnTuple[29]
                            ack_19 = returnTuple[30]
                            ack_20 = returnTuple[31]
                            ack_21 = returnTuple[32]
                            ack_22 = returnTuple[33]
                            ack_23 = returnTuple[34]
                            ack_24 = returnTuple[35]
                            ack_25 = returnTuple[36]
                            ack_26 = returnTuple[37]

                            tx_11 = returnTuple[38]
                            tx_12 = returnTuple[39]
                            tx_13 = returnTuple[40]
                            tx_14 = returnTuple[41]
                            tx_15 = returnTuple[42]
                            tx_16 = returnTuple[43]
                            tx_17 = returnTuple[44]
                            tx_18 = returnTuple[45]
                            tx_19 = returnTuple[46]
                            tx_20 = returnTuple[47]
                            tx_21 = returnTuple[48]
                            tx_22 = returnTuple[49]
                            tx_23 = returnTuple[50]
                            tx_24 = returnTuple[51]
                            tx_25 = returnTuple[52]
                            tx_26 = returnTuple[53]

                            #nodes[str(sender)] = [tx,ack,eb]
                            #expected_number_of_nodes = 9

                            #if (len(self.nodes) == expected_number_of_nodes):
                            try:
                                conn = psycopg2.connect(database='ExperimentMultiChannel', user='postgres', password='rodrigo', host='2001:660:4701:1001:fd37:8a69:16e6:7525', port='5432')   
                                cur = conn.cursor()
                				#cur.execute("SELECT max(experiment_id)  from experiments")
                				#experiment_id = cur.fetchone()[0]
                				#if (experiment_id == '' or experiment_id == None):
                				#    experiment_id = 1
                				#else:
                				#    experiment_id = experiment_id + 1
                                experiment_id = 1

                                #for key,value in self.nodes.iteritems():
                                sql = "insert into experiments (asn,node,sender,experiment_id,\
                                eb_11,eb_12,eb_13,eb_14,eb_15,eb_16,eb_17,eb_18,eb_19,eb_20,eb_21,eb_22,eb_23,eb_24,eb_25,eb_26,\
                                ack_11,ack_12,ack_13,ack_14,ack_15,ack_16,ack_17,ack_18,ack_19,ack_20,ack_21,ack_22,ack_23,ack_24,ack_25,ack_26,\
                                tx_11,tx_12,tx_13,tx_14,tx_15,tx_16,tx_17,tx_18,tx_19,tx_20,tx_21,tx_22,tx_23,tx_24,tx_25,tx_26)\
                                values({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},\
                                {},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format("'" + str(self.asn) + "'",
                                "'" + str(node) + "'" ,"'" + str(sender)+ "'",str(experiment_id),eb_11,eb_12,eb_13,eb_14,eb_15,eb_16,eb_17,eb_18,eb_19,
                                eb_20,eb_21,eb_22,eb_23,eb_24,eb_25,eb_26,ack_11,ack_12,ack_13,ack_14,ack_15,ack_16,ack_17,ack_18,ack_19,
                                ack_20,ack_21,ack_22,ack_23,ack_24,ack_25,ack_26,tx_11,tx_12,tx_13,tx_14,tx_15,tx_16,tx_17,tx_18,tx_19,
                                tx_20,tx_21,tx_22,tx_23,tx_24,tx_25,tx_26) 
                                cur.execute(sql)
                                conn.commit()
                                conn.close()
                            except Exception as err:
                                print str(err)
                                pass     
                        self.last_time = datetime.now()
                
                # log
                if log.isEnabledFor(logging.DEBUG):
                    log.debug("parsed into {0}".format(returnTuple))
                
                # map to name tuple
                return 'status', returnTuple
        
        # if you get here, no key was found
        raise ParserException(ParserException.NO_KEY, "type={0} (\"{1}\")".format(
            input[0],
            chr(input[0])))
    
    #======================== private =========================================
    
    def _addFieldsParser(self,index=None,val=None,name=None,structure=None,fields=None):
    
        # add to fields parsing keys
        self.fieldsParsingKeys.append(FieldParsingKey(index,val,name,structure,fields))
        
        # define named tuple
        self.named_tuple[name] = collections.namedtuple("Tuple_"+name, fields)
