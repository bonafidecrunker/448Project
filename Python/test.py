from g6In import *
from Logic import *


def main():
    test_file = 'graph_files/std_geng5_c.g6'
    g = g6In(test_file)
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
    # draw_graphs(nx_graphs, 'All connected graphs of 5 nodes')
    draw_graphs(non_p4_graphs, "Connected P4-free graphs of 5 nodes")
    draw_graphs(forbidden_graphs, "Connected forbidden graphs of 5 nodes")


def draw_graphs(g, title):
    total = len(g)
    cols = 3
    rows = total // cols
    rows += total % cols
    position = range(1, total + 1)

    fig = plt.figure(figsize=(10, 10))
    plt.title(title, pad=35, fontsize=16)
    plt.axis('off')
    for k in range(total):
        ax = fig.add_subplot(rows, cols, position[k])
        ax.set_title('Graph {}'.format(k + 1))
        nx.draw(g[k], with_labels='True', font_color='#bab0ac', node_color='#4e79a7')
    plt.tight_layout()
    plt.show()


main()
exit(0)
