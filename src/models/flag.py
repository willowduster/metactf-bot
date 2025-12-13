from dataclasses import dataclass
from typing import Optional

@dataclass
class Flag:
    value: str
    source_file: Optional[str] = None
    found_at: Optional[str] = None
