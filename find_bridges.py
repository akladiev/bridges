from graph import find_connected_components, Edge
import random
import sys


class DeterminedBridgeVisitor:
    def __init__(self):
        self.visit_time, self.parents, self.earliest_node_visit_time = {}, {}, {}
        self.time = 0

    def on_visit(self, root, adjacent, visited):
        self.time += 1
        self.visit_time[root] = self.earliest_node_visit_time[root] = self.time
        self.parents.update({node: root for node in adjacent - visited})
        pass

    def on_leave(self, root, adjacent):
        parent = self.parents.get(root, None)
        for node in adjacent - {parent}:
            self.earliest_node_visit_time[root] = min(
                self.visit_time[node], self.earliest_node_visit_time[node], self.earliest_node_visit_time[root]
            )
        if parent:
            self.earliest_node_visit_time[parent] = min(
                self.earliest_node_visit_time[root], self.earliest_node_visit_time[parent]
            )


class RandomizedBridgeVisitor:
    def __init__(self, graph):
        self.marked_edges, self.parents = {}, {}
        for node in graph.nodes:
            for adj in graph.get_adjacent(node):
                self.marked_edges[Edge(node, adj)] = random.randint(0, sys.maxsize)

    def on_visit(self, root, adjacent, visited):
        self.parents.update({node: root for node in adjacent - visited})

    def on_leave(self, root, adjacent):
        parent = self.parents.get(root, None)
        if not parent:  # All edges were processed
            return
        marks_sum = 0
        for adj in adjacent - {parent}:
            marks_sum = marks_sum ^ self.marked_edges[Edge(root, adj)]
        self.marked_edges[Edge(root, parent)] = marks_sum


def find_det_one_bridges(graph):
    collector = DeterminedBridgeVisitor()
    bridges = set()
    components = find_connected_components(graph, collector)
    for component in components:
        for node in component:
            parent = collector.parents.get(node, None)
            adjacent = graph.get_adjacent(node)
            for adj in adjacent - {parent}:
                if collector.earliest_node_visit_time[adj] > collector.visit_time[node]:
                    bridges.add(Edge(node, adj))
    return bridges


def find_rand_one_bridges(graph):
    collector = RandomizedBridgeVisitor(graph)
    find_connected_components(graph, collector)
    bridges = set(edge for edge in collector.marked_edges if collector.marked_edges[edge] == 0)
    return bridges


def find_rand_two_bridges(graph, sort_func=sorted):
    collector = RandomizedBridgeVisitor(graph)
    find_connected_components(graph, collector)
    non_bridge_edges = {k: v for k, v in collector.marked_edges.items() if v != 0}
    # Sort edges in ascending order by edge values
    sorted_edges = sort_func(non_bridge_edges.items(), key=lambda x: x[1])
    if not sorted_edges:
        return set()
    first_edge, current_value = sorted_edges[0]
    bridges = [{first_edge}]
    for i in range(1, len(sorted_edges)):
        edge, value = sorted_edges[i]
        if collector.marked_edges[edge] == current_value:
            bridges[-1].add(edge)
        else:
            bridges.append({edge})
            current_value = value
    bridges = {tuple(sorted(edges_set)) for edges_set in bridges if len(edges_set) > 1}
    return bridges
