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

def node_sub_pos(a, b):
  a = a - b
  return a

def max_degree(node, neighbors, cell, nodes, adjacent, central, node_dex=0, neigh_dex=0):
  if central:
    degree = len(neighbors)
    return (1 - degree * 1.0/len(nodes))
  return 1.0/len(nodes)

def metropolis(node, neighbors, cell, nodes, adjacent, central, node_dex=0, neigh_dex=0):
  if central:
    return (1 - sum([metropolis(node, neighbors, cell, nodes, adjacent, False, node_dex, i) for i in xrange(len(neighbors))]))
  return 1.0/(1 + max(len(neighbors), len(adjacent[adjacent[node_dex][neigh_dex]])))


def consensus_filter(weight_func, nodes, adjacencies, cells):
  print nodes
  for cell in cells:
    for l in xrange(100):
      node_consensus = []
      for i, node in enumerate(nodes):
        neighbors = [nodes[j] for j in adjacencies[i]]
        node_consensus.append(weight_func(node, neighbors, cell, nodes, adjacencies, True, i) * node[2] + sum([weight_func(node, neighbors, cell, nodes, adjacencies, False,i,j)*neighbors[j][2] for j in xrange(len(neighbors))]))
      for i in xrange(len(nodes)):
        nodes[i][2] = node_consensus[i]
    print nodes

def main():
  cell = [.5, .5, 50]
  nodes = generate_random_node_graph(10, 0, 1)
  nodes = [cell_measurement(cell, node, q_bar_calc(nodes)) for node in nodes]
  adjacencies = connect_nodes(nodes, .5)

  consensus_filter(metropolis, nodes, adjacencies, [cell])

if __name__ == '__main__':
  main()