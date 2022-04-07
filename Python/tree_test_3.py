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
from networkx.utils import graphs_equal


def main():
    num_graph_nodes = 6
    leaf_power = 4
    find_forbiddens(num_graph_nodes, leaf_power)

def find_forbiddens(num_graph_nodes, leaf_power):
    counter_array = [0,0,0,0,0,0,0]
    induced_counter_array = [0] * 16
 
    minimal_forbiddens = {}
    all_graphs = []
    all_trees = load_all_graphs()

    for num_nodes in range(4, num_graph_nodes + 1):
            file_path = f'graph_files/std_geng{num_nodes}_c.g6'
            graphs = nx.read_graph6(file_path)
            for graph in graphs:
                all_graphs.append(graph)
                counter_array[num_nodes-1] += 1

    #Checking leaf power L for all graphs

    for power in range(3, leaf_power + 1):
        all_forbiddens = []     
        minimal_forbiddens_removal = []
        induced_graph_list = []
        induced_graph_set = set()
        for tree in all_trees:
            nbunch = get_leaf_nodes(tree)
            tree_to_power = nx.power(tree, power)
            induced_graph = nx.induced_subgraph(tree_to_power, nbunch)
            if nx.is_connected(induced_graph) and not contains_iso(induced_graph, induced_graph_list):
                induced_graph_list.append(induced_graph)
                induced_graph_set.add(induced_graph)
                induced_counter_array[len(nbunch)-1] += 1
        
        for g in all_graphs:
            if not contains_iso(g, induced_graph_set):
                all_forbiddens.append(g)
        
        # draw_graphs(all_forbiddens)
        min_forb_copy = all_forbiddens.copy()
        for a_f in all_forbiddens:
            if contains_forb_2(a_f, all_forbiddens):      
                for min_f in all_forbiddens:
                    if graphs_equal(min_f, a_f):
                        min_forb_copy.remove(min_f)
        

        for min_forb in min_forb_copy:
            minimal_forbiddens.setdefault(power, []).append(min_forb)

    
    for k, v in minimal_forbiddens.items():
        draw_graphs(v, k)


def contains_iso(graph, induced_graphs):
    for g2 in induced_graphs:
        if is_isomorphic(graph, g2):
            return True
    return False

def contains_forb_2(graph, all_forbiddens):
    nodes = list(graph.nodes)
    for forb_g in all_forbiddens:
        combinations = list(itertools.combinations(nodes, len(forb_g.nodes)))
        for comb in combinations:
            G = graph.subgraph(comb).copy()
            if nx.is_connected(G):
                if is_isomorphic(forb_g, G) and forb_g != graph:
                    return True
    return False
            
def contains_forb(graph, all_forbiddens):
    for forb_g in all_forbiddens:       
        nodes = list(graph.nodes)
        combinations = list(itertools.combinations(nodes, len(forb_g.nodes)))
        for comb in combinations:
            G = graph.subgraph(comb).copy()       
            if is_isomorphic(forb_g, G):
                print('true', comb)
                return True
    return False          


def is_isomorphic(g1, g2):
    gm = isomorphism.GraphMatcher(g1,g2)
    return gm.is_isomorphic()

main()


class Graph(nx.Graph):
    def __eq__(self, other):
        return isomorphism.GraphMatcher(self,other).is_isomorphic()
