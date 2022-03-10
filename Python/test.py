from G6_in import *
from Logic import *


def main():
    test_file = 'graph_files/std_geng5_c.g6'
    g = G6_in(test_file)
    nx_graphs = g.create_graphs()
    counter = 1
    forbidden_graphs, non_p4_graphs = [], []
    for graph in nx_graphs:
        print("Graph # {}".format(counter))
        counter += 1
        if not Logic.has_p4(graph):
            non_p4_graphs.append(graph)
        else:
            forbidden_graphs.append(graph)
    for graph in nx_graphs:
        print(graph.edges)
    draw_graphs(non_p4_graphs, "P4-free graphs")


def draw_graphs(G, title):
    total = len(G)
    cols = 3
    rows = total // cols
    rows += total % cols
    position = range(1, total + 1)

    fig = plt.figure(figsize=(10, 10))
    plt.title(title)
    plt.axis('off')
    for k in range(total):
        ax = fig.add_subplot(rows, cols, position[k])
        nx.draw(G[k])
    plt.tight_layout()
    plt.show()


main()
exit(0)
