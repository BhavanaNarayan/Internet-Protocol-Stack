#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Paul Brower
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: test.py (from Task E: The transport layer)


import errno      # For errors!
import sys        # Basic system functionality.
import unittest   # For testing, yay!'
import thread
import Queue
import os         # for OS specific stuff
import socket     # for doing socket stuff
import time
import select

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskC')
sys.path.append('../taskD')

import Node
import LinkLayer
import NetworkLayer
import RoutingProtocol
import TransportLayer


my_port = sys.argv[1]
dest_IP = sys.argv[2]
dest_port = sys.argv[3]
TX_RX = sys.argv[4]

RDP = '1'
size = 500

# This is a trick to get python to get the real IP
# and not the localhost IP
test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
test_socket.connect(('google.com', 0))
# get our real IP and not the localhost IP
my_IP = test_socket.getsockname()[0]


#my_socket = TransportLayer.l4_socket(my_IP, my_port, dest_IP, dest_port)
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((my_IP, int(my_port)))
print "should have socket now"
input = [my_socket]
output = []
my_info = ["Blah", RDP, ""]
client_data = []
while_control = 1

#def decide(my_socket, input):
while while_control:
  RDP = '1'
  if TX_RX == 'TX':
    print "TX mode: You are going to transfer a file!"
    print "\n--- File transfer..."
    print "-   The files in the current directory that you can transfer:"
    file_names = os.listdir(".")
    for i in file_names:
        print "     -", i
    print"-   Enter the name of the file you would like"
    file_name = raw_input("-   to transfer, including extension: ")
    print file_name
    file = open(file_name, "rb")
    my_info[0] = "FileTX"
    my_info[2] = file_name
    x = 1
    while x:
      data_2_write = file.read(400)
      if data_2_write == "":
        x = 0 # EOF, exit while
        my_info[0] = "FileTXDone"
        client_msg, RDP = TransportLayer.client_pack(my_info, data_2_write, RDP)
        my_socket.sendto(client_msg, (dest_IP, int(dest_port)))
        #send that we are done.
      else:
        client_msg = " ".join(my_info)
        client_msg = client_msg + " " + data_2_write
        #client_msg, RDP = TransportLayer.client_pack(my_info, data_2_write, RDP)
        my_socket.sendto(client_msg, (dest_IP, int(dest_port)))
    
    file.close()
    print "File TX done!"
    while_control = 0
    
  elif TX_RX == 'RX':
    print "RX mode: You are going to receive a file..."
    x = 1
    while x:
      time.sleep(0.01) # sleep so we don't burn CPU cycles
      inputready, outputready, exceptready = select.select(input, output, [], 0)
      for s in inputready:
        if s == my_socket:
          client_msg, (client_IP, client_port) = my_socket.recvfrom(size)
          client_info, client_data, RDP = TransportLayer.client_unpack(client_msg, RDP)
          if client_info[0] == "FileTX":
            file_copy = "TransferedFile_"
            temp_list = []
            file_name = client_info[2]
            file_copy = file_copy + file_name
            file2 = open(file_copy, "ab")
            #print "This is raw:", client_msg.split(" ", 7)
            temp_list = client_msg.split(" ", 3)[3:]
            file2.write("".join(temp_list[0]))
            file2.close()

          elif client_info[0] == "FileTXDone":
            print "---  You just recieved a file!!!\n"
            x = 0
            while_control = 0
  else:
    print "Not a valid mode!"

#decide(my_socket, input)
print "Done...bye"
