import networkx as nx
import itertools


def get_byte_strings(filename, graph_set):
    temp_graph_list = nx.read_graph6(filename)
    with open(filename) as file:
        counter = 0
        lines = file.readlines()
        for line in lines:
            graph_set.append((line.strip(), temp_graph_list[counter]))
            counter += 1


def graph_contains(test_string, min_forbidden):
    # if min_forbidden is empty, there can be no extant subgraph in it
    if not min_forbidden:
        return False

    temp_graph = nx.from_graph6_bytes(test_string.encode("utf-8"))
    for min_f in min_forbidden:
        temp_forbidden_graph = nx.from_graph6_bytes(min_f.encode("utf-8"))
        temp_forbidden_size = len(temp_forbidden_graph.nodes())
        combinations = list(itertools.combinations(temp_graph.nodes(), temp_forbidden_size))
        for c in combinations:
            g = temp_graph.subgraph(c).copy()
            if nx.is_isomorphic(temp_forbidden_graph, g):
                return True
    return False


def generate_minimal_forbiddens(k_leaf_power):
    all_forbiddens = []
    min_forbidden_dict = {}

    for graph_size in range(3, k_leaf_power + 1):
        # load all forbidden graphs from g6 into a Python list
        file_path = f'all_forbidden_graphs/{graph_size}_leaf_forbiddens.g6'
        get_byte_strings(file_path, all_forbiddens)

        min_forbidden = set()

        for f_graph in all_forbiddens:
            if not graph_contains(f_graph, min_forbidden):
                min_forbidden.add(f_graph)

        min_forbidden_dict[graph_size] = [nx.from_graph6_bytes(n.encode('utf-8')) for n in min_forbidden]

    return min_forbidden_dict


def write_minimal_forbiddens_to_file(min_forbidden_dict):
    for k, graphs in min_forbidden_dict.items():
        file_path = f'minimal_forbiddens/{k}_leaf_minimal_forbidden_induced_subgraphs.g6'
        with open(file_path, 'ab') as file:
            for graph in graphs:
                file.write(nx.to_graph6_bytes(graph, header=False))


def main():
    k_leaf_power = 6
    min_forbidden_dict = generate_minimal_forbiddens(k_leaf_power)
    write_minimal_forbiddens_to_file(min_forbidden_dict)
