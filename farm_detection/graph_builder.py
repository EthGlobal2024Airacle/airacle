from typing import List

import networkx as nx

from .address import Address
from .transfer_collection import TransferCollection


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
