import math
from collections import defaultdict
from datetime import datetime
import networkx as nx
from itertools import combinations
from typing import Dict, Tuple

from .blockchain_analyzer import BlockchainAnalyzer
from .blockchain_data_fetcher import BlockchainDataFetcher


class Investigator:
    def __init__(self, community: nx.MultiDiGraph, fetcher: BlockchainDataFetcher):
        super().__init__()
        self.community = community
        self.fetcher = fetcher

    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> datetime:
        timestamp_str = timestamp_str.replace('Z', '+00:00')
        return datetime.fromisoformat(timestamp_str)

    def enrich_community(self):
        nodes = [node for node in self.community.nodes if self.community.nodes[node].get('is_contract') is False]
        for node, transactions, in self.fetcher.fetch_transaction_history(nodes).items():
            if not transactions:
                continue
            start_time = transactions[0]['timestamp']
            end_time = transactions[-1]['timestamp']
            self.community.nodes[node]['start_timestamp'] = self._parse_timestamp(start_time)
            self.community.nodes[node]['end_timestamp'] = self._parse_timestamp(end_time)
            self.community.add_edges_from((node, tx['to']['hash']) for tx in transactions if tx.get('to'))

        # Compute Jaccard similarity for all pairs
        jaccard_similarities = self.compute_jaccard_similarities()
        raw_similarities = defaultdict(dict)
        for (node1, node2), similarity in jaccard_similarities.items():
            raw_similarities[node1][node2] = similarity

        nx.set_node_attributes(self.community, raw_similarities, 'jaccard_similarity')

    def compute_jaccard_similarities(self) -> Dict[Tuple[str, str], float]:
        jaccard_similarities = {}
        nodes = list(self.community.nodes())

        for node1, node2 in combinations(nodes, 2):
            neighbors1 = set(self.community.neighbors(node1))
            neighbors2 = set(self.community.neighbors(node2))

            # Compute weighted Jaccard similarity
            intersection_weight = sum(self.get_edge_weight(node1, n) + self.get_edge_weight(node2, n)
                                      for n in neighbors1.intersection(neighbors2))
            union_weight = sum(self.get_edge_weight(node1, n) for n in neighbors1) + \
                           sum(self.get_edge_weight(node2, n) for n in neighbors2)

            if union_weight > 0:
                jaccard_similarity = intersection_weight / union_weight
            else:
                jaccard_similarity = 0

            jaccard_similarities[(node1, node2)] = jaccard_similarity
            jaccard_similarities[(node2, node1)] = jaccard_similarity

        return jaccard_similarities

    def get_edge_weight(self, node1: str, node2: str) -> float:
        forward_edges = self.community.number_of_edges(node1, node2)
        backward_edges = self.community.number_of_edges(node2, node1)
        total_edges = forward_edges + backward_edges
        return math.log2(total_edges + 1)

    def evaluate_farmness(self, address: str) -> float:
        if not self.community.nodes[address].get('start_timestamp'):
            return 0

        root_start_timestamp = self.community.nodes[address]['start_timestamp']
        # root_end_timestamp = self.community.nodes[address]['end_timestamp']
        farm_candidates = []
        for node, similarity, in self.community.nodes[address]['jaccard_similarity'].items():
            if similarity < 0.25:
                continue

            start_timestamp = self.community.nodes[address].get('start_timestamp')
            if not start_timestamp:
                continue

            if abs((start_timestamp - root_start_timestamp).days) <= 21:
                farm_candidates.append(node)

        if len(farm_candidates) <= 5:
            return 0

        return sum(self.community.nodes[address]['jaccard_similarity'][node] for node in farm_candidates) / len(
            farm_candidates)


def main():
    initial_address = '0x7A453ced24f502aa2cf5fbD8dffBdfb1dC0a4129'
    fetcher = BlockchainDataFetcher()
    analyzer = BlockchainAnalyzer(initial_address, fetcher)
    analyzer.analyze(max_queries=4)
    analyzer.visualize()
    subgraph = analyzer.get_community_subgraph()
    print(subgraph)
    investigator = Investigator(subgraph, fetcher)
    investigator.enrich_community()
    print(investigator.evaluate_farmness(initial_address))

    # Print some example Jaccard similarities
    # for node, similarities in list(nx.get_node_attributes(subgraph, 'jaccard_similarity').items())[:5]:
    #     print(f"Jaccard similarity between {node}: {similarities}")


if __name__ == "__main__":
    main()
