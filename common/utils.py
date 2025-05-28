import os
import json
import re
from typing import Any
from typing import Optional


# Save data as JSON to the specified file path
def save_json(data: Any, path: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # print(f"Saved to {path}")
    except Exception as e:
        print(f"Failed to save JSON to {path}: {e}")


# Load data from a JSON file and return as Python object
def load_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON from {path}: {e}")
        return []


# Clean text by collapsing whitespace and stripping leading/trailing spaces
def clean_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip()


# Create slug-style ID from title and brand
def generate_id(brand: str, title: str) -> str:
    title_slug = slugify(title)
    brand_slug = slugify(brand)
    return f"recipe_{brand_slug}_{title_slug}"


# Generate a URL-friendly slug from a string
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


# Safely strip a string
def safe_strip(value):
    return value.strip() if isinstance(value, str) else value


# Ensure the input is a dict, otherwise return empty dict
def safe_dict(d):
    return d if isinstance(d, dict) else {}


# Safely get the first element of a list,
def safe_first(lst):
    return lst[0] if isinstance(lst, list) and lst else None
