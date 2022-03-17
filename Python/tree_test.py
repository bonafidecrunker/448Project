from TreeIn import *
import os
from Graph_Draw import *


def main():
    #partition(graphs)
    graphs, names = load_g6_leaf2(False)
    draw_partitioned_graphs(graphs, names)


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
    directory = os.fsencode('tree_files_subset')
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
        with open("leaf_files/"+filename, "a+") as f:
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


main()
exit(0)
