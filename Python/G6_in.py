import itertools
from msilib.schema import SelfReg
import networkx as nx
import matplotlib.pyplot as plt
from Graph import *


class G6_in():

    def __init__(self, file) -> None:
        self.G = nx.read_graph6(file) 

    def read_file(self, file):
        self.G = nx.read_graph6(file)

    def print_edges(self):
        for graph in self.G:
            print(graph.edges())
    
    def draw_graphs(self):
        n = int(len(self.G) / 2)
        for i in range(len(self.G)):
            plt.subplot(n, n, i + 1)
            nx.draw(self.G[i])

        plt.tight_layout()
        plt.show()

    def create_graphs(self):
        """
        Make the g6 graph into our native Graph class.
        :return: array of Graph objects
        """
        out = []
        for g in self.G:
            temp_graph = nx.Graph()
            temp_graph.add_edges_from(g.edges())
            out.append(temp_graph)
        return out


