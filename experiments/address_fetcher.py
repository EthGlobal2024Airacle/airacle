import networkx as nx
import requests
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import community as community_louvain
import seaborn as sns
from matplotlib.colors import rgb2hex
from networkx.drawing.nx_pydot import write_dot
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from random import sample
from os.path import expanduser


@dataclass
class Address:
    hash: str
    is_contract: bool


@dataclass
class Transfer:
    timestamp: str
    from_address: str
    to_address: str
    tx_hash: str


@dataclass
class NativeTokenTransfer(Transfer):
    value: str


@dataclass
class ERC20Transfer(Transfer):
    symbol: str
    value: str


@dataclass
class ERC721Transfer(Transfer):
    symbol: str
    token_id: str


@dataclass
class TransferCollection:
    native_transfers: List[NativeTokenTransfer] = field(default_factory=list)
    erc20_transfers: List[ERC20Transfer] = field(default_factory=list)
    erc721_transfers: List[ERC721Transfer] = field(default_factory=list)


class BlockchainDataFetcher:
    BASE_URL = "https://arbitrum.blockscout.com/api/v2"

    @classmethod
    def fetch_native_transfers(cls, address: str, min_transfers: int = 50) -> Tuple[
        List[NativeTokenTransfer], List[Address]]:
        url = f"{cls.BASE_URL}/addresses/{address}/transactions"
        native_transfers = []
        addresses = []
        page_params = {}

        pages = 0
        while len(native_transfers) < min_transfers and pages < 3:
            response = requests.get(url, params=page_params).json()
            for tx in response['items']:
                addresses.append(Address(tx['from']['hash'], tx['from']['is_contract']))
                if tx.get('to'):
                    addresses.append(Address(tx['to']['hash'], tx['to']['is_contract']))
                if tx['value'] != '0' and tx['to'].get('hash'):
                    native_transfers.append(NativeTokenTransfer(
                        timestamp=tx['timestamp'],
                        from_address=tx['from']['hash'],
                        to_address=tx['to']['hash'],
                        value=tx['value'],
                        tx_hash=tx['hash']
                    ))

            pages += 1
            if response.get('next_page_params'):
                page_params.update(response['next_page_params'])
            else:
                break

        return native_transfers, addresses

    @classmethod
    def fetch_token_transfers(cls, address: str, min_transfers: int = 50) -> Tuple[TransferCollection, List[Address]]:
        url = f"{cls.BASE_URL}/addresses/{address}/token-transfers"
        transfers = TransferCollection()
        addresses = []
        page_params = {'type': 'ERC-20,ERC-721'}

        pages = 0
        while len(transfers.erc20_transfers) + len(transfers.erc721_transfers) < min_transfers and pages < 3:
            response = requests.get(url, params=page_params).json()
            for transfer in response['items']:
                addresses.append(Address(transfer['from']['hash'], transfer['from']['is_contract']))
                if transfer.get('to'):
                    addresses.append(Address(transfer['to']['hash'], transfer['to']['is_contract']))

                cls._process_transfer(transfer, transfers)

            pages += 1
            if response.get('next_page_params'):
                page_params.update(response['next_page_params'])
            else:
                break

        return transfers, addresses

    @staticmethod
    def _process_transfer(transfer, transfers):
        timestamp = transfer['timestamp']
        from_address = transfer['from']['hash']
        to_address = transfer['to']['hash']
        tx_hash = transfer['tx_hash']

        if transfer['token']['type'] == 'ERC-20':
            transfers.erc20_transfers.append(ERC20Transfer(
                timestamp=timestamp,
                from_address=from_address,
                to_address=to_address,
                symbol=transfer['token']['symbol'],
                value=transfer['total']['value'],
                tx_hash=tx_hash
            ))
        elif transfer['token']['type'] == 'ERC-721':
            transfers.erc721_transfers.append(ERC721Transfer(
                timestamp=timestamp,
                from_address=from_address,
                to_address=to_address,
                symbol=transfer['token']['symbol'],
                token_id=transfer['total']['token_id'],
                tx_hash=tx_hash
            ))


class GraphBuilder:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_initial_node(self, address: str):
        self.graph.add_node(address, queried=False, fillcolor='red', style='filled')

    def update_graph(self, address: str, token_transfers: TransferCollection, addresses: List[Address]):
        self.graph.nodes[address]['queried'] = True

        for native_transfer in token_transfers.native_transfers:
            self.graph.add_edge(native_transfer.from_address, native_transfer.to_address)

        for token_transfer in token_transfers.erc20_transfers + token_transfers.erc721_transfers:
            self.graph.add_edge(token_transfer.from_address, token_transfer.to_address)

        for rich_address in addresses:
            if rich_address.hash in self.graph.nodes:
                self.graph.nodes[rich_address.hash]['is_contract'] = rich_address.is_contract
                if rich_address.is_contract:
                    self.graph.nodes[rich_address.hash]['shape'] = 'rectangle'

    def remove_zero_address(self):
        if '0x0000000000000000000000000000000000000000' in self.graph.nodes:
            self.graph.remove_node('0x0000000000000000000000000000000000000000')

    def get_non_queried_addresses(self):
        return [node for node in self.graph.nodes if
                not self.graph.nodes[node].get('queried') and not self.graph.nodes[node].get('is_contract')]


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


class BlockchainAnalyzer:
    def __init__(self, initial_address: str):
        self.initial_address = initial_address
        self.graph_builder = GraphBuilder()
        self.data_fetcher = BlockchainDataFetcher()

    def analyze(self, max_queries: int = 5):
        self.graph_builder.add_initial_node(self.initial_address)

        remaining_queries = max_queries
        while remaining_queries:
            non_queried_addresses = self.graph_builder.get_non_queried_addresses()
            if not non_queried_addresses:
                break

            addresses = self._select_addresses(non_queried_addresses)

            with ThreadPoolExecutor(max_workers=8) as executor:
                results = list(executor.map(self._query_node, addresses))

            for address, result in zip(addresses, results):
                token_transfers, native_transfers, rich_addresses = result
                token_transfers.native_transfers = native_transfers
                self.graph_builder.update_graph(address, token_transfers, rich_addresses)

            remaining_queries -= 1

        self.graph_builder.remove_zero_address()

    def _select_addresses(self, non_queried_addresses):
        addresses = sample(non_queried_addresses, min(5, len(non_queried_addresses)))
        roots = [node for node in non_queried_addresses if self.graph_builder.graph.in_degree[node] == 0]
        addresses += sample(roots, min(3, len(roots)))
        return list(set(addresses))

    def _query_node(self, address: str):
        token_transfers, token_addresses = self.data_fetcher.fetch_token_transfers(address)
        native_transfers, native_addresses = self.data_fetcher.fetch_native_transfers(address)
        return token_transfers, native_transfers, token_addresses + native_addresses

    def visualize(self):
        communities = CommunityDetector.detect_communities(self.graph_builder.graph)
        GraphVisualizer.apply_community_colors(self.graph_builder.graph, communities)
        GraphVisualizer.adjust_labels(self.graph_builder.graph)
        GraphVisualizer.write_graph_to_file(self.graph_builder.graph, expanduser('~/tmp/transfers.dot'))


def main():
    initial_address = '0x7Bb79cE20e464062Ae265A0a9D03F3e6a9200501'.lower()
    analyzer = BlockchainAnalyzer(initial_address)
    analyzer.analyze()
    analyzer.visualize()


if __name__ == "__main__":
    main()