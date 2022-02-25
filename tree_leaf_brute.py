import numpy as np
import networkx as nx


def matrix_power(matrix, index):
    assert type(index) == int
    return np.linalg.matrix_power(matrix, index)


def adjacency_matrix(dataframe):
    g = nx.from_pandas_adjacency(dataframe)





