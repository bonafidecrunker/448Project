from functools import reduce
import networkx as nx
from numpy import empty
from TreeIn import *
import os
from os.path import exists
from Graph_Draw import *
from Logic import *
import pandas as pd


def main(index):
    """
    possible degree lists for graphs of four nodes:
    [1,1,2,2] => p4
    [1,1,1,3] => arrow head
    [1,2,2,3] => bow and arrow
    [2,2,2,2] => c4 (square)
    [2,2,3,3] => one outer edge (non chordal) removed from max clique
    [3,3,3,3] => max clique
    """

    four_vertex_graphs = set()
    induced_graphs_set = set()

    four_vertex_dict = {}
    induced_graph_dict = {}

    file_path = 'graph_files/std_geng4_c.g6'
    graphs = nx.read_graph6(file_path)
    for g in graphs:
        four_vertex_graphs.add(g)
        key = node_degree_func(g)
        key2 = '.'.join([str(c) for c in key])
        four_vertex_dict.setdefault(key2, []).append(g)

    for i in range(2, index + 1):
        trees = load_all_graphs(index)
        for tree in trees:
            nbunch = get_leaf_nodes(tree)
            temp_graph = nx.power(tree, index)
            induced_graph = nx.induced_subgraph(temp_graph, nbunch)
            if nx.is_connected(induced_graph):
                induced_graphs_set.add(induced_graph)
                key = node_degree_func(induced_graph)
                key2 = '.'.join([str(c) for c in key])
                induced_graph_dict.setdefault(key2, []).append(tree)

    forbidden_dict = {k: v for k, v in four_vertex_dict.items() if k not in induced_graph_dict}
    print(forbidden_dict)


def node_degree_func(graph):
    node_degree = []
    for node in graph.degree():
        node_degree.append(node[1])
    node_degree = sorted(node_degree)
    return node_degree


def get_leaf_nodes(test_graph):
    out = []
    for node in test_graph.degree():
        if node[1] == 1:
            out.append(node[0])

    return out


def load_all_graphs(index=None):
    graphs = set()
    if index is not None:
        nodes_and_diameters = [i for i in  range(2 * index + 2)]
        for nodes in nodes_and_diameters:
            for diameter in nodes_and_diameters:
                filename_ends_with = str(nodes) + '.' + str(diameter) + '.' + str(index) + '.g6'
                temp_graphs = load_graph(filename_ends_with)
                graphs.update(temp_graphs)
    else:
        temp_graphs = load_graph()
        graphs.update(temp_graphs)
    return graphs


def load_graph(file_ends_with='.g6'):
    graphs_set = set()
    directory = os.fsdecode('leaf_files')  
    temp = str(directory) + '\Tree' + str(file_ends_with)
    if exists(temp):
        graph = nx.read_graph6(temp)
        if type(graph) is list:
            for g in graph:
                temp_graph = nx.Graph(g)
                graphs_set.add(temp_graph)
        else:
            graphs_set.add(graph)
    return graphs_set


def partition(graphs):
    for g in graphs:
        n = len(g.nodes)
        d = nx.diameter(g)
        l = 0
        for node in g.degree():
            if node[1] == 1:
                l += 1
        filename = build_filename(n, d, l)
        with open("leaf_files2/"+filename, "a+") as f:
            f.write(nx.to_graph6_bytes(g).decode("utf-8").replace(">>graph6<<", ""))


def build_filename(n, d, l):
    return "Tree"+str(n)+"."+str(d)+"."+str(l)+'.g6'


main(4)

"""
Old code - May still use

def label_map_to_graph(graph):
    nodes = graph.nodes()
    edges = graph.edges()
    new_edges = []
    mapper = {}
    counter = 0
    for node in nodes:
        mapper[node] = counter 
        counter += 1
    for edge in edges:
        new_edge = (mapper[edge[0]], mapper[edge[1]])
        new_edges.append(new_edge)
    return nx.from_edgelist(new_edges)



def load_g6_leaf2():
    # Loads and returns all graphs in all files as a single list

    # :return: list of every single individual graph from each file
    
    directory = os.fsencode('leaf_files')
    graphs = []
    out = []
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        path_string = str(directory.decode('utf-8')) + "\\" + str(filename.decode('utf-8'))
        graph = nx.read_graph6(path_string)
        if type(graph) is list:
            for g in graph:
                temp = nx.Graph(g)
                graphs.append(temp)
                out.append(filename)
        else:
            graphs.append(graph)
            out.append(filename)
    return graphs, out

"""