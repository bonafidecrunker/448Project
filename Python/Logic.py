import itertools


class Logic:
    def contains_forbidden_subgraph(self, g, forbiddens):
        if self.has_p4(g):
            return True
        for f in forbiddens:
            return True
        return False

    @staticmethod
    def has_p4(g):
        combinations = list(itertools.combinations(g, 4))
        for c in combinations:
            # print(c)
            # print()
            perm = list(itertools.permutations(c))
            for p in perm:
                # print(p)
                if g.has_edge(p[0], p[1]) and g.has_edge(p[1], p[2]) and g.has_edge(p[2], p[3]):
                    if g.has_edge(p[0], p[2]) or g.has_edge(p[1], p[3]):
                        print("P4 does NOT exist")
                        break
                    else:
                        print("P4 does exist")
                        return True
        return False
