import itertools


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
                    if g.has_edge(p[0], p[2]) or g.has_edge(p[1], p[3]):
                        # print("P4 does NOT exist")
                        break
                    else:
                        # print("P4 does exist")
                        return True
        return False


