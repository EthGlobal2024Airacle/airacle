from concurrent.futures import ThreadPoolExecutor
from random import sample

import networkx as nx

from graph_builder import GraphBuilder
from blockchain_data_fetcher import BlockchainDataFetcher
from community_detector import CommunityDetector
# from graph_visualizer import GraphVisualizer


class BlockchainAnalyzer:
    def __init__(self, initial_address: str, fetcher: BlockchainDataFetcher):
        self.initial_address = initial_address
        self.graph_builder = GraphBuilder()
        self.data_fetcher = fetcher

    def analyze(self, max_queries: int = 4):
        self.graph_builder.add_initial_node(self.initial_address)

        remaining_queries = max_queries
        while remaining_queries:
            non_queried_addresses = self.graph_builder.get_non_queried_addresses()
            if not non_queried_addresses:
                break

            addresses = self._select_addresses(non_queried_addresses)

            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(self._query_node, addresses))

            for address, result in zip(addresses, results):
                token_transfers, native_transfers, rich_addresses = result
                token_transfers.native_transfers = native_transfers
                self.graph_builder.update_graph(address, token_transfers, rich_addresses)

            remaining_queries -= 1

        self.graph_builder.remove_zero_address()

        # Detect communities and set them for each node
        communities = CommunityDetector.detect_communities(self.graph_builder.graph)
        CommunityDetector.set_node_communities(self.graph_builder.graph, communities)

    def _select_addresses(self, non_queried_addresses):
        addresses = sample(non_queried_addresses, min(5, len(non_queried_addresses)))
        roots = [node for node in non_queried_addresses if self.graph_builder.graph.in_degree[node] == 0]
        addresses += sample(roots, min(3, len(roots)))
        return list(set(addresses))

    def _query_node(self, address: str):
        token_transfers, token_addresses = self.data_fetcher.fetch_token_transfers(address)
        native_transfers, native_addresses = self.data_fetcher.fetch_native_transfers(address)
        return token_transfers, native_transfers, token_addresses + native_addresses

    # def visualize(self):
    #     graph = self.graph_builder.graph.copy()
    #     GraphVisualizer.apply_community_colors(graph)
    #     GraphVisualizer.adjust_labels(graph)
    #     GraphVisualizer.write_graph_to_file(graph, '~/tmp/transfers.dot')

    def get_community_subgraph(self) -> nx.MultiDiGraph:
        if self.initial_address not in self.graph_builder.graph:
            raise ValueError("Initial address not found in the graph. Make sure to run analyze() first.")

        initial_community = self.graph_builder.graph.nodes[self.initial_address]['community']

        # Get all nodes in the same community as the initial address
        community_nodes = [node for node, data in self.graph_builder.graph.nodes(data=True)
                           if data.get('community') == initial_community]

        # Create a subgraph with only the nodes in the community
        community_subgraph = self.graph_builder.graph.subgraph(community_nodes).copy()

        return community_subgraph
