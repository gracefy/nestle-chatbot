import os
import json
import re
from typing import Any
from typing import Optional


def slugify(text: str) -> str:
    """Generate a URL-friendly slug from a string."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def save_json(data: Any, path: str):
    """Save data to a JSON file with UTF-8 encoding."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clean_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip()
