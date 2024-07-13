from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, List, Dict

import requests

from .address import Address
from .erc20_transfer import ERC20Transfer
from .erc721_transfer import ERC721Transfer
from .native_token_transfer import NativeTokenTransfer
from .transfer_collection import TransferCollection


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
            response = requests.get(url, params=page_params, headers={'accept': 'application/json'})
            if not response.ok:
                break
            response = response.json()
            for tx in response.get('items', []):
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
            response = requests.get(url, params=page_params, headers={'accept': 'application/json'})
            if not response.ok:
                break

            response = response.json()
            for transfer in response.get('items', []):
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

    @classmethod
    def fetch_transaction_history(cls, addresses: List[str], num_transactions: int = 30) -> Dict[str, List[Dict]]:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(
                lambda addr: (addr, cls._fetch_transactions(addr, num_transactions)),
                addresses
            ))

        return dict(results)

    @classmethod
    def _fetch_transactions(cls, address: str, limit: int) -> List[Dict]:
        url = f"{cls.BASE_URL}/addresses/{address}/transactions"
        params = {
            'filter': 'from',
            'limit': limit  # API typically limits to 100 per request
        }
        headers = {'accept': 'application/json'}

        all_transactions = []

        while len(all_transactions) < limit:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f"Error fetching transactions for address {address}: {response.status_code}")
                break

            data = response.json()
            transactions = data.get('items', [])
            all_transactions.extend(transactions)

            if 'next_page_params' not in data or not data['next_page_params']:
                break  # No more pages

            params.update(data['next_page_params'])

        return all_transactions[:limit]