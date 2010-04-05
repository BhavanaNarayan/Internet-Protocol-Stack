#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: TransportLayer.py (from Task E: The transport layer)


import errno      # For errors!
import socket     # Low-level networking interface.
import sys        # Basic system functionality.
import threading  # Higher-level threading interface.

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskC')
sys.path.append('../taskD')

import Node
import LinkLayer
import NetworkLayer
import RoutingProtocol


def SlidingWindowAlgorithm ():
  pass

  
def MoreReliabilityStuff ():
  pass
  

# I (Jeff) will write this by tonight.
def l4_sendto (client_socket, destination_nid, destination_port, DVRP=None, message=None, node=None):
  # We need DVRP because we are passing it to Layer 3. Currently, this Layer 4 doesn't do 
  # anything right now. It just simply calls Layer 3.
  
  #segment = Segment(node.GetNID(), node.GetPort(), destination_nid, destination_port, 0, 0)
  #segment.SetPayload(message)
  what_was_sent = NetworkLayer.l3_sendto(client_socket, 
                                         destination_nid, destination_port, 
                                         DVRP, message, node)
  return what_was_sent
  

# I (Jeff) will write this by tonight.
def l4_recvfrom(client_socket, segment, node=None):
# Simply return the message to the top layer of the application because this implies 
# all the checks went through and everything is ok. When we implement the reliability, we 
# will do checks. If the checks were not good, ask for a retransmission or something.
  return segment
  

class Segment (object):
  def __init__ (self, source_nid=1, source_port=5555, dest_nid=1, dest_port=5555, 
                checksum=0, sliding_window=0, length=0, payload=None):
    self._source_nid = source_nid
    self._source_port = source_port
    self._dest_nid = dest_nid
    self._dest_port = dest_port
    self._checksum = checksum
    self._sliding_window = sliding_window
    if payload is not None:
      self._length = len(payload)
    self._payload = payload
    
  
  def GetSourceNID (self):
    return self._source_nid
    
  
  def GetSourcePort (self):
    return self._source_port
  
  
  def GetDestNID (self):
    return self._dest_nid
    
  
  def GetDestPort (self):
    return self._dest_port
    
    
  def GetChecksum (self):
    return self._checksum
    
    
  def GetSlidingWindow (self):
    return self._sliding_window
    
  
  def GetLength (self):
    return self._length
    
    
  def GetPayload (self):
    return self._payload
    
    
  def SetSourceNID (self, source_nid):
    self._source_nid = source_nid
  
  
  def SetSourcePort (self, source_port):
    self._source_port = source_port
    
    
  def SetDestNID (self, dest_nid):
    self._dest_nid = dest_nid
    
  
  def SetDestPort (self, dest_port):
    self._dest_port = dest_port
    
  
  def SetChecksum (self, checksum):
    self._checksum = checksum
  
  
  def SetSlidingWindow (self, sliding_window):
    self._sliding_window = sliding_window
    
  
  def SetPayload (self, payload):
    self._payload = payload
    self._length = len(payload)
    
  
  def PrintContents (self):
    print(self._source_nid)
    print(self._source_port)
    print(self._dest_nid)
    print(self._dest_port)
    print(self._checksum)
    print(self._sliding_window)
    print(self._length)
    print(self._payload)
    