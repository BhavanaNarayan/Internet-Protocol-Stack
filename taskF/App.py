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
  pass

def Command_2():
  pass

def Command_3():
  pass

def Command_4():
  pass

def Command_5():
  pass

def Command_6():
  pass

def Command_7():
  pass

def Command_8():
  pass

def Command_9():
  pass

def Command_10():
  pass

def Command_11():
  pass



while_control = True

# main program loop
while while_control:
  PrintMenu()
  print "\n  Enter the command number you would like to run"
  command_num = int(raw_input(">>> "))
  if command_num == 1:
    Command_1()
    print command_num

  elif command_num == 2:
    Command_2()
    print command_num

  elif command_num == 3:
    Command_3()
    print command_num

  elif command_num == 4:
    Command_4()
    print command_num

  elif command_num == 5:
    Command_5()
    print command_num

  elif command_num == 6:
    Command_6()
    print command_num

  elif command_num == 7:
    Command_7()
    print command_num

  elif command_num == 8:
    Command_8()
    print command_num

  elif command_num == 9:
    Command_9()
    print command_num

  elif command_num == 10:
    Command_10()
    print command_num

  elif command_num == 11:
    Command_11()
    print command_num
    while_control = False

  else:
    print " Not a valid command!!"



print" Exiting program..."
#end
