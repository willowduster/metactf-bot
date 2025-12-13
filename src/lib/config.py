import os
from dotenv import load_dotenv

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, env_path: str = ".env"):
        load_dotenv(env_path)
        self.username = os.getenv("META_CTF_USERNAME")
        self.password = os.getenv("META_CTF_PASSWORD")
        self.target_env = os.getenv("TARGET_CTF_ENV")
        if not self.username or not self.password or not self.target_env:
            raise ConfigError("Missing required environment variables: META_CTF_USERNAME, META_CTF_PASSWORD, TARGET_CTF_ENV")

    def as_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "target_env": self.target_env,
        }
