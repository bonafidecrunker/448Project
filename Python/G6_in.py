import matplotlib.pyplot as plt
from Graph import *


class G6_in():

    def __init__(self, file) -> None:
        self.G = nx.read_graph6(file)
        self._index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self.G):
            raise StopIteration
        else:
            temp = self.G[self._index]
            self._index += 1
            return temp

    def read_file(self, file):
        self.G = nx.read_graph6(file)

    def print_edges(self):
        for graph in self.G:
            print(graph.edges())
    
    def draw_graphs(self):
        n = int(len(self.G) / 2)

        fig = plt.figure(figsize=(10, 10))
        for i in range(len(self.G)):
            plt.subplot(n, 3, i + 1)
            fig.subplots_adjust(wspace=0.05, hspace=0.5)
            nx.draw(self.G[i])

        plt.tight_layout()
        plt.show()

    def draw_graphs2(self):
        total = len(self.G)
        cols = 3
        rows = total // cols
        rows += total % cols
        position = range(1, total + 1)

        fig = plt.figure(figsize=(10, 10))
        for k in range(total):
            ax = fig.add_subplot(rows, cols, position[k])
            nx.draw(self.G[k])
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


