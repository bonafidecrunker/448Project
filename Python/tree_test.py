from TreeIn import *
from test import draw_graphs
import networkx as nx
import matplotlib as plt


def main():
    tree = 'tree_files/tree4.2.txt'
    g = TreeIn(tree)
    graphs = g.get_graphs()
    for a in graphs:
        print(a)
    exit(0)


main()
