from pprint import pformat
import yaml


class Graph:
    def __init__(self, adj_list):
        self.nodes = adj_list

    def __len__(self):
        return len(self.nodes)

    def __str__(self):
        return pformat(self.nodes)

    def get_adjacent(self, node):
        adj = self.nodes[node]
        return set(adj)


def read_from_file(file_path):
    with open(file_path, "r") as file:
        graph = yaml.load(file, Loader=yaml.Loader)
    return graph


def find_connected_components(graph, dfs_visitor=None):
    components = []
    non_visited_roots = set(graph.nodes)
    while non_visited_roots:
        root = non_visited_roots.pop()
        nodes = dfs(graph, root, dfs_visitor)
        components.append(nodes)
        non_visited_roots -= nodes
    return components


def dfs(graph, root, visitor=None):
    stack, visited = [root], set()
    while stack:
        root = stack[-1]
        adjacent = graph.get_adjacent(root)
        if root not in visited:
            visited.add(root)
            stack.extend(adjacent - visited)
            if visitor:
                visitor.on_visit(root, adjacent, visited)
        else:
            stack.pop()
            if visitor:
                visitor.on_leave(root, adjacent)
    return visited


class Edge(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(Edge, (x, y) if x < y else (y, x))
