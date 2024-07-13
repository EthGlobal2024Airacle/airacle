from dataclasses import dataclass

from .transfer import Transfer


@dataclass
class NativeTokenTransfer(Transfer):
    value: str
