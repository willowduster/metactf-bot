from dataclasses import dataclass, field
from typing import List

@dataclass
class Problem:
    id: str
    title: str
    description: str
    links: List[str]
    files: List[str]
    solution_field_selector: str
    url: str
