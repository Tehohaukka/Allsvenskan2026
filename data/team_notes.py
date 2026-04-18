"""
Joukkuekohtaiset muistiinpanot, aloituskokoonpanot ja tähtien luokittelu kaudelle 2026.
Lähde: Allsvenskan 2026 -kauden ennakko.
"""

# tahdet: float 1–5 (tarkkuus 0,5)
# muistiinpanot: lista merkkijonoista (luettelomerkityt)
# kokoonpano: dict { "muodostelma": str, "rivit": list[list[str]] } ylhäältä alas
# siirrot: { "in": list[str], "out": list[str] }

TEAM_NOTES: dict[int, dict] = {

    362: {  # Malmö FF
        "tahdet": 5,
        "kategoria": "Suursuosikki",
        "sijoitus_2025": "2.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Liigan vahvin joukkue paperilla — laaja ja syvä pelaajisto.",
            "Historiallisesti hallitseva kotona Eleda Stadionilla.",
            "Vahva eurooppalaisissa peleissä, mikä vaikuttaa väsymykseen liigassa.",
            "Hyökkäyksellisesti räjähtävä nopeiden laitahyökkääjien ansiosta.",
        ],
        "kokoonpano": {
            "muodostelma": "4-3-3",
            "rivit": [
                ["Hyökkääjä", "Kärkihyökkääjä", "Hyökkääjä"],
                ["KK", "KK", "KK"],
                ["VP", "KP", "KP", "OP"],
                ["MV"],
            ],
        },
    },

    363: {  # IF Elfsborg
        "tahdet": 4.5,
        "kategoria": "Mestaruusehdokas",
        "sijoitus_2025": "3.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Hyvin organisoitu joukkue korkealla pressillä ja nopeilla siirtymillä.",
            "Vahva kotona Borås Arenalla.",
            "Tasainen kärkijoukkue viime kausina.",
        ],
        "kokoonpano": None,
    },

    359: {  # IFK Göteborg
        "tahdet": 3.5,
        "kategoria": "Keskikasti",
        "sijoitus_2025": "5.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Historiallisesti suuri seura ja suuri fanijoukko Gamla Ullevilla.",
            "Rakentaa nuorista lahjakkuuksista ja kokeneista pelaajista.",
            "Tavoitteena palata liigan kärkipaikoille.",
        ],
        "kokoonpano": None,
    },

    357: {  # AIK
        "tahdet": 3.5,
        "kategoria": "Keskikasti",
        "sijoitus_2025": "4.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Tukholmalainen seura suurella kotipaineen Friends Arenalla.",
            "Fyysisesti vahva ja kurinalaisesti puolustava.",
            "Vaihtelee hyökkäävän ja puolustavan pelin välillä vastustajan mukaan.",
        ],
        "kokoonpano": None,
    },

    361: {  # Djurgårdens IF
        "tahdet": 3.5,
        "kategoria": "Keskikasti",
        "sijoitus_2025": "6.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Tukholmalainen derbyseura uskollisella fanijoukkiolla.",
            "Tekninen jalkapallo luovilla keskikenttäpelaajilla.",
            "Vahva kotona, epätasaisempi vieraissa.",
        ],
        "kokoonpano": None,
    },

    365: {  # Hammarby IF
        "tahdet": 3.5,
        "kategoria": "Keskikasti",
        "sijoitus_2025": "7.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Suuri kannattajakunta ja intensiivinen kotitunnelma Tele2 Arenalla.",
            "Hyvin harjoiteltu ja energinen pelityyli.",
            "Vahva derbeissä AIK:ta ja Djurgårdia vastaan.",
        ],
        "kokoonpano": None,
    },

    568: {  # Mjällby AIF
        "tahdet": 4,
        "kategoria": "Puolustajavahvuus",
        "sijoitus_2025": "1. — Mestari",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Hallitseva mestari — voitti Allsvenskanin 2025.",
            "Erittäin hyvin organisoitu puolustus, vaikea voittaa.",
            "Pelaa pragmaattista, tehokasta jalkapalloa viihteellisyyden sijaan.",
            "Kotistadion Strandvallen on linnoitus.",
        ],
        "kokoonpano": None,
    },

    366: {  # BK Häcken
        "tahdet": 3,
        "kategoria": "Ylempi keskikasti",
        "sijoitus_2025": "8.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Göteborgilainen seura hyökkäävällä pelityylillä.",
            "Tuottaa lahjakkuuksia eteenpäin myytäväksi.",
            "Vaihteleva vire, mutta voi voittaa kenet tahansa hyvänä päivänä.",
        ],
        "kokoonpano": None,
    },

    569: {  # IK Sirius
        "tahdet": 3,
        "kategoria": "Keskikasti",
        "sijoitus_2025": "9.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Uppsalalalainen seura vakaan liiga-aseman kanssa viime vuosina.",
            "Tasapainoinen joukkue ilman suuria tähtiä.",
            "Johtaa liigaa huhtikuun alussa 2026 — vahva avaus.",
        ],
        "kokoonpano": None,
    },

    371: {  # Halmstads BK
        "tahdet": 2.5,
        "kategoria": "Alempi keskikasti",
        "sijoitus_2025": "10.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Vakiintunut Allsvenskan-seura rajoitetulla budjetilla.",
            "Puolustuspainotteinen peli pysymiseksi sarjassa.",
        ],
        "kokoonpano": None,
    },

    570: {  # Degerfors IF
        "tahdet": 2,
        "kategoria": "Uustulokas/Alhainen",
        "sijoitus_2025": "11.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Pieni seura Degerforssista kompaktilla pelityylillä.",
            "Taistelee pudotuksen välttämiseksi.",
        ],
        "kokoonpano": None,
    },

    372: {  # GAIS
        "tahdet": 2,
        "kategoria": "Alempi kaasi",
        "sijoitus_2025": "12.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Göteborgilainen seura historialla mutta rajoitetuilla resursseilla.",
            "Taistelee selviytymisestä Allsvenskanissa.",
        ],
        "kokoonpano": None,
    },

    370: {  # IF Brommapojkarna
        "tahdet": 2,
        "kategoria": "Alempi kaasi",
        "sijoitus_2025": "13.",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Tukholmalainen seura nuorella joukkueella.",
            "Painopiste nuorisokehityksessä välittömien tulosten sijaan.",
            "Pudotusehdokas ilman vahvistuksia.",
        ],
        "kokoonpano": None,
    },

    369: {  # Kalmar FF
        "tahdet": 1.5,
        "kategoria": "Nousijajoukkue",
        "sijoitus_2025": "Superettan — noussut",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Palaa Allsvenskaniin vuoden Superettanissa olon jälkeen.",
            "Kokenut joukkue jolla tuttavuus korkeimmasta sarjasta.",
            "Realistinen tavoite: pysyä sarjassa.",
        ],
        "kokoonpano": None,
    },

    573: {  # Västerås SK
        "tahdet": 1.5,
        "kategoria": "Nousijajoukkue",
        "sijoitus_2025": "Superettan — noussut",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Debytoi Allsvenskanissa pitkän tauon jälkeen.",
            "Suuri haaste pysyä huipputasolla.",
            "Rajoitettu budjetti verrattuna vakiintuneisiin Allsvenskan-seuroihin.",
        ],
        "kokoonpano": None,
    },

    574: {  # Örgryte IS
        "tahdet": 1,
        "kategoria": "Nousija 16 vuoden tauon jälkeen",
        "sijoitus_2025": "Superettan — noussut",
        "siirrot": {
            "in":  [],
            "out": [],
        },
        "muistiinpanot": [
            "Historiallinen seura joka palaa Allsvenskaniin 16 vuoden tauon jälkeen.",
            "Suuri tunnelataaus Göteborgille, mutta heikko joukkue huipputasolla.",
            "Suursuosikki pudotukseen — tarvitsee ihmeen pysyäkseen.",
        ],
        "kokoonpano": None,
    },
}
