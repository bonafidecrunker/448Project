import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(g, title):
    total = len(g)
    cols = 3
    rows = total // cols
    rows += total % cols
    # position = range(1, total + 1)
    fig = plt.figure(figsize=(10, 10))
    plt.title(title, pad=35, fontsize=16)
    plt.axis('off')
    nx.draw(g, with_labels='True', font_color='#bab0ac', node_color='#4e79a7')
    plt.tight_layout()
    plt.show()


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