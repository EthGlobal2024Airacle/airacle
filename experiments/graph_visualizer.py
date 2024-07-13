from typing import Dict

import networkx as nx
import seaborn as sns
from matplotlib.colors import rgb2hex
from networkx.drawing.nx_pydot import write_dot


class GraphVisualizer:
    @staticmethod
    def apply_community_colors(graph: nx.MultiDiGraph, communities: Dict[str, int]):
        num_communities = max(communities.values()) + 1
        palette = sns.color_palette("husl", num_communities)
        color_map = {i: rgb2hex(palette[i]) for i in range(num_communities)}

        for node, community in communities.items():
            graph.nodes[node]['fillcolor'] = color_map[community]
            graph.nodes[node]['style'] = 'filled'

    @staticmethod
    def adjust_labels(graph: nx.MultiDiGraph):
        labels = {node: (str(node)[:6] + "..." + str(node)[-4:]) if len(str(node)) > 10 else str(node) for node in
                  graph.nodes()}
        for node in graph.nodes():
            graph.nodes[node]['label'] = labels[node]

    @staticmethod
    def write_graph_to_file(graph: nx.MultiDiGraph, filename: str):
        graph.graph['graph'] = {'rank': 'LR'}
        write_dot(graph, filename)
