"""Loader for predictions.json."""

import json
from pathlib import Path

_PATH = Path(__file__).parent / "predictions.json"


def load_predictions() -> list[dict]:
    if not _PATH.exists():
        return []
    with open(_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_round(round_number: int) -> dict:
    for snap in load_predictions():
        if snap["round"] == round_number:
            return snap
    return None
