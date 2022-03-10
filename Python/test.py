from Graph import *
from G6_in import *
from Logic import *


def main():
    test_file = 'graph_files/std_geng4_c.g6'
    g = G6_in(test_file)
    nx_graphs = g.create_graphs()
    counter = 1
    temp_graphs = []
    for graph in nx_graphs:
        print("Graph # {}".format(counter))
        counter += 1
        if not Logic.has_p4(graph):
            temp_graphs.append(graph)

    nx_graphs = temp_graphs
    for graph in nx_graphs:
        print(graph.edges)


    # g.draw_graphs()


main()
exit(0)
