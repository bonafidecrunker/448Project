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

    def create_graph(self):
        out = []
        for g in self.G:
            source = []
            destination = []
            weight = []
            edge_list = g.edges()
            for e in edge_list:
                print(e[0], end=" ")
                print(e[1])

                source.append(e[0])
                destination.append(e[1])
                weight.append(1)
            
            temp_graph = Graph(source, destination, weight)
            out.append(temp_graph)
        return out


test = G6_in('./graph_files/std_geng4_c.g6')
test.create_graph()
