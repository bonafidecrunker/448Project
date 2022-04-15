import os
from os.path import exists
from Logic import *
from Graph_Draw import *


k_leaf_power = 5

def main(k_leaf_power):
    # make the list of all graphs smaller if it contains a forbidden induced subgraph
    all_graphs = []
    all_graphs_g6 = set()
    all_canonized_induced_subgraphs = []
    all_canonized_induced_subgraphs_g6 = set()
    
    minimal_forbidden_dict = {}


    # loads all chosen graphs of input size 4 - whatever into all_graphs
    for graph_size in range(4, 9):
        file_path = f'labeled_graphs/std_geng{graph_size}_cl.g6'
        # loads in all graphs of node number index

        get_byte_strings(file_path, all_graphs)
        # for g in graphs:
        #     key = build_graph_key(g)
        #     all_graphs_g6.add(g)
        #     all_graphs.setdefault(key, []).append(g)

    for i in range(len(all_graphs)):
        all_graphs_g6.add(all_graphs[i][0])

    for graph_size in range(3, k_leaf_power + 1):
        file_path = f'induced_subgraphs/{graph_size}_leaf_power_canonized.g6'
        get_byte_strings(file_path, all_canonized_induced_subgraphs)

        for j in range(len(all_canonized_induced_subgraphs)):
            all_canonized_induced_subgraphs_g6.add(all_canonized_induced_subgraphs[j][0])

        k_node_induced = set()
        for pair in all_canonized_induced_subgraphs:
            k_node_induced.add(pair[0])
        all_forbiddens = all_graphs_g6 - k_node_induced
        # print(all_forbiddens)
        
        all_forbiddens_list = sorted(all_forbiddens, key=lambda x: len(x))
        
        min_forbiddens = set()
        
        for f_graph in all_forbiddens_list:
            if not graph_contains(f_graph, min_forbiddens):
                min_forbiddens.add(f_graph)

    
        minimal_forbidden_dict[graph_size] = [nx.from_graph6_bytes(n.encode("utf-8")) for n in min_forbiddens]

    while True:
        for k,v in minimal_forbidden_dict.items():
            counter = 0
            if len(v) > 12:
                for i in range(len(v)//12 + 1):
                    temp_v = v[counter: counter + 12]
                    draw_graphs(temp_v, f'{k}-leaf power minimal forbiddens pg. {(counter/12)}', subtitles=[build_graph_key(x) for x in temp_v])
                    counter += 12
            else:
                draw_graphs(v, f'{k}-leaf power minimal forbiddens', subtitles=[build_graph_key(x) for x in v])
        #print(len(min_forbiddens))
        


    # trees = load_all_graphs(20)
    # # loop starts here - k leaf power loop
    # for power in range(6, k_leaf_power + 1):
    #     print(f'{power} leaf powers\n')
    #     for tree in trees:
    #         nbunch = get_leaf_nodes(tree)
    #         temp_graph = nx.power(tree, power)
    #         induced_graph = nx.induced_subgraph(temp_graph, nbunch)
    #         if nx.is_connected(induced_graph):
    #             nx.write_graph6(induced_graph, f'induced_subgraphs\\{power}_leaf_power_induced_subgraphs.g6', header=False)


def get_byte_strings(filename, graph_set):
    temp_graph_list = nx.read_graph6(filename)
    with open(filename) as file:
        counter = 0
        lines = file.readlines()
        for line in lines:
            graph_set.append((line.strip(), temp_graph_list[counter]))
            counter += 1


def contains_known_forbidden_subgraph(all_forbidden_dict, graphs, index):
    """
    Function to check if a subgraph of each graph in graphs is contained in the list of known minimal forbidden
    induced subgraphs for k-leaf powers.

    :param all_forbidden_dict: dictionary containing all known minimal forbidden induced subgraphs
    :param graphs: list of graphs over which to compare to graphs in all_forbidden_dict
    :param index:
    :return: True if graph is found, False otherwise
    """

    # if all_forbidden_dict is empty, it cannot contain a forbidden subgraph
    if not bool(all_forbidden_dict):
        return False

    for graph in graphs:
        if index in all_forbidden_dict.keys():
            if build_graph_key(graph) in all_forbidden_dict[index - 1]:
                return True
    return False


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
    for i in range(4, index + 1):
        nodes_and_diameters = [i for i in range(index + 1)]  # default value is 15 but can be higher if we want
        for nodes in nodes_and_diameters:
            filename_ends_with = str(nodes) + '.' + str(i) + '.g6'
            temp_graphs = load_all_graphs_helper(filename_ends_with)
            graphs.update(temp_graphs)
    return graphs


def load_all_graphs_helper(file_ends_with='.g6'):
    """
    Given a file containing some numbers of graphs (>= 1), load those graphs into a set.

    :param file_ends_with:
    :return: a set of graphs from the g6 file
    """
    graphs_set = set()
    directory = os.fsdecode('partitioned_trees')
    temp = '{0}\\Tree{1}'.format(str(directory), str(file_ends_with))
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
    Takes in a list of graphs and partitions the graphs in the files into files that contain only trees of the
    specified number of nodes (n), and leaves (l). As trees of n.l are found, they are appended to the
    output file rather than overwritten. Additionally, the trees are specifically added as g6 bytes for ease of reading
    and comparison down the line.

    :param graphs: a list of graphs
    """
    for g in graphs:
        nodes = len(g.nodes)
        leaves = 0
        for node in g.degree():
            if node[1] == 1:
                leaves += 1
        if leaves > 3:
            filename = build_filename(nodes, leaves)
            with open("partitioned_trees/" + filename, "a+") as f:
                f.write(nx.to_graph6_bytes(g).decode("utf-8").replace(">>graph6<<", ""))


def build_filename(nodes, leaves):
    return f"Tree{nodes}.{leaves}.g6"


def build_graph_key(graph):
    return '.'.join([str(c) for c in node_degree_func(graph)]) if type(graph) != str else graph


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


def graph_contains(test_string, min_forbidden):
    # if min_forbidden is empty, there can be no extant subgraph in it
    if not min_forbidden:
        return False

    temp_graph = nx.from_graph6_bytes(test_string.encode("utf-8"))
    for min_f in min_forbidden:
        temp_forbidden_graph = nx.from_graph6_bytes(min_f.encode("utf-8"))
        temp_forbidden_size = len(temp_forbidden_graph.nodes())
        combinations = list(itertools.combinations(temp_graph.nodes(), temp_forbidden_size))
        for c in combinations:
            g = temp_graph.subgraph(c).copy()
            if nx.is_isomorphic(temp_forbidden_graph, g):
                return True
    return False


def load_g6_leaf2():
    # Loads and returns all graphs in all files as a single list
    directory = os.fsencode('tree_files')
    graphs = []
    # out = []
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        path_string = str(directory.decode('utf-8')) + "\\" + str(filename.decode('utf-8'))
        graph = nx.read_sparse6(path_string)
        if type(graph) is list:
            for g in graph:
                temp = nx.Graph(g)
                graphs.append(temp)
                # out.append(filename)
        else:
            graphs.append(graph)
            # out.append(filename)
    return graphs


main(k_leaf_power)


class G6_NX_Graphs:
    def __init__(self, g6_string, nx_graph):
        self.g6_string = g6_string
        self.nx_graph = nx_graph

    def get_g6_string(self):
        return self.g6_string

    def get_nx_graph(self):
        return self.nx_graph


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