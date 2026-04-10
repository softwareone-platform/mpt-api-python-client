from dataclasses import dataclass


@dataclass
class QueryOptions:
    """Options for query state."""

    render: bool = False
