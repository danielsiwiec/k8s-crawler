from dataclasses import dataclass


@dataclass
class Node:
    id: str
    name: str
    type: str


@dataclass
class Link:
    source: str
    target: str
