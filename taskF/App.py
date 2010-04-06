#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Paul Brower
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: App.py (from Task F: Application)

import sys

sys.path.append('../taskA')
sys.path.append('../taskB')
sys.path.append('../taskC')
sys.path.append('../taskD')
sys.path.append('../taskE')

import Node
import LinkLayer
import NetworkLayer
import RoutingProtocol
import TransportLayer


def PrintMenu():
  print "\n==============================================================="
  print "*  Command Menu                                               *"
  print "*                                                             *"
  print "*   1) start_service(P)                                       *"
  print "*   2) stop_service(S)                                        *"
  print "*   3) connect(Y, S, W)                                       *"
  print "*   4) close(C)                                               *"
  print "*   5) download(C, F)                                         *"
  print "*   6) set_garbler(L, C)                                      *"
  print "*   7) route_table                                            *"
  print "*   8) link_down(N)                                           *"
  print "*   9) link_up(N)                                             *"
  print "*  10) debug                                                  *"
  print "*  11) exit                                                   *"
  print "*                                                             *"
  print "==============================================================="

def Command_1():
  """
  This command should call RTP to start a service point (port)
  at the local node.  It should return a Service ID number (port)
  that will accept P connections. 
  This should probably spin off a thread to handle that.
  ???RTP._start_service(P)???
  """
  pass

def Command_2():
  """
  This command should stop the service started with 1
  This should probably talk to the thread started in 1
  ???RTP._stop_service(S)???
  """
  pass

def Command_3():
  """
  This should start a connection with a remote SID at a remote node
  to handle the file transfer.
  ???RTP._connect(Y, S, W)???
  """
  pass

def Command_4():
  """
  This should close the connected socket from 3
  """
  pass

def Command_5():
  """
  This should talk to the connected 'socket' created in 3
  This will eventually need to be a thread to facilitate returning
  the command prompt so another download can be started.
  ???Download(C, F)???
  """
  pass

# TODO: add functionality
def Command_6():
  print "*** set_garbler does nothing yet"

# TODO: add functionality
def Command_7():
  print "*** route_table does nothing yet"

#TODO: add functionality
def Command_8():
  print "*** link_down does nothing yet"

# TODO: add functionality
def Command_9():
  print "*** link_up does nothing yet"

# TODO: add functionality
def Command_10():
  print "*** debug: this code has no bugs!!"

# TODO: add cleaningup code
def Command_11():
  print " Program is exiting..."


def main():
  global node
  node = Node.ConfigInitialNetworkTopology(sys.argv[2], int(sys.argv[1]))
  node.UpdateLinkStatus((2, 'localhost', 1))
  node.PrintContents() # for testing


while_control = True

# main program loop
while while_control:
  PrintMenu()
  print "\n  Enter the command number you would like to run"
  command_num = int(raw_input(">>> "))

  if command_num == 1:
    Command_1()

  elif command_num == 2:
    Command_2()

  elif command_num == 3:
    Command_3()

  elif command_num == 4:
    Command_4()

  elif command_num == 5:
    Command_5()

  elif command_num == 6:
    Command_6()

  elif command_num == 7:
    Command_7()

  elif command_num == 8:
    Command_8()

  elif command_num == 9:
    Command_9()

  elif command_num == 10:
    Command_10()

  elif command_num == 11:
    Command_11()
    while_control = False

  else:
    print " Not a valid command!!"



print" ...exiting program...Bye!"
#end


if __name__ == '__main__':
  main()
