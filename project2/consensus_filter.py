import random
from math import sqrt
from math import pow
def generate_random_node_graph(n, a, b):
  random.seed()
  nodes = []
  for i in xrange(n):
    # Generate Random node within range
    x = random.uniform(a, b)
    y = random.uniform(a, b)
    node = [x,y]
    nodes.append(node)
  return nodes

def connect_nodes(nodes, distance):
  adjacent = []
  for i, node in enumerate(nodes):
    neighbors = [x for x in nodes if x!=node]
    neighbor_list = []
    for j, neighbor in enumerate(neighbors):
      dist = sqrt(pow(neighbor[0] - node[0], 2) + pow(neighbor[1] - node[1],2))
      if (dist <= distance):
        neighbor_list.append(j)

    adjacent.append(neighbor_list)
  return adjacent

def cell_measurement(cell, node, q_bar):
  dist_center = [0.0, 0.0]
  dist_center[0] = node[0] - q_bar[0]
  dist_center[1] = node[1] - q_bar[1]
  dist_center_mag = pow(dist_center[0],2) + pow(dist_center[1],2)
  variance = (dist_center_mag + 0.01) / 2.56

  measurement = cell[2] + random.gauss(0, variance)
  node.append(measurement)
  return node

def q_bar_calc(nodes):
  pos_sum = [0.0, 0.0]
  for node in nodes:
    pos_sum[0] = pos_sum[0] + node[0]
    pos_sum[1] = pos_sum[1] + node[1]
  pos_sum[0] = pos_sum[0]/len(nodes)
  pos_sum[1] = pos_sum[1]/len(nodes)
  return pos_sum

def max_degree(node, neighbors, cell):
  pass

def consensus_filter(weight_func, nodes, adjacencies, cells):
  print weight_func(nodes[0], [nodes[i] for i in adjacencies[0]], cells[0])

def main():
  cell = [.5, .5, 50]
  nodes = generate_random_node_graph(10, 0, 1)
  nodes = [cell_measurement(cell, node, q_bar_calc(nodes)) for node in nodes]
  print nodes
  adjacencies = connect_nodes(nodes, .25)

if __name__ == '__main__':
  main()