from TreeIn import *
import os
from Graph_Draw import *


def main(file):
    g = TreeIn(file)
    graphs = g.get_graphs()
    draw_graphs(graphs, "Graphs")
    exit(0)


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

    #print(graphs)
    draw_graphs(graphs, "asd")
    exit(0)

    print(graphs)
    #draw_graphs(graphs,"asd")


main('tree_files/tree6.3.txt')
main('tree_files/tree6.4.txt')
