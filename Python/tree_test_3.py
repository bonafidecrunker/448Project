from ast import Return
import os
from os.path import exists
import networkx as nx
from numpy import True_
from Graph_Draw import *
from Logic import *
from tree_test import remove_one_node, load_all_graphs, node_degree_func, get_leaf_nodes, build_graph_key
from networkx import isomorphism
import itertools


def main():
    num_graph_nodes = 5
    leaf_power = 3
    find_forbiddens(num_graph_nodes, leaf_power)

def find_forbiddens(num_graph_nodes, leaf_power):
    all_forbiddens = {}
    minimal_forbiddens = {}
    all_graphs = []
    all_trees = load_all_graphs()

    for num_nodes in range(4, num_graph_nodes + 1):
            file_path = f'graph_files/std_geng{num_nodes}_c.g6'
            graphs = nx.read_graph6(file_path)
            for graph in graphs:
                all_graphs.append(graph)

    #Checking leaf power L for all graphs

    for power in range(3, leaf_power + 1):
        induced_graph_list = []
        induced_graph_set = set()
        for tree in all_trees:
            nbunch = get_leaf_nodes(tree)
            if len(nbunch) == 4:
                tree_to_power = nx.power(tree, power)
                induced_graph = nx.induced_subgraph(tree_to_power, nbunch)
                if nx.is_connected(induced_graph):
                    induced_graph_list.append(induced_graph)
                    induced_graph_set.add(induced_graph)


    all_graphs_copy = all_graphs.copy()

    
    for g in all_graphs:
        if not contains_iso(g, induced_graph_set):
            all_forbiddens.setdefault(3, []).append(g)
    draw_graphs(all_forbiddens[3])


def contains_iso(graph, induced_graphs):
    for g2 in induced_graphs:
        if is_isomorphic(graph, g2):
            return True
    return False
            
            


def is_isomorphic(g1, g2):
    gm = isomorphism.GraphMatcher(g1,g2)
    return gm.is_isomorphic()

main()