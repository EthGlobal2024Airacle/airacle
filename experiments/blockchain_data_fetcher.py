from typing import Tuple, List

import requests

from experiments.address import Address
from experiments.erc20_transfer import ERC20Transfer
from experiments.erc721_transfer import ERC721Transfer
from experiments.native_token_transfer import NativeTokenTransfer
from experiments.transfer_collection import TransferCollection


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
