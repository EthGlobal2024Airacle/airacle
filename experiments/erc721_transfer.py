from dataclasses import dataclass

from experiments.transfer import Transfer


@dataclass
class ERC721Transfer(Transfer):
    symbol: str
    token_id: str
