#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Paul Brower
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: App.py (from Task F: The application)

import errno                  # Used for error reporting.
import os                     # Used for OS-related functions.
import re                     # Used for regular expressions.
import socket                 # Low-level networking interface.
import string                 # Used for complaint string manipulation.
import sys                    # Basic system functionality.
import threading              # Low-level threading interface.

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


def PrintUsage ():
  print('\nUsage: python2.5 App.py <nid> <itc script>')
  print('\tex: python2.5 App.py 1 itc.txt')
  print('\n\tNOTE: This program may also be invoked by ./App.py')
  print('\t      assuming you have sufficient user permissions.\n')
  

def main (object):
  if len(sys.argv) != 3:
    PrintUsage()
  else:
    pass
  

if __name__ == '__main__':
  main(object)
