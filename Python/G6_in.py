import networkx as nx
import matplotlib.pyplot as plt



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
            plt.subplot(n,n,i+1)
            nx.draw(self.G[i])

        plt.tight_layout()
        plt.show()
    


test = G6_in('./graph_files/std_geng4_c.g6')
test.draw_graphs()
