from Node import *
from collections import deque


def add_edge(src, dest):
    src.edges.append(dest)
    dest.edges.append(src)


class Graph:
    """
    Does not currently support addition of single nodes or disconnected nodes. Supports multi-edges. Consider changing
    class variables to be an edge list of tuples rather than it's current form. Would likely require refactoring of
    each other method.
    """
    def __init__(self, src_nodes=None, dest_nodes=None, weights=None):
        """
        Three argument constructor accepting three ordered lists of source nodes, destination nodes, and their weights.
        :param src_nodes: Ordered list of source nodes
        :param dest_nodes: Ordered list of destination nodes
        :param weights: Ordered list of weights
        """
        assert len(src_nodes) == len(dest_nodes) == len(weights)
        self.src_nodes = src_nodes
        self.dest_nodes = dest_nodes
        self.weights = weights

    def __str__(self):
        """
        :return: String representation of the source nodes, destination nodes, and their respective weights.
        """
        return 'Source: {}\nDestination: {}\nWeight: {}'.format(self.src_nodes, self.dest_nodes, self.weights)

    def add_edge(self, src, dest, weight):
        """
        Accepts new edges from source to destination with given weight. Currently, these nodes do not have to exist in
        the graph.
        :param src: source node/vertex
        :param dest: destination node/vertex
        :param weight: edge weight between the source and destination
        :return: n/a
        """
        self.src_nodes.append(src)
        self.dest_nodes.append(dest)
        self.weights.append(weight)

    def __adjacency_matrix(self):
        """
        Private method that builds an adjacency matrix from the list of source and destination nodes using the
        adjacency_matrix() method from networkx.
        :return: 2D matrix form of the adjacency matrix
        """
        df = pd.DataFrame({'source': self.src_nodes,
                           'destination': self.dest_nodes,
                           'weight': self.weights})
        g = nx.from_pandas_edgelist(df, 'source', 'destination', edge_attr='weight')
        adj_mat = nx.adjacency_matrix(g)
        return adj_mat.todense()

    def print_adjacency_matrix(self):
        """
        Pretty formatting for the adjacency matrix representation of the graph.
        :return: Formatted dataframe containing the adjacency matrix and labels for printing.
        """
        am = self.__adjacency_matrix()
        return pd.DataFrame(am, index=self.src_nodes, columns=self.src_nodes)
    # def __init__(self, nodes=None):
    #     if nodes is None:
    #         nodes = []
    #     self.nodes = nodes
    #
    # def add_node(self, label):
    #     new_node = Node(label)
    #     self.nodes.append(new_node)
    #
    # def bfs(self):
    #     if not self.nodes:
    #         return []
    #     start = self.nodes[0]
    #     visited, queue, result = {start}, deque([start]), []
    #     while queue:
    #         node = queue.popleft()
    #         result.append(node)
    #         for node in node.edges:
    #             if node not in visited:
    #                 queue.append(node)
    #                 visited.add(node)
    #     return result


