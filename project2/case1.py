#!/usr/bin/env python

from consensus_filter import *
import numpy as np
import pylab as pl
import sys

def main(argv):
  iterations = 100
  n_nodes = 10
  cell = [.5, .4, 50]
  nodes = generate_random_node_graph(n_nodes, 0, 1)
  nodes = [cell_measurement(cell, node, q_bar_calc(nodes)) for node in nodes]

  # Calculate average
  average = sum([node[2] for node in nodes])/float(len(nodes))
  adjacencies = connect_nodes(nodes, .5)
  result = consensus_filter(metropolis, nodes, adjacencies, cell, iterations)


  print average
  print result[iterations-1][0]

  
  # Plot Connected Graph
  for i, node in enumerate(nodes):
    # build connections for node 1
    for j in adjacencies[i]:
      dx = node[0] - nodes[j][0]
      dy = node[1] - nodes[j][1]
      m = dy/dx
      b = node[1] - m*node[0]
      x = np.linspace(node[0], nodes[j][0], 20)
      y = [m * i + b for i in x]
      pl.plot(x, y, 'r')
    pl.plot(node[0], node[1],'o', label=('node:' + str(i)))
  pl.show()


  x = range(iterations)
  for i, node in enumerate(nodes):
    pl.plot(x, [result[j][i] - result[iterations-1][0] for j in xrange(iterations)], label=('node: ' + str(i)))
  pl.legend(loc='upper right')
  pl.show()

if __name__ == '__main__':
  main(sys.argv)