from graph import *
from find_bridges import *
from pathlib import Path
import networkx as nx
import unittest
import yaml
import os


class GraphTest(unittest.TestCase):
    @property
    def data(self):
        raise NotImplementedError

    def setUp(self):
        self.test_data_dir = Path(os.path.dirname(__file__), "test_data", self.data)
        self.test_data = {}
        for data_file in self.test_data_dir.glob("*.yml"):
            with open(str(data_file), "r") as file:
                data = yaml.load(file, Loader=yaml.Loader)
                self.test_data.update(data)

    def run_test(test_func):
        def test_wrapper(self):
            for graph_file, expected in self.test_data.items():
                with self.subTest(graph=graph_file):
                    graph_path = self.test_data_dir / graph_file
                    adj_list = read_from_file(graph_path)
                    graph = Graph(adj_list)
                    test_func(self, graph, graph_file, expected)
        return test_wrapper


class GraphCreationTest(GraphTest):
    data = "simple"

    @GraphTest.run_test
    def test_nodes_count(self, graph, graph_file, expected):
        expected = expected["nodes"]
        actual = len(graph)
        msg = f"{graph_file} has correct number of nodes:\nExpected {expected}, actual: {actual}"
        self.assertEqual(actual, expected, msg)

    @GraphTest.run_test
    def test_adjacent(self, graph, graph_file, expected):
        adj_list = graph.nodes
        for node, adj_nodes in adj_list.items():
            for adj in adj_nodes:
                msg = f"{adj} adjacent to {node} in {graph_file} is in adjacency list {adj_list}"
                self.assertTrue(adj in adj_list, msg)
                msg = f"{adj} adjacent to {node} in {graph_file} has {node} in its adjacency list {adj_list}"
                self.assertTrue(node in adj_list[adj], msg)

    @GraphTest.run_test
    def test_components(self, graph, graph_file, expected):
        nx_graph = nx.Graph(graph.nodes)
        expected = list((nx.connected_components(nx_graph)))
        actual = find_connected_components(graph)
        msg = f"Components number is correct for {graph_file}:\nExpected: {len(expected)}, result: {len(actual)}"
        self.assertEqual(len(expected), len(actual), msg)
        msg = f"Components are found correctly in {graph_file}:\nExpected: {expected}, result: {actual}"
        self.assertTrue(all([component in actual for component in expected]), msg)


class BridgeTest(GraphTest):
    @property
    def data(self):
        raise NotImplementedError

    @property
    def ref_name(self):
        raise NotImplementedError

    def run_bridge_test(self, find_bridges_func, graph, graph_file, expected):
        result = find_bridges_func(graph)
        expected_bridges = expected[self.ref_name] if self.ref_name in expected else []
        msg = f"Correct bridges are found in {graph_file}:\nResult - expected: {result - set(expected_bridges)}"
        self.assertTrue(all([edge in expected_bridges for edge in result]), msg)
        msg = f"Correct bridges are found in {graph_file}:\nExpected - result: {set(expected_bridges) - result}"
        self.assertTrue(all([edge in result for edge in expected_bridges]), msg)


class OneBridgeTest(BridgeTest):
    data = "generated"
    ref_name = "bridges"

    @GraphTest.run_test
    def test_determined_one_bridge(self, graph, graph_file, expected):
        self.run_bridge_test(find_det_one_bridges, graph, graph_file, expected)

    @GraphTest.run_test
    def test_randomized_one_bridge(self, graph, graph_file, expected):
        self.run_bridge_test(find_rand_one_bridges, graph, graph_file, expected)


class TwoBridgesTest(BridgeTest):
    data = "two_bridges"
    ref_name = "two_bridges"

    @GraphTest.run_test
    def test_randomized_two_bridge(self, graph, graph_file, expected):
        self.run_bridge_test(find_rand_two_bridges, graph, graph_file, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
