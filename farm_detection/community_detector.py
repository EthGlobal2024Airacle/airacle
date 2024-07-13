import networkx as nx
import community as community_louvain
from typing import Dict
from collections import defaultdict

class CommunityDetector:
    @staticmethod
    def detect_communities(graph: nx.MultiDiGraph) -> Dict[str, int]:
        weighted_graph = CommunityDetector._convert_to_weighted_graph(graph)
        communities = community_louvain.best_partition(weighted_graph, weight='weight')
        return communities

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

    @staticmethod
    def set_node_communities(graph: nx.MultiDiGraph, communities: Dict[str, int]):
        nx.set_node_attributes(graph, max(communities.values()) + 1, 'community')
        for node, community in communities.items():
            if node in graph.nodes:
                graph.nodes[node]['community'] = community