import pandas as pd
import networkx as nx


class Graph:
    def __init__(self, src_nodes=None, dest_nodes=None, weights=None):
        self.src_nodes = src_nodes
        self.dest_nodes = dest_nodes
        self.weights = weights

    def __str__(self):
        return 'Source: {}\nDestination: {}\nWeight: {}'.format(self.src_nodes, self.dest_nodes, self.weights)

    def add_edge(self, node1, node2, weight):
        self.src_nodes.append(node1)
        self.dest_nodes.append(node2)
        self.weights.append(weight)

    def __adjacency_matrix(self):
        df = pd.DataFrame({'source': self.src_nodes,
                           'destination': self.dest_nodes,
                           'weight': self.weights})
        g = nx.from_pandas_edgelist(df, 'source', 'destination', edge_attr='weight')
        adj_mat = nx.adjacency_matrix(g)
        return adj_mat.todense()

    def print_adjacency_matrix(self):
        am = self.__adjacency_matrix()
        return pd.DataFrame(am, index=self.src_nodes, columns=self.src_nodes)


