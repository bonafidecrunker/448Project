import networkx as nx


class TreeIn:
    def __init__(self, file_path):
        """
        Holds networkx graphs of trees generated from tree files at https://users.cecs.anu.edu.au/~bdm/data/trees.html

        :param file_path: relative or absolute path to the file containing the trees
        """
        self.graphs = []
        self.file = file_path
        self._create_graphs()
        # with open(str(file_path), 'r') as file:
        #     for line in file:
        #         edges = line.split('  ')
        #         print(edges)
        #         graph = nx.Graph()
        #         for pair in edges:
        #             graph.add_edge(pair[0], pair[1])
        #     self.graphs.append(graph)

    # def __iter__(self):
    #     return self

    def get_graphs(self):
        return self.graphs

    def _create_graphs(self):

        f = open(self.file, "r")
        for line in f:
            edges = line.split('  ')
            print(edges)
            graph = nx.Graph()
            for pair in edges:
                graph.add_edge(pair[0], pair[1])
            self.graphs.append(graph)


