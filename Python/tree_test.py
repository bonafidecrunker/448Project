import os
from os.path import exists
from Graph_Draw import *
from Logic import *


def main(index, k_leaf_power):
    # make the list of all graphs smaller if it contains a forbidden induced subgraph

    forbidden_dict = {}

    vertex_dict = {}
    induced_graph_dict = {}

    # loads in all graphs of node number index
    file_path = f'graph_files/std_geng{index}_c.g6'
    graphs = nx.read_graph6(file_path)
    for g in graphs:
        key = node_degree_func(g)
        key2 = '.'.join([str(c) for c in key])
        vertex_dict.setdefault(key2, []).append(g)
        if key2 == '1.1.2.3.3' or key2 == '1.2.2.3.4' or key2 == '2.2.3.3.4':
            print(f'{key2} is not allowed')

    # for files of name Tree.n.d.l where l is index, takes the k_leaf_power of each graph up to k_leaf_power times and
    # adds it to a set (dictionary) of computed induced graphs
    for i in range(2, index + 1):
        trees = load_all_graphs(index)
        for tree in trees:
            nbunch = get_leaf_nodes(tree)
            temp_graph = nx.power(tree, i)
            induced_graph = nx.induced_subgraph(temp_graph, nbunch)
            if nx.is_connected(induced_graph) and nx.diameter(induced_graph) <= k_leaf_power:
                key = node_degree_func(induced_graph)
                key2 = '.'.join([str(c) for c in key])
                #Check if graph - each node exists within forbidden_dict, if it does not add to induced graph_dict
                induced_graph_dict.setdefault(key2, []).append(tree)

    temp_forbidden_dict = {k: v for k, v in vertex_dict.items() if k not in induced_graph_dict}
    for value in temp_forbidden_dict.values():
        print(temp_forbidden_dict.keys())

    for k, v in temp_forbidden_dict.items():
        forbidden_dict.setdefault(k, []).append(v)

    print(forbidden_dict)
    for v in temp_forbidden_dict.values():
        draw_graphs(v)


def remove_one_node(graph):
    """
    Function to remove each node once and add it to a list
    :param graph:
    :return: list of graphs with one node removed
    """
    graph_out_list = []
    node_list = list(graph.nodes)
    print(node_list)
    for i in node_list:
        temp_graph = graph.remove_node(i)
        graph_out_list.append(temp_graph)
    print(graph_out_list)
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


def load_all_graphs(index=None):
    """
    Loads all graphs of given diameter index for all trees. Returns a set networkx graphs.

    :param index: diameter of the tree for which to load tree files
    :return: set of networkx graphs
    """
    graphs = set()
    if index is not None:
        nodes_and_diameters = [i for i in range(16)]  # only considering graphs and trees up to 15 nodes for now
        for nodes in nodes_and_diameters:
            for diameter in nodes_and_diameters:
                filename_ends_with = str(nodes) + '.' + str(diameter) + '.' + str(index) + '.g6'
                temp_graphs = load_all_graphs_helper(filename_ends_with)
                graphs.update(temp_graphs)
    else:
        temp_graphs = load_all_graphs_helper()
        graphs.update(temp_graphs)
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


index = 5
k_leaf_power = 6
main(index, k_leaf_power)


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