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
import select
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
    #node = Node.Node(1, 'localhost', 5555)
    #print(node)
    #client_address, client_socket = LinkLayer.InitializeSocket(node)
    #print(client_socket)
    #client_socket.close()
    pass
  
  
  def test_FrameStuff (self):
    #some_frame = LinkLayer.Frame()
    #print(some_frame)
    pass
    
 
  def test_communications (self):
    #node = Node.Node(1, 'localhost', 5555)
    #node.SetMTU(1500)
    #node.AddLink((2, 'localhost', 1))
    #node.AddLink((3, 'localhost', 1))
    node = Node.ConfigInitialNetworkTopology('itc_test.txt', int(sys.argv[1]))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    datagram = NetworkLayer.Datagram()
    datagram.SetMTU(node.GetMTU())
    if int(sys.argv[1]) == 1:
      datagram.SetDestPort(5556)
    else:
      datagram.SetDestPort(5555)
    # YOU MUST PUT THE \r\n IN HERE OR IT WILL NOT WORK.
    #datagram.SetPayload('This is a payload.\r\n')
    print(datagram.GetDestPort())
    inputs = [client_socket, sys.stdin]
    #print(what_was_sent.PrintContents())
    while(1):
      inputready,outputready,exceptready = select.select(inputs,[],[])
      for s in inputready:
        if s == client_socket:
          length_of_buffer, received_frame, datagram_to_pass, external_address, received_segment = LinkLayer.l2_recvfrom(client_socket, node) # added node as a parameter 04-06-2010.
          print(datagram_to_pass.GetPayload())
        #  received_segment.PrintContents()
        elif s == sys.stdin:
          payload = list(sys.stdin.readline())
          payload.remove('\n')
          payload.append('\r')
          payload.append('\n')
          payload = ''.join(payload)
          datagram.SetPayload(payload)
          what_was_sent = LinkLayer.l2_sendto(client_socket, sys.argv[2], datagram, node)
      #print(length_of_buffer)
      #received_frame.PrintContents()
      #if received_frame.GetLength() > 0:
      #  pass # We need to deal with Layer 3 send here.
      #datagram_to_pass.PrintContents()
      #print(external_address)
    client_socket.close()
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
  
