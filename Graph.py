from Node import *
import pandas as pd
import numpy as np


class Graph:
    def __init__(self, graph=None):
        if graph is None:
            graph = []
        self.graph = graph

    def __str__(self):
        out = ''
        for n in self.graph:
            out += str(n) + ": " + str(self.graph[n]) + "\n"
        return out

    def add_node(self, char):
        node = Node(char)
        if node not in self.graph:
            self.graph.append(node)

    def add_edge(self, node1, node2):
        assert node1, node2 in self.graph
        self.graph[node1].append(node2)
        self.graph[node2].append(node1)

    def build_adjacency_matrix(self):
        n = len(self.graph)
        adj_mat = [[0 for x in range(n)] for y in range(n)]

        # grab the labels from the graph, add all the edges to the adjacency matrix
        labels = []
        for node in self.graph:
            labels.append(node.label)

        # loop through the graph and add all the edges to the adjacency matrix
        for node in self.graph:
            for edge in node.edges:
                adj_mat[node][edge] = 1

        df = pd.DataFrame(adj_mat, index=labels, columns=labels)
        print(df)
