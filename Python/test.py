from g6In import *
from Logic import *
import time
from Graph_Draw import *


def main():
    test_file = 'graph_files/std_geng5_c.g6'
    g = g6In(test_file)
    nx_graphs = g.create_graphs()
    counter = 1
    forbidden_graphs, non_p4_graphs = [], []
    t0 = time.time()
    for graph in nx_graphs:
        #print("Graph # {}".format(counter))
        counter += 1
        if not Logic.has_p4_improved(graph):
            non_p4_graphs.append(graph)
        else:
            forbidden_graphs.append(graph)
    t1 = time.time()
    #for graph in nx_graphs:
    #    print(graph.edges)
    # draw_graphs(nx_graphs, 'All connected graphs of 5 nodes')
    draw_graphs(non_p4_graphs, "Connected P4-free graphs of 6 nodes")
    #draw_graphs(forbidden_graphs, "Connected forbidden graphs of 6 nodes")
    print("Accepted Graphs")
    print(len(non_p4_graphs), end="\n\n")
    print("Forbidden Graphs")
    print(len(forbidden_graphs))
    print("Total Completion Time {}".format(t1-t0))
    

main()
exit(0)
