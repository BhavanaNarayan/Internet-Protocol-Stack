#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Paul Brower
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


# @Paul: Don't forget to rename the following functions. These functions will be for 
# the reliability stuff. However, for this Phase 1, they will be blank for now.
def SlidingWindowAlgorithm ():
  pass

  
def MoreReliabilityStuff ():
  pass
  

class Segment (object):
  # From Jeff, @Paul: 
  #
  # Define your header stuff here. I am not sure what you want to include.
  # You may want to include things like source/dest NIDs and ports, sequence numbers, 
  # etc, etc.
  #
  # Do note that Source/dest NIDs and ports and sequence numbers are in the Datagram 
  # header already. Just see what makes sense.
  #
  # I included checksum and sliding_window so far. Keep it if it makes sense, remove it
  # if it doesn't.
  def __init__ (self, checksum=0, sliding_window=0):
    self._checksum = checksum
    self._sliding_window = sliding_window
    
  
  # @Paul: Make sure to define Getter methods.
  def GetChecksum (self):
    return self._checksum
    
    
  def GetSlidingWindow (self):
    return self._sliding_window
    
    
  # @Paul: Make sure to define Setter methods. Depending on what needs to be done, 
  # some Setter methods may not be as trivial as these 1-liner codes below.
  def SetChecksum (self, checksum):
    self._checksum = checksum
  
  
  def SetSlidingWindow (self, sliding_window):
    self._sliding_window = sliding_window
    
  
  # @Paul: And lastly, don't forget this debugging function. It will be helpful to know
  # what is printed. Update this when you add more header information (class member variables).
  def PrintContents (self):
    print(self._checksum)
    print(self._sliding_window)
    