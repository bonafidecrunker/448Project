from TreeIn import *
import os
from Graph_Draw import *


def main():
    #partition(graphs)
    graphs = load_g6_leaf(False)

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
            g = nx.read_graph6(temp)
            for graph in g:
                if isinstance(type(g), list):
                    for g2 in graph:
                        graphs.append(g2)
                else:
                    graphs.append(graph)
        print(graphs)
        if(bool):
            draw_graphs(graphs, filename.decode("utf-8"))
    return graphs
    
def partition(graphs):
    for g in graphs:
        n = len(g.nodes)
        d = nx.diameter(g)
        l = 0
        for node in g.degree():
            if node[1] == 1:
                l += 1
        filename = build_filename(n,d,l)
        with open("leaf_files/"+filename, "a+") as f:
            f.write(nx.to_graph6_bytes(g).decode("utf-8").replace(">>graph6<<",""))

def build_filename(n,d,l):
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
