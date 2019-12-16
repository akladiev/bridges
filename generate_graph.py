from utils import *
from graph import Graph
from pathlib import Path
import networkx as nx
import itertools
import yaml
import random
import numpy as np


def generate(nodes_count, prob, seed=None):
    random.seed(seed)
    nodes = np.array(range(1, nodes_count+1))
    adj_list = {i: set() for i in nodes}
    for i in adj_list:
        for j in range(i + 1, len(nodes)):
            if random.random() < prob:
                adj_list[i].add(j)
                adj_list[j].add(i)
    # Convert sets to lists for proper dumping to yml
    adj_list = {i: list(adj_list[i]) for i in adj_list}
    return Graph(adj_list)


if __name__ == "__main__":
    collect_refs = False
    save_graph_as_image = False
    save_folder = "sparse_dense"

    densities = [0.01]
    node_counts = [10000]
    graph_gen_params = sorted(list(itertools.product(node_counts, densities)))

    for nodes_count, density in graph_gen_params:
        print(f"Generating configuration with {nodes_count} nodes, density: {density}")
        edges_count = int(density * ((nodes_count * nodes_count) / 2))
        print(f"Expected average edges count: {edges_count}")

        graph, gen_time = generate(nodes_count=nodes_count, prob=density)
        print(f"Time elapsed: {gen_time}")

        nx_graph = nx.Graph(graph.nodes)
        actual_edges = nx_graph.number_of_edges()
        graph_name = f"{density}_density_{nodes_count}_nodes_{actual_edges}_edges.graph"
        graph_desc = {graph_name: {"nodes": nodes_count, "edges": actual_edges}}

        if collect_refs:
            bridges = list(nx.bridges(nx_graph))
            graph_desc[graph_name]["bridges"] = bridges

        print(f"Generated: {graph_desc}\n")

        save_path = Path("tests") / "test_data" / save_folder
        save_path.mkdir(exist_ok=True)
        path = save_path / graph_name

        with open(path.with_suffix(".graph"), "w") as file:
            yaml.dump(graph.nodes, file, default_flow_style=False)

        with open(path.with_suffix(".yml"), "w") as file:
            yaml.dump(graph_desc, file, default_flow_style=False)

        if save_graph_as_image:
            save_graph_image(nx_graph, path.with_suffix(".png"))
