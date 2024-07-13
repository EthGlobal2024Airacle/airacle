from dataclasses import dataclass

from experiments.transfer import Transfer


@dataclass
class NativeTokenTransfer(Transfer):
    value: str
