from functools import reduce
import networkx as nx
from TreeIn import *
import os
from Graph_Draw import *
from Logic import *
import pandas as pd


def main():
    # test2 = nx.from_edgelist([(0, 1), (1, 2), (2, 3), (3, 0)])
    # nx.add_cycle(test2, [3, 6, 5, 3, 2])
    # nx.add_cycle(test2, [3, 4, 0])
    # nx.add_cycle(test2, [3, 4, 6])
    # v_d_l = ['7', '4', '4']  # Vertex, Diameter, Leaf
    # leaf_power = 2
    # test_file = '.'.join(v_d_l)
    # # graph = nx.read_graph6('leaf_files/Tree' + test_file + '.g6')
    # # if isinstance(graph, list):
    # #    graph = graph[0]
    # graph = test2
    # draw_graph(graph, test_file)
    # graph = nx.to_numpy_matrix(graph)
    # test = Logic.k_leaf_power(graph, leaf_power)
    # test = reduce_to_ones(test)
    # test = test.astype(int)
    # test = pd.DataFrame(test, columns=range(int(v_d_l[0])), index=range(int(v_d_l[0])))
    # print(test)
    #
    # graph_square = nx.from_pandas_adjacency(test)
    # clique_counter = 0
    # for clq in nx.clique.find_cliques(graph_square):
    #     clique_counter = clique_counter + 1
    #     print(clq)
    #
    # for cycle in nx.cycle_basis(graph_square):
    #     if len(cycle) > 3:
    #         print("cycle " + str(cycle))
    # draw_graph(graph_square, test_file + ' Leaf Power: ' + str(leaf_power) + ', # of cliques: ' + str(clique_counter))

    trees_filepath = 'leaf_files/Tree7.3.5.g6'
    graphs_filepath = 'graph_files/std_geng7_c.g6'
    compare_trees_graphs(graphs_filepath, trees_filepath, 4)

    exit(0)


def draw_partitioned_graphs(graphs, names):
    out = {}
    for i in range(len(graphs)):
        print(names[i], graphs[i])
        out.setdefault(names[i],[]).append(graphs[i])

    for key in out.keys():
        if len(out.get(key)) > 1:
            draw_graphs(out.get(key), key)
        else:
            draw_graph(out.get(key)[0], key)


def load_all_graphs():
    directory = os.fsencode('tree_files_subset2')
    graphs = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.txt'):
            temp = str(directory.decode("utf-8")) + "\\" + str(filename)
            g = TreeIn(temp)
            for i in g.get_graphs():
                graphs.append(i)
    return graphs


def load_g6_leaf(bool):
    directory = os.fsencode('leaf_files')
    graphs = []
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        if filename.startswith('Tree'.encode("utf-8")):
            temp = str(directory.decode("utf-8") + "\\" + filename.decode("utf-8"))
            all_graphs_in_file = nx.read_graph6(temp)
            for graph in all_graphs_in_file:
                if isinstance(type(all_graphs_in_file), list):
                    for g2 in graph:
                        graphs.append(g2)
                else:
                    graphs.append(graph)
        if bool:
            draw_graphs(graphs, filename.decode("utf-8"))
    print(graphs)
    return graphs


def load_g6_leaf2(bool):
    """
    Loads and returns all graphs in all files as a single list
    :param bool:
    :return: list of every single individual graph from each file
    """
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


def count_leaves(graphs):
    count = 0
    graph_leaves = []
    for g in graphs:
        count += 1
        degree_count = [0] * 10
        for node in g.degree():
            degree_count[node[1]] = degree_count[node[1]] + 1
        graph_leaves.append((g, degree_count))

    print(graph_leaves)


def compare_trees_graphs(graphs_file_path, trees_file_path, index, num_nodes=None):
    """
    Compares the k-leaf power of all k-leaf trees of num_nodes nodes with all possible graphs of num_nodes nodes.
    Comparison is carried out using string comparison of generated g6 format byte-string codes in a list-wise fashion.
    Performance improvements are likely to occur through implementation of hashing for these values.

    :param graphs_file_path: file path to the file containing the graphs of num_nodes
    :param trees_file_path: file path to the file containing the trees of num_nodes and index leaves
    :param index: simultaneously the number of leaves in a tree and the k-leaf power to which to raise the tree
    :param num_nodes: optional number of nodes in the graphs
    :return: n/a
    """
    trees_in = nx.read_graph6(trees_file_path)
    trees = []
    graphs = []
    for tree in trees_in:
        trees.append(nx.to_graph6_bytes(tree, header=False))
    graphs_in = nx.read_graph6(graphs_file_path)
    for graph in graphs_in:
        graphs.append(nx.to_graph6_bytes(graph, header=False))
    print("Trees\tNum Trees: {}\n".format(len(trees)), trees, "\nGraphs\tNum Graphs: {}\n".format(len(graphs)), graphs)
    k_leaf_powers = set()
    for t in trees_in:
        temp = nx.to_numpy_matrix(t)
        temp = Logic.k_leaf_power(temp, index)
        temp = nx.Graph(temp)
        draw_graph(temp, "G")
        k_leaf_powers.add(nx.to_graph6_bytes(temp, header=False))
    print('{}-leaf powers\n'.format(index), k_leaf_powers)
    for i in k_leaf_powers:
        print(i)


main()
