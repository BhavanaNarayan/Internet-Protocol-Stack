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
import Node
import LinkLayer


class TestNodeFunctions (unittest.TestCase):
  def test_InitializeSocket (self):
    node = Node.Node(1, 'localhost', 5555)
    #print(node)
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    #print(client_socket)
    client_socket.close()
  
  
  def test_FrameStuff (self):
    some_frame = LinkLayer.Frame()
    #print(some_frame)
    
 
  def test_l2_recvfrom (self):
    #addr = ''
    #frame_queue = Queue.Queue()
    #external_address_queue = Queue.Queue()
    
    # To use receive from, we go like this:
    # frame, external_address = LinkLayer.l2
    node = Node.Node(1, 'localhost', 5555)
    node.SetMTU(1500)
    node.AddLink((2, 'localhost', 1))
    node.AddLink((3, 'localhost', 1))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    #print(client_address, client_socket.getsockname())
    some_frame = LinkLayer.Frame()
    some_frame.SetPayload('This is a payload.')
    #node.PrintContents()
    #some_frame.PrintContents()
    LinkLayer.l2_sendto(client_socket, 'localhost', some_frame, node)
    
    #frame_queue.put(result)
    #external_address_queue.put(addr)
    #thread_id = thread.start_new_thread(LinkLayer.l2_recvfrom, (client_socket, node))
    #frame = frame_queue.get()
    #external_address = external_address_queue.get()
    frame, external_address = LinkLayer.l2_recvfrom(client_socket, node)
    frame.PrintContents()
    #LinkLayer.l2_sendto(client_socket, 'localhost', some_frame, node)
    client_socket.close()
    pass
  
  
  def test_l2_sendto (self):
    # To use l2_sendto, we go like this:
    # <will add this tomorrow, April 02, 2010>
    node = Node.Node(1, 'localhost', 5556)
    node.SetMTU(1500)
    node.AddLink((2, 'localhost', 1))
    node.AddLink((3, 'localhost', 1))
    client_address, client_socket = LinkLayer.InitializeSocket(node)
    some_frame = LinkLayer.Frame()
    some_frame.SetPayload('This is a payload.')
    LinkLayer.l2_sendto(client_socket, 'localhost', some_frame, node)
    client_socket.close()
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
  