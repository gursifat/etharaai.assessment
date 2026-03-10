from dataclasses import dataclass
from pathlib import Path
from typing import List
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from `.env` if it exists.
load_dotenv(BASE_DIR / ".env")


def _parse_origins(raw: str) -> List[str]:
    """
    Convert a comma-separated CORS_ORIGINS string into a list.

    Examples:
    - "*" -> ["*"]
    - "http://localhost:3000, https://my-app.netlify.app"
      -> ["http://localhost:3000", "https://my-app.netlify.app"]
    """
    if not raw or raw.strip() == "*":
        return ["*"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@dataclass
class Settings:
    """
    Simple settings object for the application.

    Keeping this class small and explicit makes it easier for
    a beginner to understand where configuration values come from.
    """

    db_path: str = os.getenv("DB_PATH", str(BASE_DIR / "hrms.db"))
    cors_origins: List[str] = None  # will be filled in __post_init__

    def __post_init__(self) -> None:
        raw_origins = os.getenv("CORS_ORIGINS", "*")
        self.cors_origins = _parse_origins(raw_origins)


settings = Settings()

