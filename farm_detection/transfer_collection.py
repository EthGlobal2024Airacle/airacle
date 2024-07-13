from dataclasses import dataclass, field
from typing import List

from .erc20_transfer import ERC20Transfer
from .erc721_transfer import ERC721Transfer
from .native_token_transfer import NativeTokenTransfer


@dataclass
class TransferCollection:
    native_transfers: List[NativeTokenTransfer] = field(default_factory=list)
    erc20_transfers: List[ERC20Transfer] = field(default_factory=list)
    erc721_transfers: List[ERC721Transfer] = field(default_factory=list)
