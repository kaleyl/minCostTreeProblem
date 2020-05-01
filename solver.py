import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from collections import defaultdict
import sys
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    numNodes = G.number_of_nodes()
    numEdges = G.number_of_edges()
    if G.number_of_nodes() == 3 and G.number_of_edges == 2:
        return G
    if numEdges == numNodes * (numNodes -1) / 2:
        T = nx.Graph()
        T.add_node(list(G)[0])
    elif numEdges == (numNodes- 1):
        T = solveTree(G)
    else : 
        T = nx.minimum_spanning_tree(G)
    return T


def solveTree(G):
    nonleaf = [v for v in G.nodes() if G.degree[v] > 1]
    T = G.subgraph(nonleaf).copy()
    avg = T.size(weight='weight') / len(nonleaf)
    leafs = [v for v in G.nodes() if G.degree[v] == 1]
    for v in leafs:
        u = G.neighbors(v)
        weight = G.get_edge_data(v, u, default=0)
        if weight < avg and weight != 0:
            T.add_node(v)
            avg += weight
    return T

# Usage: python3 solver.py inputs
if __name__ == '__main__':
    assert len(sys.argv) == 2
    dir = sys.argv[1]
    for path in os.listdir(dir):
    	G = read_input_file(dir + '/' + path)
    	T = solve(G)
    	assert is_valid_network(G, T)
    	print("Average pairwise distance: {}".format(average_pairwise_distance(T)))
    	write_output_file(T, 'outputs/' + path[:(len(path)-3)] + '.out')
