from Graph import *


def main():
    source = ['a', 'b', 'c', 'd', 'e']
    destination = ['b', 'c', 'd', 'e', 'a']
    weights = [1, 1, 1, 1, 1]
    g = Graph(source, destination, weights)
    print(g.print_adjacency_matrix())


main()
exit(0)
