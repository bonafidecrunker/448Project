import tree_leaf_brute
from Graph import *
from Node import *
from tree_leaf_brute import *
import numpy as np


def main():
    g = Graph()

    for i in range(5):
        new_node = Node(chr(ord('a') + i))
        g.add_node(new_node)

    # g.build_adjacency_matrix()
    labels = ['a', 'b', 'c']
    matrix = [[0, 1, 0],
              [1, 0, 1],
              [0, 1, 0]]
    sq = tree_leaf_brute.matrix_power(matrix, 2)
    df = pd.DataFrame(sq, index=labels, columns=labels)
    print(df)


main()
exit(0)
