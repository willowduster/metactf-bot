from dataclasses import dataclass

@dataclass
class Credentials:
    username: str
    password: str
    target_env: str
