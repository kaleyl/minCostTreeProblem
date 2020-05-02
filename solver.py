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
        T = solveGraph(G)
    return T


def solveTree(G):
    """ solve for tree 
    - evaluating whether a leaf is worth adding to T
    
    """
    nonleaf = [v for v in G.nodes() if G.degree[v] > 1]
    T = G.subgraph(nonleaf).copy()
    count = len(nonleaf)
    avg = T.size(weight = 'weight') / count
    leafs = [v for v in G.nodes() if G.degree[v] == 1]
    for v in leafs:
        u = G.neighbors(v)
        weight = G.get_edge_data(v, u, default=0)
        if weight < avg and weight != 0:
            T.add_node(v)
            avg += weight / (count + 1)
            count += 1
    return T

def solveGraph(G):
    # using dominating set to solve for general case
    '''
    Look for all ds and calculate the shortest path that connects
    all the vertices in the ds.
    return the ds with the shortest path.
    '''
    minSet = None
    minSize = G.size(weight = 'weight') / G.number_of_edges()
    for v in G.nodes():
        ds = nx.dominating_set(G, v)
        if len(ds) == 1:
            minSet = ds
            break;
        temp = G.subgraph(ds).copy()
        if nx.is_connected(temp):
            avg = temp.size(weight = 'weight') / temp.number_of_edges()
            if  avg < minSize:
                minSet = ds
                minSize = avg 
    if minSet == None:
        return nx.minimum_spanning_tree(G, weight='weight')
    else :
        T = nx.Graph()
        for v in minSet:
            T.add_node(v)
        return T


def getShortestPath(G, ds):
    return


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
