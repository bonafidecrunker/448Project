import numpy as np
import pandas as pd


def matrix_power(matrix, index):
    assert type(index) == int
    return np.linalg.matrix_power(matrix, index)


def build_adjacency_matrix(g):
    graph = g.graph
    n = len(graph)
    adj_mat = [[0 for x in range(n)] for y in range(n)]

    # grab the labels from the graph and create a labels array for pretty formatting with pandas later
    labels = []
    for n in graph:
        labels.append(n.label)

    # loop through the graph and add all the edges to an adjacency matrix
    for node in graph:
        for edge in node.edges:
            adj_mat[node][edge] = 1

    df = pd.DataFrame(adj_mat, index=labels, columns=labels)
    print(df)




