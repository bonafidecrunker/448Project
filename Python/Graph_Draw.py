import matplotlib.pyplot as plt
import networkx as nx
import random


def draw_graph(g, title=None, isTree=False):
    total = len(g)
    cols = 3
    rows = total // cols
    rows += total % cols  
    fig = plt.figure(figsize=(10, 10))
    plt.title(title, pad=35, fontsize=16)
    plt.axis('off')
    if isTree:
        position = hierarchy_pos(g)
        nx.draw(g, pos=position, with_labels='True', font_color='#bab0ac', node_color='#4e79a7')
    else:
        nx.draw_shell(g, with_labels='True', font_color='#bab0ac', node_color='#4e79a7')
    plt.tight_layout()
    plt.show()


def draw_graphs(g, title=None, subtitles=None):
    total = len(g)
    cols = 3
    rows = total // cols
    rows += total % cols
    position = range(1, total + 1)
    fig = plt.figure(figsize=(10, 12))
    plt.title(title, pad=35, fontsize=16)
    plt.axis('off')
    for k in range(total):
        ax = fig.add_subplot(rows, cols, position[k])
        ax.set_title(subtitles[k] if subtitles is not None else f'G{k + 1}')
        nx.draw_networkx(g[k], with_labels='True', font_color='#bab0ac', node_color='#4e79a7')
    plt.tight_layout()
    plt.show()


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    """
    Reference: https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209
    """
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
