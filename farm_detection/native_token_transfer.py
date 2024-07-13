from dataclasses import dataclass

from farm_detection.transfer import Transfer


@dataclass
class NativeTokenTransfer(Transfer):
    value: str
