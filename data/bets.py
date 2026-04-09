"""
Persistent storage for bets.
List of bet dicts stored in bets.json.
"""

import json
from pathlib import Path

_PATH = Path(__file__).parent / "bets.json"


def load_bets() -> list[dict]:
    if _PATH.exists():
        with open(_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_bets(bets: list[dict]) -> None:
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(bets, f, indent=2, ensure_ascii=False)


def update_bet(bet_id: int, updates: dict) -> None:
    bets = load_bets()
    for bet in bets:
        if bet["id"] == bet_id:
            bet.update(updates)
            break
    save_bets(bets)


def add_bet(bet: dict) -> None:
    bets = load_bets()
    new_id = max((b["id"] for b in bets), default=0) + 1
    bet["id"] = new_id
    bets.append(bet)
    save_bets(bets)
