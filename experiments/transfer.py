from dataclasses import dataclass


@dataclass
class Transfer:
    timestamp: str
    from_address: str
    to_address: str
    tx_hash: str
