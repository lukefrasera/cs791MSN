#!/usr/bin/env python

from consensus_filter import *
import numpy as np
import pylab as pl
import sys

def main(argv):
  iterations = 1000
  n_nodes = 30
  # cell = [.5, .4, 50]
  nodes = generate_random_node_graph(n_nodes, 0, 8)
  # nodes = [cell_measurement(cell, node, q_bar_calc(nodes)) for node in nodes]

  # Calculate average
  average = sum([node[2] for node in nodes])/float(len(nodes))
  adjacencies = connect_nodes(nodes, 5)
  # result = consensus_filter(metropolis, nodes, adjacencies, cell, iterations)

  data_temp = [float(c) for c in open('field1.txt').read().split(',')]
  data = [[[] for c in xrange(25)] for i in xrange(25)]
  result = [[[] for c in xrange(25)] for i in xrange(25)]

  for i in xrange(25):
    for j in xrange(25):
      data[i][j] = [float(i)/25.0 * 12,float(j)/25.0* 12,data_temp[i*25 + j]]

  for i, row in enumerate(data):
    for j, cell in enumerate(row):
      nodes = [cell_measurement(cell, node, q_bar_calc(nodes)) for node in nodes]
      result[i][j] = consensus_filter(metropolis, nodes, adjacencies, cell, iterations)[iterations-1][0]

  squared_error = []
  for i, row in enumerate(data):
    for j, cell in enumerate(row):
      squared_error.append(pow(cell[2] - result[i][j],2))
  least_squared_error = sqrt(sum(squared_error) * 1.0/float(len(squared_error)))
  print least_squared_error
  # print average
  # print result[iterations-1][0]

  
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

  pl.plot(range(25*25), squared_error)
  pl.show()


  # x = range(iterations)
  # for i, node in enumerate(nodes):
  #   pl.plot(x, [result[j][i] - result[iterations-1][0] for j in xrange(iterations)], label=('node: ' + str(i)))
  # pl.legend(loc='upper right')
  # pl.show()

if __name__ == '__main__':
  main(sys.argv)