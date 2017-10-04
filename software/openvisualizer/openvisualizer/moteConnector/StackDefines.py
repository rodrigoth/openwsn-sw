# DO NOT EDIT DIRECTLY!
# This file was generated automatically by GenStackDefines.py
# on Thu, 07 Sep 2017 16:22:47
#

components = {
   0: "NULL",
   1: "OPENWSN",
   2: "IDMANAGER",
   3: "OPENQUEUE",
   4: "OPENSERIAL",
   5: "PACKETFUNCTIONS",
   6: "RANDOM",
   7: "RADIO",
   8: "IEEE802154",
   9: "IEEE802154E",
  10: "SIXTOP_TO_IEEE802154E",
  11: "IEEE802154E_TO_SIXTOP",
  12: "SIXTOP",
  13: "NEIGHBORS",
  14: "SCHEDULE",
  15: "SIXTOP_RES",
  16: "SF",
  17: "OPENBRIDGE",
  18: "IPHC",
  19: "FORWARDING",
  20: "ICMPv6",
  21: "ICMPv6ECHO",
  22: "ICMPv6ROUTER",
  23: "ICMPv6RPL",
  24: "OPENTCP",
  25: "OPENUDP",
  26: "OPENCOAP",
  27: "C6T",
  28: "CEXAMPLE",
  29: "CINFO",
  30: "CLEDS",
  31: "CSENSORS",
  32: "CSTORM",
  33: "CWELLKNOWN",
  34: "TECHO",
  35: "TOHLONE",
  36: "UECHO",
  37: "UINJECT",
  38: "RRT",
  39: "SECURITY",
  40: "USERIALBRIDGE",
  41: "UEXPIRATION",
  42: "UMONITOR",
  43: "CJOIN",
  44: "OPENOSCOAP",
  45: "RANKING",
}

errorDescriptions = {
   1: "received an echo request",
   2: "received an echo reply",
   3: "getData asks for too few bytes, maxNumBytes={0}, fill level={1}",
   4: "the input buffer has overflown",
   5: "the command is not allowed, command = {0}",
   6: "unknown transport protocol {0} (code location {1})",
   7: "wrong TCP state {0} (code location {1})",
   8: "TCP reset while in state {0} (code location {1})",
   9: "unsupported port number {0} (code location {1})",
  10: "unexpected DAO (code location {0}). A change maybe happened on dagroot node.",
  11: "unsupported ICMPv6 type {0} (code location {1})",
  12: "unsupported 6LoWPAN parameter {1} at location {0}",
  13: "no next hop",
  14: "invalid parameter",
  15: "invalid forward mode",
  16: "large DAGrank {0}, set to {1}",
  17: "packet discarded hop limit reached",
  18: "loop detected due to previous rank {0} lower than current node rank {1}",
  19: "upstream packet set to be downstream, possible loop.",
  20: "neighbors table is full (max number of neighbor is {0})",
  21: "there is no sent packet in queue",
  22: "there is no received packet in queue",
  23: "schedule overflown",
  24: "wrong celltype {0} at slotOffset {1}",
  25: "unsupported IEEE802.15.4 parameter {1} at location {0}",
  26: "got desynchronized at slotOffset {0}",
  27: "synchronized at slotOffset {0}",
  28: "large timeCorr.: {0} ticks (code loc. {1})",
  29: "wrong state {0} in end of frame+sync",
  30: "wrong state {0} in startSlot, at slotOffset {1}",
  31: "wrong state {0} in timer fires, at slotOffset {1}",
  32: "wrong state {0} in start of frame, at slotOffset {1}",
  33: "wrong state {0} in end of frame, at slotOffset {1}",
  34: "maxTxDataPrepare overflows while at state {0} in slotOffset {1}",
  35: "maxRxAckPrepapare overflows while at state {0} in slotOffset {1}",
  36: "maxRxDataPrepapre overflows while at state {0} in slotOffset {1}",
  37: "maxTxAckPrepapre overflows while at state {0} in slotOffset {1}",
  38: "wdDataDuration overflows while at state {0} in slotOffset {1}",
  39: "wdRadio overflows while at state {0} in slotOffset {1}",
  40: "wdRadioTx overflows while at state {0} in slotOffset {1}",
  41: "wdAckDuration overflows while at state {0} in slotOffset {1}",
  42: "busy sending",
  43: "sendDone for packet I didn't send",
  44: "no free packet buffer (code location {0})",
  45: "freeing unused memory",
  46: "freeing memory unsupported memory",
  47: "unsupported command {0}",
  48: "unknown message type {0}",
  49: "wrong address type {0} (code location {1})",
  50: "bridge mismatch (code location {0})",
  51: "header too long, length {1} (code location {0})",
  52: "input length problem, length={0}",
  53: "booted",
  54: "invalid serial frame",
  55: "invalid packet frome radio, length {1} (code location {0})",
  56: "busy receiving when stop of serial activity, buffer input length {1} (code location {0})",
  57: "wrong CRC in input Buffer (input length {0})",
  58: "synchronized when received a packet",
  59: "security error on frameType {0}, code location {1}",
  60: "sixtop return code {0} at sixtop state {1}",
  61: "there are {0} cells to request mote",
  62: "the cells reserved to request mote contains slot {0} and slot {1}",
  63: "the slot {0} to be added is already in schedule",
  64: "the received packet format is not supported {code location {0}}",
  65: "the metadata type is not suppored",
  66: "the received packet has expired",
  67: "packet expiry time reached, dropped",
  68: "node joined",
  69: "OSCOAP sequence number reached maximum value",
  70: "OSCOAP buffer overflow detected {code location {0}}",
  71: "OSCOAP replay protection failed",
  72: "OSCOAP decryption and tag verification failed",
  73: "Aborted join process {code location {0}}",
  80: "Ranking array is empty",
  81: "Parent not changed",
  82: "No parent found",
  83: "First parent index {0}",
  84: "First parent index {0} second parent {1}",
  85: "Array not empty",
  86: "Parent changed",
}

sixtop_returncode = {
   0: "RC_SUCCESS",
   1: "RC_ERROR",
   2: "RC_EOL",
   3: "RC_RESET",
   4: "RC_VER_ERR",
   5: "RC_SFID_ERR",
   6: "RC_GEN_ERR",
   7: "RC_BUSY",
   8: "RC_NORES",
   9: "RC_CELLLIST_ERR",
}

sixtop_statemachine = {
   0: "IDLE",
   1: "WAIT_ADDREQUEST_SENDDONE",
   2: "WAIT_DELETEREQUEST_SENDDONE",
   3: "WAIT_RELOCATEREQUEST_SENDDONE",
   4: "WAIT_COUNTREQUEST_SENDDONE",
   5: "WAIT_LISTREQUEST_SENDDONE",
   6: "WAIT_CLEARREQUEST_SENDDONE",
   7: "WAIT_ADDRESPONSE",
   8: "WAIT_DELETERESPONSE",
   9: "WAIT_RELOCATERESPONSE",
  10: "WAIT_COUNTRESPONSE",
  11: "WAIT_LISTRESPONSE",
  12: "WAIT_CLEARRESPONSE",
}
