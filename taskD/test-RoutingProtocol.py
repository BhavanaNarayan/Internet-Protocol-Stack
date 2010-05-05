#!/usr/bin/python2.5

# CPE 701: Internet Protocol Design, Spring 2010
# Project - Emulation of a Reliable Transport Protocol
#
# Authors: Jeffrey Naruchitparames, Qiping Yan
# University of Nevada, Reno
# Department of Computer Science and Engineering
#
# File: RouteLayer.py (from Task D: The routing protocol)
# This is not really a layer of our protocol stack, but rather part of Layer 3, 
# which is the Network layer (task C).


import errno      # For errors!
import socket     # Low-level networking interface.
import sys        # Basic system functionality.
import threading  # Higher-level threading interface.

sys.path.append('../taskA')
sys.path.append('../taskB')

import Node
import LinkLayer


def Announce (link_from_node, link_to_node, link_change):
  """
  The node only need to tell its neighbors and only when this node's routing table
  changes.
  
  This function is supposed to send an update to all nodes using l2_send from the 
  LinkLayer module. The message it is sending is to notify all nodes that a link 
  has gone up or down. We need to know that so we can update our routing tables, 
  Node structures, and compute a new Shortest Path to converge our network.
  """
  for neighborNID in node.GetGlobalLinkTable()[node.GetNID()]:
    message = Datagram(1,1,999,10,node.GetNID(), node.GetPort(),neighborNID, 0, link_change, 1)
    l3_sendto(client_socket, neighborNID,0,DVRP, message,node)
  pass

  
  
# TODO(Qiping): Fix this.
def ComputeShortestPath (link_table, source_NID, destination_NID, via_NID=0):
  """
  Find the shortest path from source_NID to destination_NID based on link_table. 
  Returns a tuple of (via node, cost).
  """
#  link_table = node.GetGlobalLinkTable()
  routing_table_temp = {}
  for key in link_table.keys():
    if key == destination_NID:
        routing_table_temp[key] = (destination_NID, 0)
    elif key in link_table[destination_NID]:
        routing_table_temp[key] = (destination_NID, 1)
    else:
        routing_table_temp[key] = (0, -1)
  changed=1
  while changed:
    changed = 0
    for node in routing_table_temp.keys():
        if node != destination_NID:
            for neighbor_node in link_table[node]:
                if routing_table_temp[neighbor_node][1] != -1:
                    if routing_table_temp[node][1] == -1 or routing_table_temp[node][1] > routing_table_temp[neighbor_node][1] + 1:
                        routing_table_temp[node] = (neighbor_node, routing_table_temp[neighbor_node][1] + 1)
                        changed = 1
  return routing_table_temp[source_NID]
  
def Converge (node, link_from_node, link_to_node, link_change=0):
  """
  link_change = 0: the link from link_from_node to link_to_node went down
                1: the line is back up
  NOTE: Parameters are not yet defined.
  
  This function will be used in conjunction with the ComputerShortestPath() function.
  """
  if link_change == 0:
    if link_to_node not in node.GetGlobalLinkTable()[link_from_node]: # No change in the link table
      return
    else:
      if node.GetGlobalLinkTable()[link_from_node][0] == link_to_node:
        node.GetGlobalLinkTable()[link_from_node][0] = 0
      elif node.GetGlobalLinkTable()[link_from_node][1] == link_to_node:
        node.GetGlobalLinkTable()[link_from_node][1] = 0
      routing_table = BuildRoutingTable(link_table)
      Annouce(link_from_node, link_to_node, link_change)
  elif link_change == 1:
    if link_to_node in node.GetGlobalLinkTable()[link_from_node]: # No change in the link table
      return
    else:
      if node.GetGlobalLinkTable()[link_from_node][0] == 0:
        node.GetGlobalLinkTable()[link_from_node][0] = link_to_node
      elif node.GetGlobalLinkTable()[link_from_node][1] == 0:
        node.GetGlobalLinkTable()[link_from_node][1] = link_to_node
      routing_table = BuildRoutingTable(link_table)
      Annouce(link_from_node, link_to_node, link_change)

def printtable(table):
##  print table
  for key in table.keys():
    print key, ":", table[key]

def link_down(link_table, from_node, to_node):
  temp_link = link_table[from_node]
  new_link = []
  for i in temp_link:
    if i != to_node:
        new_link.append(i)
  link_table[from_node] = tuple(new_link)
  temp_link = link_table[to_node]
  new_link = []
  for i in temp_link:
    if i != from_node:
        new_link.append(i)
  link_table[to_node] = tuple(new_link)

def link_up(link_table, from_node, to_node):
  temp_link = link_table[from_node]
  new_link = [to_node]
  for i in temp_link:
    if i != to_node:
        new_link.append(i)
  link_table[from_node] = tuple(new_link)
  temp_link = link_table[to_node]
  new_link = [from_node]
  for i in temp_link:
    if i != from_node:
        new_link.append(i)
  link_table[to_node] = tuple(new_link)

def build_routing_table(link_table, fro):
  routing_table_temp = {}
  
  for key in link_table.keys():
    routing_table_temp[key] = ComputeShortestPath(link_table, fro, key)
  return routing_table_temp  



  
# Distance Vector Routing Protocol
class DVRP (object):
  """
  This class will maintain the a routing table for each node. That is, every instance 
  of our application will have ONE and only ONE routing table. The members are as follow:
  
    [0] _link_table = dictionary
      key: the node NID
      value: a tutple (of 2?) -- NID of the (2) neighbors. 
      It should be more effient to add _link_table to the Node class.
    [1] _routing_table = dictionary
      This is a dictionary where we have a {key:value} pair of {node:link cost}.
      We build our initial routing table by accessing the Node structure. In that 
      structure, we access Node._links because _links has all the physical links 
      associated with THIS node already. However, we have to DEFINE default 
      LINK COSTS by ourselves to associate with these physical links.
      
    [2] _shortest_path = <we have to define this data structure.
      Pretty much, this variable will have a listing of all the shortest paths from 
      THIS node (locally) to all other nodes. It will be another table maybe.
    
  This Task D is not really a layer in itself. It will be used in Task C (our Layer 3).
  """
  # Might need to add Node() class as a parameter here.
  def __init__ (self, node=None):
    # An example routing table would be: {1:10, 2:5, 3:8}. This means that 
    # THIS node is connected to nodes 1, 2, and 3 with link costs of 10, 5, and 8
    # respectively.
        
    self._routing_table = self.BuildRoutingTable(node)
    # self._shortest_path = shortest_path


  # Might need to add Node() class as a parameter here.
  def BuildRoutingTable(self, node):
    routing_table = {}
    for key in node.GetGlobalLinkTable().keys():
      # TODO(Qiping): Fix this.
      routing_table[key] = ComputeShortestPath(node, node.GetNID(), key, 0)

    return routing_table
  

  def GetRoutingTable (self):
    return self._routing_table
  
  
  def GetLinkTable (self):
    return self._link_table

  
  def GetShortestPath (self):
    return self._shortest_path


if __name__ == '__main__':
  print "Routing Protocol [test mode]"
  routing_table = {}
  link_table = {1:(2, 4), 2:(1, 3), 3:(2, 4, 5, 6), 4:(1, 3, 5, 8, 9), 5:(3, 4, 7), 6:(3, 7, 10, 11), 7:(5, 6, 12, 13), 8:(4, 9), 9:(4, 8), 10:(6, 11), 11:(6, 10), 12:(7, 13), 13:(7, 12)}
  home_NID = 3
  print "Initial Link Table"
  printtable(link_table)
  print
  print "Building initial Routing Table ... (done)"
  print
  routing_table = build_routing_table(link_table, home_NID)
  print "Routing Table (for node %d):" % home_NID
  printtable(routing_table)
  quiting = 0
  while not quiting:
    print
    print "Enter command: q -- quit, d -- link down, u -- link up"
    c = raw_input(">>")
    if c == "q":
      quiting = 1
    elif c == "d":
      link_from = int(raw_input("link down from node:"))
      link_to = int(raw_input("link down to node:"))
      print "Link from node %d to node " % link_from, "%d is going down ..." % link_to
      link_down(link_table, link_from, link_to)
      print "Updating Link Table ... (done)"
      print "New Link Table:"
      printtable(link_table)
      print "Converging Routing Table ... (done)"
      routing_table = build_routing_table(link_table, home_NID)
      print "New Routing Table:"
      printtable(routing_table)
    elif c == "u":
      link_from = int(raw_input("link up from node:"))
      link_to = int(raw_input("link up to node:"))
      print "Link from node %d to node " % link_from, "%d is going up ..." % link_to
      link_up(link_table, link_from, link_to)
      print "Updating Link Table ... (done)"
      print "New Link Table:"
      printtable(link_table)
      print "Converging Routing Table ... (done)"
      routing_table = build_routing_table(link_table, home_NID)
      print "New Routing Table:"
      printtable(routing_table)
  link_up(link_table, 4, 3)
  print
  printtable(link_table)
  
