import json
import os
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def read_json(filename: str) -> Any:
    """Read data from a JSON file in the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filename: str, data: Any) -> None:
    """Write data to a JSON file in the data directory."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_to_json_list(filename: str, items: List[Any]) -> None:
    """Append items to a JSON list file."""
    existing = read_json(filename)
    if not isinstance(existing, list):
        existing = []
    existing.extend(items)
    write_json(filename, existing)


def read_logs() -> List[str]:
    """Read all stored log messages."""
    return read_json("logs.json")


def save_logs(logs: List[str]) -> None:
    """Save log messages (append to existing)."""
    append_to_json_list("logs.json", logs)


def read_results() -> List[Dict]:
    """Read all stored analysis results."""
    return read_json("results.json")


def save_result(result: Dict) -> None:
    """Save a single analysis result."""
    append_to_json_list("results.json", [result])
