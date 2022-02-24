class Node:
    def __init__(self, label):
        self.label = label
        self.edges = []

    def __str__(self):
        return str(self.label)

    def get_edges(self):
        return self.edges

    def add_edge(self, node):
        self.edges.append(node)
