import itertools
import networkx as nx
import numpy as np


def reduce_to_ones(adj_matrix):
    temp = np.where(adj_matrix >= 1, 1, 0)
    for i in range(len(temp)):
        temp[i][i] = 0
    return temp


class Logic:
    def contains_forbidden_subgraph(self, g, forbiddens):
        """
        Checks to see if a graph contains a known forbidden subgraph.

        :param g: networkx graph
        :param forbiddens: a list of forbidden graphs
        :return: Boolean value depending on whether the graph contains forbidden subgraphs or not
        """
        if self.has_p4(g):
            return True
        # for f in forbiddens:
        #     return True
        return False

    @staticmethod
    def has_p4(g):
        """
        Generates all possible edge list permutations and checks if there exists a 4-path with no other connections
        back on itself i.e., only a 4 path, no cycles allowed.

        :param g: networkx graph
        :return: Boolean value depending on whether the graph has a p4 or not
        """
        combinations = list(itertools.combinations(g, 4))
        for c in combinations:
            permutations = list(itertools.permutations(c))
            for p in permutations:
                if g.has_edge(p[0], p[1]) and g.has_edge(p[1], p[2]) and g.has_edge(p[2], p[3]):
                    if g.has_edge(p[0], p[2]) or g.has_edge(p[0], p[3]) or g.has_edge(p[1], p[3]):
                        # print("P4 does NOT exist")
                        break
                    else:
                        # print("P4 does exist")
                        return True
        return False

    @staticmethod
    def has_p4_improved(g):
        combinations = list(itertools.combinations(g, 4))
        v0, v1, v2, v3 = 0, 0, 0, 0
        for c in combinations:
            #for p in permutations:
            if g.has_edge(c[0], c[1]):
                v0, v1 = v0 + 1, v1 + 1
            if g.has_edge(c[1], c[2]):
                v1, v2 = v1 + 1, v2 + 1
            if g.has_edge(c[2], c[3]):
                v2, v3 = v2 + 1, v3 + 1
            if g.has_edge(c[0], c[3]):
                v0, v3 = v0 + 1, v3 + 1
            if g.has_edge(c[1], c[3]):
                v1, v3 = v1 + 1, v3 + 1
            if g.has_edge(c[0], c[2]):
                v0, v2 = v0 + 1, v2 + 1
                #if g.has_edge(p[0], p[1]) and g.has_edge(p[1], p[2]) and g.has_edge(p[2], p[3]):
                #    if g.has_edge(p[0], p[2]) or g.has_edge(p[0], p[3]) or g.has_edge(p[1], p[3]):
                        # print("P4 does NOT exist")
                #        break
                #    else:
                        # print("P4 does exist")
                #        return True
        sorted_list = np.sort([v0, v1, v2, v3])
        if sorted_list[0] == sorted_list[1] == 1 and sorted_list[2] == sorted_list[3] == 2:
            return True
        return False

    @staticmethod
    def k_leaf_power(adj_matrix, k):
        """
        Generates the k-leaf power for a given graph. See https://en.wikipedia.org/wiki/Leaf_power for explanations on
        k-leaf power.
        
        :param adj_matrix: the graph in adjacency matrix form
        :param k: the index to which to raise the graph 
        :return: the adjacency matrix representation of the k-leaf power of the graph 
        """
        gk_minus_one = np.zeros_like(adj_matrix)
        for i in range(0, k): # changed from range(1,k)
            if i == 0: # changed from i == 1
                gk_minus_one = adj_matrix
            else:
                gk_minus_one = np.linalg.matrix_power(adj_matrix, i + 1) + np.array(gk_minus_one) # changed from (adj_matrix, i)
        # gk = nx.from_numpy_matrix(np.array(gk_minus_one))
        gk_minus_one = reduce_to_ones(gk_minus_one)
        return gk_minus_one

    @staticmethod
    def k_leaf_recursion(adj_matrix, k):
        temp_matrix = adj_matrix
        print(temp_matrix)
        if k == 1:
            return temp_matrix
        return Logic.k_leaf_recursion(np.linalg.matrix_power(temp_matrix, k) + adj_matrix, k - 1)

