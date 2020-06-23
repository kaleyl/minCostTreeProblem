import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
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
    '''
    numNodes = G.number_of_nodes()
    numEdges = G.number_of_edges()
    sortedNodes = sorted(G.degree, key=lambda x: x[1], reverse=True)
    if G.number_of_nodes() == 3 and G.number_of_edges == 2:
        return G
    elif G.degree(sortedNodes[0]) == numNodes - 1:
        return sortedNodes[0]
    if numEdges == numNodes * (numNodes - 1) / 2:
        T = nx.Graph()
        T.add_node(list(G)[0])
    elif numEdges == (numNodes- 1):
        T = solveTree(G)
    else : 
        T = solveGraph(G)
    return T
    '''
    return greedy(G)

def new_kruskal(G, weight='weight'):
    from networkx.utils import UnionFind
    from random import choice

    T = G.__class__()
    if len(G) == 1:
        return G
    subtrees = UnionFind()
    d = {}
    for node in G.nodes():
        G_copy = nx.Graph(G)
        G_copy.remove_node(node)
        if not nx.is_connected(G_copy):
            d[node] = float('inf')
        else:
            d[node] = average_pairwise_distance_fast(G_copy)
    def kruskal_key(t):
        u, v, d = t
        return d[u] + d[v]
    edges = sorted(G.edges(data=True), key=lambda t: d[t[0]] + d[t[1]], reverse=True)
    for u, v, d in edges:
        if G.degree[u] == G.number_of_nodes() - 1 and not G.has_edge(u, u):
            T = nx.Graph()
            T.add_node(u)
            return T
        if G.degree[v] == G.number_of_nodes() - 1 and not G.has_edge(v, v):
            T = nx.Graph()
            T.add_node(v)
            return T
        if (u == v):
            continue
        if subtrees[u] != subtrees[v]:
            T.add_node(u)
            T.add_node(v)
            T.add_edge(u, v, weight=d.get('weight', 1))
            subtrees.union(u, v)
        if nx.is_tree(T) and nx.is_dominating_set(G, T.nodes):
            break
    old_T = nx.Graph(T)
    while True:
        edges_T = sorted(T.edges(data=True), key=lambda t: t[2].get('weight', 1), reverse=True)
        for u, v, d in edges_T:
            avg_pairwise_dist = average_pairwise_distance_fast(T)
            T.remove_edge(u, v)
            graphs = list(T.subgraph(c).copy() for c in nx.connected_components(T))
            if nx.is_tree(graphs[0]) and nx.is_dominating_set(G, graphs[0].nodes):
                new_avg_pairwise_dist = average_pairwise_distance_fast(graphs[0])
                if new_avg_pairwise_dist > avg_pairwise_dist:
                    T.add_edge(u, v, weight=d.get('weight', 1))
                else:
                    T = nx.Graph(graphs[0])
                    if len(graphs[1]) > 1:
                        break
            elif nx.is_tree(graphs[1]) and nx.is_dominating_set(G, graphs[1].nodes):
                new_avg_pairwise_dist = average_pairwise_distance_fast(graphs[1])
                if new_avg_pairwise_dist > avg_pairwise_dist:
                    T.add_edge(u, v, weight=d.get('weight', 1))
                else:
                    T = nx.Graph(graphs[1])
                    if len(graphs[0]) > 1:
                        break
            else:
                T.add_edge(u, v, weight=d.get('weight', 1))
        if len(old_T) == len(T): break
        old_T = nx.Graph(T)
    return T

def greedy(G, weight='weight'):
    from random import choice

    T = G.__class__()
    if len(G) == 1:
        return G
    node = choice(list(G.nodes()))
    next_edges = list(G.edges(node, data=True))
    T.add_node(node)

    def heuristic(edge):
        if edge[0] == edge[1]: return float('inf')
        T_copy = nx.Graph(T)
        T_copy.add_edge(edge[0], edge[1], weight=edge[2].get('weight', 1))
        T_copy.add_node(edge[0])
        T_copy.add_node(edge[1])
        if not nx.is_tree(T_copy): return float('inf')
        return average_pairwise_distance_fast(T_copy)

    while True:
        curr_avg = average_pairwise_distance_fast(T)
        min_edge = min(next_edges, key=heuristic)
        min_new_avg = heuristic(min_edge)
        if is_valid_network(G, T) and min_new_avg > curr_avg:
            break
        else:
            if T.has_node(min_edge[0]):
                T.add_node(min_edge[1])
                T.add_edge(min_edge[0], min_edge[1], weight=min_edge[2].get('weight', 1))
                next_edges = next_edges + (list(G.edges(min_edge[1], data=True)))
            elif T.has_node(min_edge[1]):
                T.add_node(min_edge[0])
                T.add_edge(min_edge[0], min_edge[1], weight=min_edge[2].get('weight', 1))
                next_edges = next_edges + (list(G.edges(min_edge[0], data=True)))
            next_edges = list(filter(lambda e: not (e[0] == min_edge[0] and e[1] == min_edge[1]) and not (e[0] == min_edge[1] and e[1] == min_edge[0]), next_edges))

    return T



def solveTree(G):
    """ solve for tree 
    - evaluating whether a leaf is worth adding to T
    
    """
    nonleaf = [v for v in G.nodes() if G.degree[v] > 1]
    T = G.subgraph(nonleaf).copy()
    avg = average_pairwise_distance_fast(T)
    leafs = [v for v in G.nodes() if G.degree[v] == 1]
    for v in leafs:
        u = G.neighbors(v)
        weight = G.get_edge_data(v, u, default=0)
        if weight < avg and weight != 0:
            T.add_node(v)
            tempAvg = average_pairwise_distance_fast(T)
            if tempAvg > avgv:
                T.remove_node(v)
            else:
                avg = tempAvg
    return T




# Usage: python3 solver.py inputs
if __name__ == '__main__':
    assert len(sys.argv) == 2
    dir = sys.argv[1]
    for path in os.listdir(dir):
        print(path)
        G = read_input_file(dir + '/' + path)
        T = solve(G)
        assert is_valid_network(G, T)
        print("Average pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'outputs/' + path[:(len(path) - 3)] + '.out')

