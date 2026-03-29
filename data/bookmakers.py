"""
Bookmaker list for odds comparison.

Sharp = efficient market, reliable reference for true probabilities.
Soft = exploitable margins.

Bookmakers within the same group share the same odds feed —
if one limits, swap to another in the group.
"""

BOOKMAKERS = {
    # --- SHARPS ---
    "Pinnacle":           {"short": "Pinny",   "sharp": True,  "group": "pinnacle",  "status": "active"},
    "Veikkaus":           {"short": "Veke",    "sharp": True,  "group": "veikkaus",  "status": "active"},
    "Betfair Exchange":   {"short": "BF Exch", "sharp": True,  "group": "betfair",   "status": "active"},
    "Betfair Sportsbook": {"short": "BF SB",   "sharp": False, "group": "betfair",   "status": "active"},

    # --- SOFTS: unique feeds, no replacements if limited ---
    "Bet365":             {"short": "B365",    "sharp": False, "group": "bet365",    "status": "active"},
    "Coolbet":            {"short": "Coolbet", "sharp": False, "group": "coolbet",   "status": "active"},
    "Betway":             {"short": "Betway",  "sharp": False, "group": "betway",    "status": "active"},
    "Novibet":            {"short": "Novibet", "sharp": False, "group": "novibet",   "status": "active"},
    "Epicbet":            {"short": "Epicbet", "sharp": False, "group": "epicbet",   "status": "active"},

    # --- SOFTS: Betsson-ryhmä (sama feed) ---
    "Betsson":            {"short": "Betsson", "sharp": False, "group": "betsson",   "status": "limited"},
    "Nordicbet":          {"short": "Nordic",  "sharp": False, "group": "betsson",   "status": "active"},
    "iBet":               {"short": "iBet",    "sharp": False, "group": "betsson",   "status": "active"},
    "Rizk":               {"short": "Rizk",    "sharp": False, "group": "betsson",   "status": "active"},
    "Gutz":               {"short": "Gutz",    "sharp": False, "group": "betsson",   "status": "active"},
    "Betsafe":            {"short": "Betsafe", "sharp": False, "group": "betsson",   "status": "active"},
    "Bethard":            {"short": "Bethard", "sharp": False, "group": "betsson",   "status": "active"},

    # --- SOFTS: Olybet-ryhmä (sama feed) ---
    "Olybet":             {"short": "Olybet",  "sharp": False, "group": "olybet",    "status": "limited"},
    "Fastbet":            {"short": "Fastbet", "sharp": False, "group": "olybet",    "status": "active"},
    "Betive":             {"short": "Betive",  "sharp": False, "group": "olybet",    "status": "active"},

    # --- SOFTS: Ninjacasino-ryhmä (sama feed) ---
    "Ninjacasino":        {"short": "Ninja",   "sharp": False, "group": "ninja",     "status": "limited"},
    "Luckycasino":        {"short": "Lucky",   "sharp": False, "group": "ninja",     "status": "active"},
    "Wildz":              {"short": "Wildz",   "sharp": False, "group": "ninja",     "status": "active"},
    "Budsino":            {"short": "Budsino", "sharp": False, "group": "ninja",     "status": "active"},
    "Casinobud":          {"short": "CBud",    "sharp": False, "group": "ninja",     "status": "active"},

    # --- SOFTS: Kambi-ryhmä (sama feed) ---
    "Paf":                {"short": "Paf",     "sharp": False, "group": "kambi",     "status": "limited"},
    "Unibet":             {"short": "Unibet",  "sharp": False, "group": "kambi",     "status": "active"},
    "Leovegas":           {"short": "Leo",     "sharp": False, "group": "kambi",     "status": "active"},
    "Expekt":             {"short": "Expekt",  "sharp": False, "group": "kambi",     "status": "active"},

    # --- SOFTS: Tonybet (oma feed) ---
    "Tonybet":            {"short": "Tony",    "sharp": False, "group": "tonybet",   "status": "active"},
}

SHARPS  = [k for k, v in BOOKMAKERS.items() if v["sharp"]]
SOFTS   = [k for k, v in BOOKMAKERS.items() if not v["sharp"]]
ACTIVE  = [k for k, v in BOOKMAKERS.items() if v["status"] == "active"]
LIMITED = [k for k, v in BOOKMAKERS.items() if v["status"] == "limited"]


def best_in_group(group: str) -> list[str]:
    """Return active bookmakers in a given odds group."""
    return [k for k, v in BOOKMAKERS.items()
            if v["group"] == group and v["status"] == "active"]
