from dataclasses import dataclass

from farm_detection.transfer import Transfer


@dataclass
class ERC721Transfer(Transfer):
    symbol: str
    token_id: str
