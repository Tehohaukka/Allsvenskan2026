"""
Hakee Allsvenskan 2025 -kauden kaikki tulokset Sofascoresta.
Tallentaa: data/raw/sofascore_allsvenskan_2025.json
"""
import json
import time
from pathlib import Path

_BASE = "https://api.sofascore.com/api/v1"
_TOURNAMENT_ID = 40  # Allsvenskan
_CACHE_DIR = Path(__file__).parent / "data" / "raw"
_CACHE_FILE = _CACHE_DIR / "sofascore_allsvenskan_2025.json"


def find_2025_season_id(driver) -> int | None:
    url = f"{_BASE}/unique-tournament/{_TOURNAMENT_ID}/seasons"
    driver.get(url)
    time.sleep(1.5)
    body = driver.find_element("tag name", "body").text
    data = json.loads(body)
    seasons = data.get("seasons", [])
    for s in seasons:
        if s.get("year") == 2025 or "2025" in str(s.get("name", "")):
            print(f"  Löydettiin kausi 2025: id={s['id']} name={s.get('name')}")
            return s["id"]
    # Jos ei löydy suoraan, tulostetaan kaikki vaihtoehdot
    print("  Kaikki kaudet:")
    for s in seasons[:10]:
        print(f"    id={s['id']} name={s.get('name')} year={s.get('year')}")
    return None


def fetch_season(driver, season_id: int) -> list[dict]:
    all_events = []
    for round_num in range(1, 31):
        url = f"{_BASE}/unique-tournament/{_TOURNAMENT_ID}/season/{season_id}/events/round/{round_num}"
        driver.get(url)
        time.sleep(1.2)
        try:
            body = driver.find_element("tag name", "body").text
            data = json.loads(body)
            events = data.get("events", [])
        except Exception as exc:
            print(f"  Kierros {round_num}: VIRHE {exc}")
            break
        if not events:
            print(f"  Kierros {round_num}: tyhjä — lopetetaan")
            break
        for e in events:
            e["_round"] = round_num
        all_events.extend(events)
        ft = sum(1 for e in events if e.get("status", {}).get("type") == "finished")
        print(f"  Kierros {round_num}: {len(events)} ottelua ({ft} valmis)", flush=True)
    return all_events


def main():
    import undetected_chromedriver as uc

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options, version_main=147)

    try:
        print("Avataan Sofascore...")
        driver.get("https://www.sofascore.com")
        time.sleep(3)

        print("Haetaan kausi-ID 2025...")
        season_id = find_2025_season_id(driver)
        if not season_id:
            print("VIRHE: kauden 2025 ID ei löytynyt")
            return

        print(f"Haetaan kaikki kierrokset (season={season_id})...")
        events = fetch_season(driver, season_id)
    finally:
        driver.quit()

    if not events:
        print("VIRHE: ei tapahtumia haettu")
        return

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    ft_count = sum(1 for e in events if e.get("status", {}).get("type") == "finished")
    print(f"\nValmis. {len(events)} tapahtumaa ({ft_count} FT) -> {_CACHE_FILE}")


if __name__ == "__main__":
    main()
