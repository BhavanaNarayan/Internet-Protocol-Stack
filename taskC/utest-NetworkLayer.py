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
import sys        # Basic system functionality.
import unittest   # For testing, yay!'

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskD')

import Node
import LinkLayer
import RoutingProtocol
import NetworkLayer


class TestNodeFunctions (unittest.TestCase):
  def test_communications (self):
    node = Node.Node(1, 'localhost', 5555)
    routing_table = RoutingProtocol.DVRP(node)
    segment = 'This is a payload.'
    
    node.SetMTU(1500)
    node.AddLink((2, 'localhost', 1))
    node.AddLink((3, 'localhost', 1))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    what_was_sent = NetworkLayer.l3_sendto(client_socket, 1, 5555, routing_table, segment, node)
    # Receive it.
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
  