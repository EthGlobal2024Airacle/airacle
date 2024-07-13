from dataclasses import dataclass


@dataclass
class Address:
    hash: str
    is_contract: bool
