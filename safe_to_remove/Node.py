from operator import index


class Node:
    """
    Currently unnecessary. Probably safe to remove.
    """
    def __init__(self, label):
        self.label = label
        self.edges = []

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.label == other.label
        try:
            return self.label == index(other)
        except TypeError:
            return NotImplemented

    def __hash__(self):
        return hash(self.label)

    def get_edges(self):
        return self.edges

    def add_edge(self, node):
        self.edges.append(node)
