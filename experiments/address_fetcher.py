from collections import defaultdict
from random import randrange

import networkx as nx
import requests
from typing import List
from dataclasses import dataclass, field
import community as community_louvain
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

from networkx.drawing.nx_pydot import write_dot
import seaborn as sns


@dataclass
class Transfer:
    timestamp: str
    from_address: str
    to_address: str
    tx_hash: str


@dataclass
class Address:
    hash: str
    is_contract: bool


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


def fetch_native_transfers(address: str, min_transfers: int = 50) -> List[NativeTokenTransfer]:
    base_url = f"https://arbitrum.blockscout.com/api/v2/addresses/{address}/transactions"
    native_transfers = []
    addresses = []
    page_params = {'filter': 'to'}
    page_params = {}

    pages = 0
    while len(native_transfers) < min_transfers and pages < 3:
        response = requests.get(base_url, params=page_params).json()
        for tx in response['items']:
            addresses.append(Address(tx['from']['hash'], tx['from']['is_contract']))
            if tx.get('to'):
                addresses.append(Address(tx['to']['hash'], tx['to']['is_contract']))
            if tx['value'] != '0':
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


def fetch_token_transfers(address: str, min_transfers: int = 50) -> TransferCollection:
    base_url = f"https://arbitrum.blockscout.com/api/v2/addresses/{address}/token-transfers"
    transfers = TransferCollection()
    addresses = []
    page_params = {
        # 'filter': 'to',
        # 'type': 'ERC-20,ERC-721,ERC-1155'}
        'type': 'ERC-20,ERC-721'}

    pages = 0
    while len(transfers.erc20_transfers) + len(transfers.erc721_transfers) < min_transfers and pages < 3:
        response = requests.get(base_url, params=page_params).json()
        for transfer in response['items']:
            addresses.append(Address(transfer['from']['hash'], transfer['from']['is_contract']))
            if transfer.get('to'):
                addresses.append(Address(transfer['to']['hash'], transfer['to']['is_contract']))
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

        pages += 1
        if response.get('next_page_params'):
            page_params.update(response['next_page_params'])
        else:
            break

    return transfers, addresses


g = nx.MultiDiGraph()
g.add_node('0x7Bb79cE20e464062Ae265A0a9D03F3e6a9200501', queried=False, fillcolor='red', style='filled')

remaining_queries = 10
while remaining_queries:
    non_queried_addresses = [node for node in g.nodes if
                             not g.nodes[node].get('queried') and not g.nodes[node].get('is_contract')]
    if not non_queried_addresses:
        break
    address = non_queried_addresses[randrange(len(non_queried_addresses))]
    g.nodes[address]['queried'] = True

    token_transfers, native_addresses = fetch_token_transfers(address)
    token_transfers.native_transfers, token_addresses = fetch_native_transfers(address)
    for native_transfer in token_transfers.native_transfers:
        g.add_edge(native_transfer.from_address, native_transfer.to_address)

    for token_transfer in token_transfers.erc20_transfers:
        g.add_edge(token_transfer.from_address, token_transfer.to_address)

    for token_transfer in token_transfers.erc721_transfers:
        g.add_edge(token_transfer.from_address, token_transfer.to_address)

    for rich_address in native_addresses + token_addresses:
        if rich_address.hash in g.nodes:
            g.nodes[rich_address.hash]['is_contract'] = rich_address.is_contract

    remaining_queries -= 1

if '0x0000000000000000000000000000000000000000' in g.nodes:
    g.remove_node('0x0000000000000000000000000000000000000000')


def convert_to_weighted_graph(multi_di_graph):
    g = nx.Graph()

    # Use a dictionary to store the cumulative weights of edges
    edge_weights = defaultdict(float)

    for u, v, data in multi_di_graph.edges(data=True):
        weight = data.get('weight', 1)  # Assuming default weight is 1 if not specified
        edge_weights[(u, v)] += weight

    # Add edges with cumulative weights to the new Graph
    for (u, v), weight in edge_weights.items():
        g.add_edge(u, v, weight=weight)

    return g


communities = community_louvain.best_partition(convert_to_weighted_graph(g), weight='weight')
print(communities)

num_communities = max(communities.values()) + 1
palette = sns.color_palette("husl", num_communities)
color_map = {i: rgb2hex(palette[i]) for i in range(num_communities)}


# Assign color attributes to nodes based on their community
for node, community in communities.items():
    g.nodes[node]['fillcolor'] = color_map[community]
    g.nodes[node]['style'] = 'filled'

# Adjust labels to be the first 6 characters and the last 4 characters with "..." in the middle
labels = {node: (str(node)[:6] + "..." + str(node)[-4:]) if len(str(node)) > 10 else str(node) for node in g.nodes()}

# Write the graph to a DOT file with community colors and adjusted labels
for node in g.nodes():
    g.nodes[node]['label'] = labels[node]

# g.graph['graph'] = {'overlap': False}

write_dot(g, 'notebooks/data/transfers.dot')
