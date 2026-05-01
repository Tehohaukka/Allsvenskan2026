"""Päivittää kierrosten 3-5 tulokset Sofascoresta undetected_chromedriver:lla."""
import json
import time
from pathlib import Path

_BASE = "https://api.sofascore.com/api/v1"
_TOURNAMENT_ID = 40
_SEASON_ID = 87925
_CACHE = Path(__file__).parent / "data" / "raw" / "sofascore_allsvenskan_2026.json"

ROUNDS_TO_UPDATE = [3, 4, 5]


def main():
    import undetected_chromedriver as uc

    with open(_CACHE, encoding="utf-8") as f:
        all_events: list[dict] = json.load(f)

    by_id = {e["id"]: e for e in all_events}

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options, version_main=147)

    try:
        driver.get("https://www.sofascore.com")
        time.sleep(3)

        for r in ROUNDS_TO_UPDATE:
            url = f"{_BASE}/unique-tournament/{_TOURNAMENT_ID}/season/{_SEASON_ID}/events/round/{r}"
            print(f"Haetaan kierros {r}...", flush=True)
            driver.get(url)
            time.sleep(1.5)

            try:
                body = driver.find_element("tag name", "body").text
                data = json.loads(body)
                new_events = data.get("events", [])
            except Exception as exc:
                print(f"  VIRHE kierros {r}: {exc}")
                continue

            updated = added = 0
            for e in new_events:
                e["_round"] = r
                eid = e["id"]
                if eid in by_id:
                    if by_id[eid].get("status", {}).get("type") != e.get("status", {}).get("type"):
                        by_id[eid] = e
                        updated += 1
                    elif by_id[eid].get("homeScore") != e.get("homeScore"):
                        by_id[eid] = e
                        updated += 1
                else:
                    by_id[eid] = e
                    added += 1

            for e in new_events:
                home = e.get("homeTeam", {}).get("name", "?")
                away = e.get("awayTeam", {}).get("name", "?")
                st = e.get("status", {}).get("type", "?")
                hs = e.get("homeScore", {}).get("current", "-")
                aws = e.get("awayScore", {}).get("current", "-")
                score = f"{hs}-{aws}" if st == "finished" else "ei tulosta vielä"
                print(f"  {home} {score} {away} [{st}]")

            print(f"  -> päivitetty {updated}, lisätty {added}")

    finally:
        driver.quit()

    updated_list = sorted(by_id.values(), key=lambda e: (e.get("_round", 0), e.get("startTimestamp", 0)))
    with open(_CACHE, "w", encoding="utf-8") as f:
        json.dump(updated_list, f, ensure_ascii=False, indent=2)

    print(f"\nValmis. Tallennettu {len(updated_list)} tapahtumaa.")


if __name__ == "__main__":
    main()
