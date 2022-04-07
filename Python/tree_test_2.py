import os
from os.path import exists
import networkx as nx
from Graph_Draw import *
from Logic import *
from tree_test import remove_one_node, load_all_graphs, node_degree_func, get_leaf_nodes, build_graph_key
from networkx import isomorphism

num_graph_nodes = 5
leaf_power = 3

def main(num_graph_nodes, leaf_power):
    
    all_forbiddens = {}
    
    all_forbiddens_2 = {}
    minimal_forbiddens = {}
    all_graphs = {}
    all_trees = load_all_graphs()
    #print(len(all_trees))
    counter = 0
    for num_nodes in range(4, num_graph_nodes + 1):
        all_graphs.clear()
        file_path = f'graph_files/std_geng{num_nodes}_c.g6'
        graphs = nx.read_graph6(file_path)
        for graph in graphs:
            key = node_degree_func(graph)
            key_str = '.'.join([str(c) for c in key])
            all_graphs.setdefault(key_str, []).append(graph)
        
        induced_graph_dict = {}
        for tree in all_trees:
            nbunch = get_leaf_nodes(tree)
            tree_to_power = nx.power(tree, leaf_power)
            induced_graph = nx.induced_subgraph(tree_to_power, nbunch)
            
 
            if nx.is_connected(induced_graph):
                induced_key = build_graph_key(induced_graph)
                induced_graph_dict.setdefault(induced_key, []).append(tree)

        #print('connected counter:', counter)
        temp_forbidden_dict = {k: v for k, v in all_graphs.items() if k not in induced_graph_dict}

        #print('temp forbidden dict', temp_forbidden_dict.keys())
        for k, v in temp_forbidden_dict.items():
            all_forbiddens_2.setdefault(leaf_power + counter, []).append(k)
            all_forbiddens.setdefault(leaf_power, {}.setdefault(k, [])).append(v)
        counter += 1

    print(all_forbiddens_2)    
    # contains_forbidden_subgraph(all_forbiddens)
    # for k,v in all_forbiddens.items():
    #     print('power ', k)
    #     for key in v:
    #         for k in key:
    #             print(k)


def contains_forbidden_subgraph(all_forbiddens):
    power_list = list(all_forbiddens.keys())
    power_list.sort(reverse=True)
    for power in power_list:
        temp_dict = all_forbiddens[power]
        if power - 1 in all_forbiddens.keys():
            for v in temp_dict:
                # if inner list has more than one graph per key
                if len(v) > 1:
                    for graph in v:
                        temp_remove_one_node = remove_one_node(graph)
                        compared_graphs = [i for i in  temp_remove_one_node if i in all_forbiddens[power - 1]]
                        print(len(temp_remove_one_node))
                else:
                    one_node_smaller_graphs = remove_one_node(v[0])
                    compared_graphs = [i for i in  one_node_smaller_graphs if i in all_forbiddens[power - 1]]
                    print(len(one_node_smaller_graphs))



def is_isomorphic(g1, g2):
    gm = isomorphism.GraphMatcher(g1,g2)
    return gm.is_isomorphic()


#main(num_graph_nodes, leaf_power)


