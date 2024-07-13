from dataclasses import dataclass

from experiments.transfer import Transfer


@dataclass
class ERC20Transfer(Transfer):
    symbol: str
    value: str
