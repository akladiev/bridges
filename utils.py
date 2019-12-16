import networkx as nx
from collections import defaultdict
from matplotlib import pyplot as plt
from pathlib import Path
from graph import read_from_file
import numpy as np
import time
import json


def to_edge(fr, to):
    return (fr, to) if fr < to else (to, fr)


def average_exec_time(retry_count):
    def time_measure(func):
        def wrapper(*args, **kwargs):
            times = []
            for i in range(retry_count):
                start_time = time.time()
                func(*args, **kwargs)
                time_elapsed = time.time() - start_time
                times.append(time_elapsed)
            return sum(times) / len(times)
        return wrapper
    return time_measure


def nested_dict():
    return defaultdict(nested_dict)


def show_graph(graph):
    if isinstance(graph, str):
        adj_list = read_from_file(graph)
        graph = nx.Graph(adj_list)
    nx.draw_networkx(graph)
    plt.show()


def save_graph_image(graph, graph_path):
    if isinstance(graph, str):
        adj_list = read_from_file(graph)
        graph = nx.Graph(adj_list)
    plt.figure(figsize=(20, 20))
    nx.draw_networkx(graph)
    plt.savefig(Path(graph_path).with_suffix(".png"), format="PNG")


def positive_number(x):
    x = float(x)
    assert(x > 0)
    return x


def load_benchmark_data(data_filepath):
    with open(data_filepath, "r") as file:
        data = json.load(file)
    # Rearrange data for plotting convenience
    plot_data = {}
    for density, nodes_data in data.items():
        plot_data[density] = {}
        for node_count, algo_data in nodes_data.items():
            for algo, time in algo_data.items():
                point = (node_count, time)
                if algo in plot_data[density]:
                    plot_data[density][algo].append(point)
                else:
                    plot_data[density][algo] = [point]
    return plot_data


def plot_benchmark_data(data_filepath):
    data = load_benchmark_data(Path(data_filepath))
    plt.figure(figsize=(15, 40))
    subplots_number = len(data)

    for i, (density, algo_data) in enumerate(data.items()):
        ax = plt.subplot(subplots_number, 1, i + 1)
        ax.set_title(f"Density: {density}")
        ax.set_xlabel("nodes_count")
        ax.set_ylabel("time (sec)")

        for algo, points in algo_data.items():
            x = np.asarray([p[0] for p in points])
            y = np.asarray([p[1] for p in points])
            ax.plot(x, y, label=algo)
            plt.legend()
    plt.show()
