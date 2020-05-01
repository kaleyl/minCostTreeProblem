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
    T = nx.minimum_spanning_tree(G)
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
