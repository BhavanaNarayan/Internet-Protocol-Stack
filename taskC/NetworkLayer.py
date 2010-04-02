#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Qiping Yan
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: NetworkLayer.py (from Task C: The network layer)


import errno      # For errors!
import socket     # Low-level networking interface.
import sys        # Basic system functionality.
import threading  # Higher-level threading interface.

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskD')

import Node
import LinkLayer
import RoutingProtocol


def ResolveNID (nid=None, node=None):
  """
  This function takes in two parameters, a nid and Node respectively. From there, 
  it creates a temporary copy of all the links associated with this node (we are 
  on localhost). After that, we iterate through all the links where each element of 
  this 'links' variable is a tuple consisting of (nid, hostname, flag). The flag 
  determines if the link is up or down. If our nid matches an nid in the 'links' 
  list variable, then we return the host name. This is necessary for resolving the 
  host name so we can use an ip address to send Frames over the wire.
  """
  links = node.GetLinks()
  
  for entry in links:
    if nid == entry[0]:
      return entry[1]


def l3_sendto (source_nid, source_port, destination_nid, destination_port, node = None, DVRP=None, payload=None):
  """
  This function will be used in Layer 4, the Transport layer. Nowhere in this Layer 3
  is this function used--rather, this layer purely uses l2_sendto from 
  the LinkLayer module.
  """
  datagram = Datagram(source_nid, source_port, destination_nid, destination_port, payload)
  frame = Frame(node.GetNID(), node.GetPort(), destination_nid, destination_port, datagram)
  L2_sendto(DVRP.GetRoutingTable()[destination_nid], frame) 
  pass
  

def l3_recvfrom (datagram, node=None):
  """
  This function will be used in Layer 4, the Transport layer. Nowhere in this Layer 3
  is this function used--rather, this layer purely uses l2_recvfrom from 
  the LinkLayer module.
  """
  destination_nid = datagram.GetDestinationNID()
  destination_port = datagram.GetDestinationPort()
  if destination_nid == node.GetNID():
    if destination_port == node.GetPort():
      data = datagram.GetPayload()
      l4_recvfrom(data)
      # pass data to app to save
    else:
      print("Error: bad port number -- ", destination_port)
  else:
    if datagram.GetTTL() >= 1:
      datagram.DecreaseTTL()
      l2_sendto(node,destination_nid, destination_port, datagram.GetPayload())  


# We are not using inheritance beacuse inheritance does not meet our goals.
# The idea is that, the payload of this class will be the Frame. The string that
# will be passed will be put in the Frame.
class Datagram (object):
  """
  Notes: We need to include the MTU (for fragmentation and reassembly), TTL,
    payload = Frame. The TTL will be decremented after each hop.
  """
  def __init__ (self, source_nid, source_port, destination_nid, destination_port, payload=None):
    self._mtu = mtu
    self._ttl = 20
    self._payload = payload
    self._source_nid = source_nid
    self._source_port = source_port
    self._destination_nid = destination_nid
    self._destination_port = destination_port
    
    
  
  
  def GetMTU (self):
    return self._mtu
    
    
  def GetTTL (self):
    return self._ttl
    
    
  # WE MIGHT NEED TO CHANGE THIS DRASTICALLY.
  # Idea: We get a string -> set headers for this layer -> build Frame. GO.
  def GetPayload (self):
    return self._payload
    
    
  def SetMTU (self, mtu):
    self._mtu = mtu
    
    
  def SetTTL (self, ttl):
    self._ttl = ttl

  def DecreaseTTL (self, ttl):
    self._ttl = self._ttl -1

    
  # WE MIGHT NEED TO CHANGE THIS DRASTICALLY.
  def SetPayload (self, payload):
    self._payload = payload
