from utils import average_exec_time, nested_dict
from find_bridges import *
from sorting import *
from generate_graph import generate
import networkx as nx
import itertools
import json


def dump_results(data, filepath="bench_data.json"):
    with open(filepath, "w") as file:
        json.dump(data, file)


if __name__ == '__main__':
    sort_funcs = {"sorted": sorted, "bucket": bucket_sort, "radix": radix_sort}

    step = 500
    densities = [0.01]
    node_counts = list(range(5000, 10000 + step, step))
    sparse = sorted(list(itertools.product(densities, node_counts)))

    step = 200
    densities = [0.9, 0.95, 0.97, 0.99, 0.999]
    node_counts = list(range(100, 1000 + step, step))
    dense = sorted(list(itertools.product(densities, node_counts)))

    runs_count = 1
    benchmark_data = nested_dict()
    graph_gen_params = sparse + dense

    for density, nodes_count in graph_gen_params:
        print(f"Generating configuration with {nodes_count} nodes, density: {density}")
        edges_count = int(density * ((nodes_count * nodes_count) / 2))
        print(f"Expected average edges count: {edges_count}")

        graph = generate(nodes_count=nodes_count, prob=density)

        actual_edges = nx.Graph(graph.nodes).number_of_edges()
        print(f"Actual edges: {actual_edges}")

        print(f"Running benchmark")

        det_one_time = average_exec_time(1)(find_det_one_bridges)(graph)
        print(f"Determined one bridge: {det_one_time} sec")
        benchmark_data[density][nodes_count]["det_1"] = det_one_time
        dump_results(benchmark_data)

        rand_one_time = average_exec_time(runs_count)(find_rand_one_bridges)(graph)
        print(f"Randomized one bridge: {rand_one_time} sec")
        benchmark_data[density][nodes_count]["rand_1"] = rand_one_time
        dump_results(benchmark_data)

        for sort_func_name, sort_func in sort_funcs.items():
            rand_two_time = average_exec_time(runs_count)(find_rand_two_bridges)(graph, sort_func)
            print(f"Randomized two bridges ({sort_func_name} sort): {rand_two_time} sec")
            benchmark_data[density][nodes_count][f"rand_2_{sort_func_name}"] = rand_two_time
            dump_results(benchmark_data)

        print()

    print(json.dumps(benchmark_data))
