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
    node = Node.ConfigInitialNetworkTopology(sys.argv[3], int(sys.argv[1]))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    datagram = NetworkLayer.Datagram()
    datagram.SetMTU(node.GetMTU())

    itc_script = open('itc_test.txt')
    a_list = itc_script.readlines()
    itc_script.close()

    for entry in a_list:
      temp = entry.split(' ')
      if sys.argv[1] == temp[0]:
        datagram.SetSourcePort(int(temp[2]))
      if sys.argv[2] in temp[0]:
        datagram.SetDestPort(int(temp[2]))
    # YOU MUST PUT THE \r\n IN HERE OR IT WILL NOT WORK.
    #datagram.SetPayload('This is a payload.\r\n')
    inputs = [client_socket, sys.stdin]
    #print(what_was_sent.PrintContents())
    go=1
    while(go is 1):
      #sys.stdout.write(str(node.GetNID()) + '> ')
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

          if 'exit' in payload:
            print('exiting...')
            go=0

          datagram.SetPayload(payload)
          hn = NetworkLayer.ResolveNID(int(sys.argv[2]), node)
          what_was_sent = LinkLayer.l2_sendto(client_socket, hn, datagram, node)
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
  
