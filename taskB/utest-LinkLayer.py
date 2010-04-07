#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: utest-LinkLayer.py (from Task B: Emulation of point-to-point links)


import errno      # For errors!
import sys        # Basic system functionality.
import unittest   # For testing, yay!'
import thread
import Queue

sys.path.append('../taskA')
sys.path.append('../taskC')

import Node
import LinkLayer
import NetworkLayer


class TestNodeFunctions (unittest.TestCase):
  def test_InitializeSocket (self):
    node = Node.Node(1, 'localhost', 5555)
    #print(node)
    #client_address, client_socket = LinkLayer.InitializeSocket(node)
    #print(client_socket)
    #client_socket.close()
  
  
  def test_FrameStuff (self):
    some_frame = LinkLayer.Frame()
    #print(some_frame)
    
 
  def test_communications (self):
    #node = Node.Node(1, 'localhost', 5555)
    #node.SetMTU(1500)
    #node.AddLink((2, 'localhost', 1))
    #node.AddLink((3, 'localhost', 1))
    node = Node.ConfigInitialNetworkTopology('itc_test.txt', int(sys.argv[1]))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    datagram = NetworkLayer.Datagram()
    datagram.SetMTU(node.GetMTU())
    # YOU MUST PUT THE \r\n IN HERE OR IT WILL NOT WORK.
    datagram.SetPayload('This is a payload.\r\n')
    what_was_sent = LinkLayer.l2_sendto(client_socket, 'localhost', datagram, node)
    print(what_was_sent.PrintContents())
    while(1):
      length_of_buffer, received_frame, datagram_to_pass, external_address, received_segment = LinkLayer.l2_recvfrom(client_socket, node) # added node as a parameter 04-06-2010.
      #print(length_of_buffer)
      #received_frame.PrintContents()
      #if received_frame.GetLength() > 0:
      #  pass # We need to deal with Layer 3 send here.
      #datagram_to_pass.PrintContents()
      #print(external_address)
      received_segment.PrintContents()
    client_socket.close()
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
  