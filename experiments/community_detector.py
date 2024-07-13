from collections import defaultdict
from typing import Dict

import community as community_louvain
import networkx as nx


class CommunityDetector:
    @staticmethod
    def detect_communities(graph: nx.MultiDiGraph) -> Dict[str, int]:
        weighted_graph = CommunityDetector._convert_to_weighted_graph(graph)
        return community_louvain.best_partition(weighted_graph, weight='weight')

    @staticmethod
    def _convert_to_weighted_graph(multi_di_graph: nx.MultiDiGraph) -> nx.Graph:
        g = nx.Graph()
        edge_weights = defaultdict(float)

        for u, v, data in multi_di_graph.edges(data=True):
            weight = data.get('weight', 1)
            edge_weights[(u, v)] += weight

        for (u, v), weight in edge_weights.items():
            g.add_edge(u, v, weight=weight)

        return g
