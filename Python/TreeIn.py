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

    def __iter__(self):
        return self

    def get_graphs(self):
        return self.graphs

    def _create_graphs(self):
        f = open(self.file, "r")
        for line in f:
            edges = line.split('  ')
            graph = nx.Graph()
            for pair in edges:
                t = pair.split()
                graph.add_edge(t[0], t[1])
            self.graphs.append(graph)


