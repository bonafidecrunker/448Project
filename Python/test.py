from Graph import *
from G6_in import *


def main():
    testFile = 'graph_files/std_geng4_c.g6'
    g = G6_in(testFile)
    g.create_graph()
    g.draw_graphs()


main()
exit(0)
