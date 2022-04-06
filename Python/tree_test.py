import os
from os.path import exists
import networkx as nx
from Graph_Draw import *
from Logic import *


def main(k_leaf_power):
    # make the list of all graphs smaller if it contains a forbidden induced subgraph
    all_graphs_k = {}
    all_forbidden_dict = {}
    minimal_forbidden_dict = {}
    trees = load_all_graphs()
    # loads in all graphs of node number index
    for i in range(4, index + 1):
        file_path = f'graph_files/std_geng{i}_c.g6'
        graphs = nx.read_graph6(file_path)
        for g in graphs:
            key = node_degree_func(g)
            key2 = '.'.join([str(c) for c in key])
            all_graphs_k.setdefault(key2, []).append(g)
    induced_graph_dict = {}


    # """
    # 1.1.2.3.3 -> Bull
    # 1.2.2.3.4 -> Dart
    # 2.2.3.3.4 -> Gem
    # """

    # loop starts here - k leaf power loop
    
    
    
    for tree in trees:
        nbunch = get_leaf_nodes(tree)
        temp_graph = nx.power(tree, k_leaf_power)
        induced_graph = nx.induced_subgraph(temp_graph, nbunch)     
        key = build_graph_key(induced_graph)
        if key == '1.1.1.3':
            print(f"missing {key}")
        if nx.is_connected(induced_graph):
            induced_graph_dict.setdefault(key, []).append(tree)



# set like operation to build a dictionary containing the difference all_graphs - induced_graphs
    temp_forbidden_dict = {k: v for k, v in all_graphs_k.items() if k not in induced_graph_dict}
    #print(induced_graph_dict)
    print('temp forb', temp_forbidden_dict.keys())
    for k, v in temp_forbidden_dict.items():
        # check for k_leaf_power - 1 all_forbidden_dict : if true - add here
    


        if contains_known_forbidden_subgraph(minimal_forbidden_dict, v, k_leaf_power - 1):
           all_forbidden_dict.setdefault(k_leaf_power, []).append(k)
        # false add here
        else:
           minimal_forbidden_dict.setdefault(k_leaf_power, []).append(k)
        # add to another dict all_minimal_forbidden
    
    #print('internal minimal' , minimal_forbidden_dict)

    # loop ends here
    print('forbidden', all_forbidden_dict)

    square = nx.from_edgelist([(0, 1), (1, 2), (2, 3), (3, 0)])
    print('minimal', minimal_forbidden_dict)


def contains_known_forbidden_subgraph(dict_in, graphs, index):
    """
    Function to check if a subgraph of each graph in graphs is contained in the list of known minimal forbidden
    induced subgraphs for k-leaf powers.

    :param all_forbidden_dict: dictionary containing all known minimal forbidden induced subgraphs
    :param graphs: list of graphs over which to compare to graphs in all_forbidden_dict
    :return: True if graph is found, False otherwise
    """
    bool_arr = []

    # if all_forbidden_dict is empty, it cannot contain a forbidden subgraph
    if not bool(dict_in):
        return False
    for graph in graphs:
        if  index in dict_in.keys():
            temp_key = build_graph_key(graph)
            for v in dict_in.get(index):
                if type(v) == list:
                    for v_i in v:
                        temp_v = build_graph_key(v_i)
                        if temp_key == temp_v:  
                            bool_arr.append(True)
                        else:
                             bool_arr.append(False)
                else:
                    if temp_key == v:
                         bool_arr.append(True)
                    else:
                         bool_arr.append(False)
                         
    return bool_arr


def remove_one_node(graph):
    """
    Function that takes in a graph and removes a single node from it at a time, produces a new graph, and adds it to a
    list of output graphs. For use with contains_known_forbidden_subgraph()

    :param graph: a graph from which to remove a single node at a time
    :return: list of graphs with one node removed
    """
    graph_out_list = []
    for i in graph.nodes:
        temp_graph = nx.from_edgelist(graph.edges)
        temp_graph.remove_node(i)
        graph_out_list.append(temp_graph)
    return graph_out_list


def node_degree_func(graph):
    """
    Returns a sorted list by the number of degrees of each node in the graph.

    :param graph: a networkx graph
    :return: sorted list with degrees of each node in graph
    """
    node_degree = []
    for node in graph.degree():
        node_degree.append(node[1])
    node_degree = sorted(node_degree)
    return node_degree


def get_leaf_nodes(graph):
    """
    Function to return a list of leaf nodes in a networkx graph.

    :param graph: networkx graph
    :return: list of leaf nodes
    """
    out = []
    for node in graph.degree():
        if node[1] == 1:
            out.append(node[0])
    return out


def load_all_graphs(index=15):
    """
    Loads all graphs of given diameter index for all trees. Returns a set networkx graphs.

    :param index: diameter of the tree for which to load tree files
    :return: set of networkx graphs
    """
    graphs = set()
    # if index is not None:
    for i in range(3, index):
        nodes_and_diameters = [i for i in range(index + 1)]  # default value is 15 but can be higher if we want
        for nodes in nodes_and_diameters:
            for diameter in nodes_and_diameters:
                filename_ends_with = str(nodes) + '.' + str(diameter) + '.' + str(i) + '.g6'
                temp_graphs = load_all_graphs_helper(filename_ends_with)
                graphs.update(temp_graphs)
    # else:
    #     temp_graphs = load_all_graphs_helper()
    #     graphs.update(temp_graphs)
    return graphs


def load_all_graphs_helper(file_ends_with='.g6'):
    """
    Given a file containing some numbers of graphs (>= 1), load those graphs into a set.

    :param file_ends_with:
    :return: a set of graphs from the g6 file
    """
    graphs_set = set()
    directory = os.fsdecode('leaf_files')  
    temp = str(directory) + '\Tree' + str(file_ends_with)
    if exists(temp):
        graph = nx.read_graph6(temp)

        # if there is more than one graph in the file
        if type(graph) is list:
            for g in graph:
                temp_graph = nx.Graph(g)
                graphs_set.add(temp_graph)
        else:
            graphs_set.add(graph)
    return graphs_set


def partition(graphs):
    """
    Takes in a list of tree files and partitions the graphs in the files into files that contain only trees of the
    specified number of nodes (n), diameter (d), and leaves (l). As trees of n.d.l are found, they are appended to the
    output file rather than overwritten. Additionally, the trees are specifically added as g6 bytes for ease of reading
    and comparison down the line.

    :param graphs: a list of graphs
    """
    for g in graphs:
        nodes = len(g.nodes)
        diameter = nx.diameter(g)
        leaves = 0
        for node in g.degree():
            if node[1] == 1:
                leaves += 1
        filename = build_filename(nodes, diameter, leaves)
        with open("leaf_files2/"+filename, "a+") as f:
            f.write(nx.to_graph6_bytes(g).decode("utf-8").replace(">>graph6<<", ""))


def build_filename(nodes, diameter, leaves):
    return f"Tree{nodes}.{diameter}.{leaves}.g6"


def build_graph_key(graph):
    return '.'.join([str(c) for c in node_degree_func(graph)])


k_leaf_power = 2
#main(index, k_leaf_power)


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