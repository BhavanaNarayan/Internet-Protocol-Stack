#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Paul Brower
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: utest-TransportLayer.py (from Task E: The transport layer)


import errno      # For errors!
import sys        # Basic system functionality.
import unittest   # For testing, yay!'
import thread
import Queue

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskC')
sys.path.append('../taskD')

import Node
import LinkLayer
import NetworkLayer
import RoutingProtocol
import TransportLayer


class TestNodeFunctions (unittest.TestCase):
  def test_communications (self):
    node = Node.Node(1, 'localhost', 5555)
    routing_table = RoutingProtocol.DVRP(node)
    # YOU NEED THE \r\n IN HERE.
    segment = 'This is a payload.\r\n'
    
    node.SetMTU(1500)
    node.AddLink((1, 'localhost', 1))  # A link to itself...
    node.AddLink((2, 'localhost', 1))
    node.AddLink((3, 'localhost', 1))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    what_was_sent = TransportLayer.l4_sendto(client_socket, 1, 5555, routing_table, segment, node)
    print(what_was_sent)
    # Receive it.
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
  