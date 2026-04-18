"""
Lagspecifika anteckningar, startuppställningar och stjärnklassificering för säsongen 2026.
Källa: Allsvenskan säsongsförhandsvisning 2026.
"""

# stjarnor: float 1–5 (precision 0,5)
# anteckningar: lista av strängar (punktlistor)
# startuppstallning: dict { "formation": str, "rader": list[list[str]] } uppifrån och ned
# transfers: { "in": list[str], "out": list[str] }

TEAM_NOTES: dict[int, dict] = {

    362: {  # Malmö FF
        "stjarnor": 5,
        "kategori": "Storfavorit",
        "placering_2025": "2:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Ligans starkaste trupp på pappret — bred och djup spelartrupp.",
            "Historiskt dominerande hemma på Eleda Stadion.",
            "Stark i europeiska sammanhang, vilket påverkar trötthet i ligaspelet.",
            "Offensivt explosiva med snabba anfallare på kanterna.",
        ],
        "startuppstallning": {
            "formation": "4-3-3",
            "rader": [
                ["Anfallare", "Spets", "Anfallare"],
                ["CM", "CM", "CM"],
                ["VB", "CB", "CB", "HB"],
                ["MV"],
            ],
        },
    },

    363: {  # IF Elfsborg
        "stjarnor": 4.5,
        "kategori": "Titelkandidat",
        "placering_2025": "3:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Välorganiserat lag med hög press och snabba omställningar.",
            "Starkt hemma på Borås Arena.",
            "Konsekvent topplag de senaste säsongerna.",
        ],
        "startuppstallning": None,
    },

    359: {  # IFK Göteborg
        "stjarnor": 3.5,
        "kategori": "Mittenskikt",
        "placering_2025": "5:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Historiskt storlaget med stort fansupport på Gamla Ullevi.",
            "Bygger på unga talanger och erfarna spelare.",
            "Ambition att återta topppositionerna i ligan.",
        ],
        "startuppstallning": None,
    },

    357: {  # AIK
        "stjarnor": 3.5,
        "kategori": "Mittenskikt",
        "placering_2025": "4:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Stockholm-laget med stor hemmapress på Friends Arena.",
            "Fysiskt starkt och disciplinerat försvar.",
            "Varierar mellan offensivt och defensivt spel beroende på motstånd.",
        ],
        "startuppstallning": None,
    },

    361: {  # Djurgårdens IF
        "stjarnor": 3.5,
        "kategori": "Mittenskikt",
        "placering_2025": "6:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Stockholmsderbylaget med lojal fanbas.",
            "Tekniskt fotboll med kreativa mittfältare.",
            "Stark hemma, mer ojämn borta.",
        ],
        "startuppstallning": None,
    },

    365: {  # Hammarby IF
        "stjarnor": 3.5,
        "kategori": "Mittenskikt",
        "placering_2025": "7:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Stor supporterbas och intensiv hemmastämning på Tele2 Arena.",
            "Vältränat och energiskt spelstil.",
            "Stark i derby mot AIK och Djurgården.",
        ],
        "startuppstallning": None,
    },

    568: {  # Mjällby AIF
        "stjarnor": 4,
        "kategori": "Försvarsmästare",
        "placering_2025": "1:a — Mästare",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Regerande mästare — vann Allsvenskan 2025.",
            "Extremt välorganiserat försvar, svårt att besegra.",
            "Spelar pragmatisk, effektiv fotboll snarare än underhållande.",
            "Hemmaplan på Strandvallen är en fästning.",
        ],
        "startuppstallning": None,
    },

    366: {  # BK Häcken
        "stjarnor": 3,
        "kategori": "Övre mittenskikt",
        "placering_2025": "8:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Göteborgslaget med offensiv spelstil.",
            "Producerar talanger som säljs vidare.",
            "Variabel form men kan besegra vem som helst på en bra dag.",
        ],
        "startuppstallning": None,
    },

    569: {  # IK Sirius
        "stjarnor": 3,
        "kategori": "Mittenskikt",
        "placering_2025": "9:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Uppsalalaget med stabil ligaposition de senaste åren.",
            "Välbalanserat lag utan stora stjärnor.",
            "Leder ligatabellen i tidig april 2026 — stark inledning.",
        ],
        "startuppstallning": None,
    },

    371: {  # Halmstads BK
        "stjarnor": 2.5,
        "kategori": "Nedre mittenskikt",
        "placering_2025": "10:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Etablerat Allsvenskalag men med begränsad budget.",
            "Försvarsorienterat spel för att hålla sig kvar.",
        ],
        "startuppstallning": None,
    },

    570: {  # Degerfors IF
        "stjarnor": 2,
        "kategori": "Nykomling/Nedre",
        "placering_2025": "11:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Litet lag från Degerfors med kompakt spelstil.",
            "Kampar om att undvika nedflyttning.",
        ],
        "startuppstallning": None,
    },

    372: {  # GAIS
        "stjarnor": 2,
        "kategori": "Nedre skikt",
        "placering_2025": "12:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Göteborgslaget med historik men begränsade resurser.",
            "Kämpar för överlevnad i Allsvenskan.",
        ],
        "startuppstallning": None,
    },

    370: {  # IF Brommapojkarna
        "stjarnor": 2,
        "kategori": "Nedre skikt",
        "placering_2025": "13:a",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Stockholmsklubben med ung trupp.",
            "Fokus på ungdomsutveckling snarare än direkta resultat.",
            "Nedflyttningskandidat om inte förstärkning sker.",
        ],
        "startuppstallning": None,
    },

    369: {  # Kalmar FF
        "stjarnor": 1.5,
        "kategori": "Uppflyttad",
        "placering_2025": "Superettan — uppflyttad",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Återvänder till Allsvenskan efter ett år i Superettan.",
            "Erfaret lag med bekantskap med toppdivisionen.",
            "Realistiskt mål: stanna kvar i ligan.",
        ],
        "startuppstallning": None,
    },

    573: {  # Västerås SK
        "stjarnor": 1.5,
        "kategori": "Uppflyttad",
        "placering_2025": "Superettan — uppflyttad",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Debuterar i Allsvenskan på länge.",
            "Stor utmaning att hålla sig kvar på toppnivå.",
            "Begränsad budget jämfört med etablerade Allsvenskalag.",
        ],
        "startuppstallning": None,
    },

    574: {  # Örgryte IS
        "stjarnor": 1,
        "kategori": "Uppflyttad efter 16 år",
        "placering_2025": "Superettan — uppflyttad",
        "transfers": {
            "in":  [],
            "out": [],
        },
        "anteckningar": [
            "Historisk klubb som återvänder till Allsvenskan efter 16 år.",
            "Stor emotionell händelse för Göteborg men svag trupp för toppdivisionen.",
            "Storfavorit till nedflyttning — behöver mirakel för att stanna kvar.",
        ],
        "startuppstallning": None,
    },
}
