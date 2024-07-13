from dataclasses import dataclass

from .transfer import Transfer


@dataclass
class ERC20Transfer(Transfer):
    symbol: str
    value: str
