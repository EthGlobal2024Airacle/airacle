from dataclasses import dataclass

from farm_detection.transfer import Transfer


@dataclass
class ERC20Transfer(Transfer):
    symbol: str
    value: str
