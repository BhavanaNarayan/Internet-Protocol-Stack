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


def l3_sendto (client_socket, destination_nid, destination_port, DVRP=None, segment=None, node=None):
  """
  This function will be used in Layer 4, the Transport layer. Nowhere in this Layer 3
  is this function used--rather, this layer purely uses l2_sendto from 
  the LinkLayer module.
  """
  next_hop = DVRP.GetRoutingTable()[destination_nid]
  mtu = node.GetMTU()
  sequence_number = 1
  total_sequence_numbers = 1
  dest_hostname = ResolveNID(destination_nid)
  dest_hostname = socket.gethostbyname(dest_hostname)
  
  while len(segment) > mtu:
    temp_segment = segment[:mtu-1]
    datagram = Datagram(sequence_number, total_sequence_numbers, mtu, 10, 
                        node.GetNID(), node.GetPort(), 
                        destination_nid, destination_port, temp_segment)
    to_wire = LinkLayer.l2_sendto(client_socket, dest_hostname, datagram, node)
    segment = segment[mtu:]
    sequence_number += 1
    total_sequence_numbers += 1
  
  if len(payload) > 0:
    datagram = Datagram(sequence_number, total_sequence_numbers, mtu, 10, 
                        node.GetNID(), node.GetPort(), 
                        destination_nid, destination_port, payload)
    to_wire = LinkLayer.l2_sendto(client_socket, dest_hostname, datagram, node)
  

def l3_recvfrom (client_socket, datagram, node=None):
  """
  This function will be used in Layer 4, the Transport layer. Nowhere in this Layer 3
  is this function used--rather, this layer purely uses l2_recvfrom from 
  the LinkLayer module.
  """
  # Split the headers.
  packet = datagram.split('@@')
  datagram_header = packet[0].split('@')
  segment_header = packet[1].split('@')
  
  # Now we should have something like [Datagram, Segment].
  # Step 1. Build a new Datagram.
  new_datagram = Datagram(datagram_header[0], datagram_header[1], datagram_header[2], 
                 datagram_header[3], datagram_header[4], datagram_header[5], 
                 datagram_header[6], datagram_header[7], datagram_header[8], 
                 packet[1])
  
  # If it's at the destination node...
  if int(datagram_header[6]) == node.GetNID():
    #segment = RTP.Segment(A BUNCH OF SEGMENT HEADERS)
    # Reassemble packets.
    
    # Call l4_sendto
    #RTP.l4_sendto(segment)
    return # len(packet), new_datagram, segment
  else:
    # Step 1. If TTL is 0, then drop, else, decrease
    if new_datagram.GetTTL() > 0:
      new_datagram.DecreaseTTL()
      # TODO: Consider reassembly issues with MTU. (possibly up there ---^ Line 93). 


# We are not using inheritance beacuse inheritance does not meet our goals.
# The idea is that, the payload of this class will be the Frame. The string that
# will be passed will be put in the Frame.
class Datagram (object):
  """
  Notes: We need to include the MTU (for fragmentation and reassembly), TTL,
    payload = Frame. The TTL will be decremented after each hop.
  """
  def __init__ (self, sequence_number=1, total_sequence_numbers=1, mtu=0, ttl=10, 
                source_nid='1', source_port=5555, 
                destination_nid='1', destination_port=5555, 
                length=0, payload=None):
    self._sequence_number = sequence_number
    self._total_sequence_numbers = total_sequence_numbers
    self._mtu = mtu
    self._ttl = ttl
    self._source_nid = source_nid
    self._source_port = source_port
    self._destination_nid = destination_nid
    self._destination_port = destination_port
    if payload is not None:
      self._length = len(payload)
    self._payload = payload
  
  
  def GetSequenceNumber (self):
    return self._sequence_number
  
  
  def GetTotalSequenceNumbers (self):
    return self._total_sequence_numbers
    
  
  def GetMTU (self):
    return self._mtu
    
    
  def GetTTL (self):
    return self._ttl
    
  
  def GetSourceNID (self):
    return self._source_nid
    
  
  def GetSourcePort (self):
    return self._source_port
  
  
  def GetDestNID (self):
    return self._destination_nid
    
  
  def GetDestPort (self):
    return self._destination_port
    
    
  # WE MIGHT NEED TO CHANGE THIS DRASTICALLY.
  # Idea: We get a string -> set headers for this layer -> build Frame. GO.
  def GetPayload (self):
    return self._payload
  
  
  def GetLength (self):
    return self._length
    
    
  def SetSequenceNumber (self, sequence_number):
    self._sequence_number = sequence_number
  
  
  def SetTotalSequenceNumbers (self, total_sequence_numbers):
    self._total_sequence_numbers = total_sequence_numbers
    
  
  def SetMTU (self, mtu):
    self._mtu = mtu
    
    
  def SetTTL (self, ttl):
    self._ttl = ttl

  def DecreaseTTL (self):
    self._ttl = self._ttl -1
    
  
  def SetSourceNID (self, source_nid):
    self._source_nid = source_nid
  
  
  def SetSourcePort (self, source_port):
    self._source_port = source_port
    
  
  def SetDestNID (self, destination_nid):
    self._destination_nid = destination_nid
    
    
  def SetDestPort (self, destination_port):
    self._destination_port = destination_port

    
  # WE MIGHT NEED TO CHANGE THIS DRASTICALLY.
  def SetPayload (self, payload):
    self._payload = payload
    self._length = len(payload)
    
    
  def PrintContents (self):
    print(self._sequence_number)
    print(self._total_sequence_numbers)
    print(self._mtu)
    print(self._ttl)
    print(self._source_nid)
    print(self._source_port)
    print(self._destination_nid)
    print(self._destination_port)
    print(self._length)
    print(self._payload)
