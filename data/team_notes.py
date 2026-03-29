"""
Joukkuekohtaiset muistiinpanot, avauskokoonpanot ja tähtiluokitus kaudelle 2026.
Lähde: Positiossa-kausiennakko (Ville Makkonen & Mikko Koskenranta).
"""

# Tähtiluokitus: float 1–5 (0.5 tarkkuudella)
# Muistiinpanot: lista stringejä (bullet pointit)
# Kokoonpano: dict { "muodostelma": str, "rivit": list[list[str]] } ylhäältä alas
# Siirrot: { "in": list[str], "out": list[str] }

TEAM_NOTES: dict[int, dict] = {

    1168: {  # TPS
        "tahdet": 1,
        "kategoria": "Hirveältä näyttää",
        "sijoitus_2025": "Ykkösliigan 2. — karsinnoissa tiputtivat KTP:n",
        "siirrot": {
            "in":  ["Hradecky", "Zaal", "Ivanovic", "Talo", "Azongnitode"],
            "out": ["Boström", "Helen", "Pippola", "Riski"],
        },
        "muistiinpanot": [
            "Nousijoukkue. Ivan Pinol jatkaa päävalmentajana — onnistui nousemaan kapealla budjetilla.",
            "Viime kaudella pelattiin ylihyökkäävää futista ja maaleja annettiin myös omiin; "
            "Pinolin on nyt pakko rakentaa tiiviimpi puolustuspeli sarjatasolla.",
            "Avainpelaajat Pippola, Helen ja Boström kaikki lähteneet — viime kauden ykkösliigatähdet.",
            "Ivanovic (ex-Lahti) on todennäköinen ykköshyökkääjä, mutta jäi Lahdessa ~5 maaliin — iso kysymysmerkki.",
            "Nikolas Talo hyvä hankinta laidalle/toppariksi. Charlemagne (ex-Oulu) neutraali muisto.",
            "Zaal ja Hradecky ovat liigatasolla testaamattomia; Ikonen ja Juvente (ex-PK) myös epävarmoja.",
            "Sairinen pelasi yllättävän vahvan kauden TPS:ssä 2025 — jatkuuko kehitys?",
            "Kapea penkki: ei kestä loukkaantumisia. Viime kausi meni lähes ilman niitä — tuuri jatkuuko?",
            "Kesän siirtoikkuna ratkaiseva: taloudellisten lihasten puuttuessa täsmähankinnat vaikeita.",
            "Pelasivat harjoituspeleissä myös kolmen topparin linjaa (pakkomielte roster-kapeudesta).",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Ivanovic"],
                ["Vauhkonen", "Zaal", "Muzaci"],
                ["Hradecky", "Ikonen"],
                ["Talo", "Sihvonen", "Charlemagne", "Häggström"],
                ["Henriksson"],
            ],
        },
    },

    1166: {  # FC Lahti
        "tahdet": 1.5,
        "kategoria": "Pikapaluu liigaan",
        "sijoitus_2025": "Ykkösliigan voittaja",
        "siirrot": {
            "in":  ["Neemias", "Andersson", "Yapi", "Muller", "Cassubie"],
            "out": ["Karkulowski", "Kante", "Muzinga"],
        },
        "muistiinpanot": [
            "Nousijoukkue. Pereira rakensi tiiviin puolustuspelin — ei ilotulistusta mutta omissa ei soinut, nousu ansaittu.",
            "Selvästi vahvemmalla pohjalla kuin TPS: leveä rinki, vaihtoehto jokaiselle pelipaikalle — kestää loukkaantumisia.",
            "Lähtijöistä ei suuria menetyksiä. Tulijat kohtalaisilla CV:llä: Andersson (Ruotsin pääsarja/Superettan), Yapi (Ranska kakkostaso), Muller, Cassubie.",
            "Maalivahdit: Maukonen (19v, ykkösliiganvoittajan paras veskari) vs Hakala (ex-KuPS) — kova kilpailutilanne. Maukonen voi lähteä kesällä ulkomaille.",
            "Hyökkäys isoin kysymysmerkki: Neemias 'naamiomies' — kulttihahmo mutta epävarma. Lindholm, Mamir, Bellaabid tukena.",
            "Viime kaudella maalit jakaantuivat tasaisesti eikä yhtä selkeää piikin tekijää ollut — sama uhkakuva nyt.",
            "Ainoa joukkue joka pelaa koko kauden luonnonnurmella. Kenttä huonossa kunnossa keväällä — kotipeli 18.4 ongelma.",
            "Varakenttä Oulunkylässä tarvittaessa, mutta siirto kallis — seura haluaa pelata kotona vaikka perunakentällä.",
            "Liigakupin hallipeleissä kaatoi HJK:n — rohkaiseva merkki joukkueen tasosta.",
            "Tavoite: sarjapaikan säilytys. Onnistuessaan voi taistella yläpuoliskon viimeisistä sijoista.",
        ],
        "kokoonpano": {
            "muodostelma": "4-3-3",
            "rivit": [
                ["Neemias"],
                ["Ferreira", "Sarr"],
                ["Andersson", "Kabashi", "Montiel"],
                ["Sand", "Dantas", "Muller", "Yapi"],
                ["Maukonen"],
            ],
        },
    },

    2077: {  # AC Oulu
        "tahdet": 3,
        "kategoria": "Positiivisia merkkejä ilmassa",
        "sijoitus_2025": "10.",
        "siirrot": {
            "in":  ["Santos", "Pirinen", "Karjalainen", "Kallio"],
            "out": ["Eskelinen", "Jatta", "Rennicks", "Barrow"],
        },
        "muistiinpanot": [
            "Isokangas jatkaa päävalmentajana — viisas ratkaisu, tuo jatkuvuutta pitkään sekoiluun.",
            "Mika Nurmela urheilutoimenjohtajaksi: strategia nuoriin suomalaisiin (Eerikkilä > Afrikka).",
            "Santos (ex-Jaro) talven kovin kaappaus — torjunnoillaan tarjoaa joukkueelle pistemahdollisuudet, monet pitävät liigan parhaana.",
            "Rasmus Karjalainen palaa Ouluun — oman kylän poika, tuo johtajuutta ja maalintekoa (hyvät kaudet SJK:ssa).",
            "Pirinen tärkeä palanen topparilinjaan — puuttui Liigacupin finaalista, heti huomattiin kuinka iso.",
            "Elias Kallio (KäPa → Oulu) — yksi talven mielenkiintoisimmista siirroista, odotetaan nousua liigapelaajana.",
            "Tuomas Kaukua siirretty laitapakiksi — rohkea liike, vakuuttava talvi hallissa. Avoimena kysymys: miten sopeutuu ulkokentälle.",
            "Lähes kaikki ulkomaalaispelaajat lähteneet, jäljellä Kassama ja Ghezali — erittäin suomalainen kokoonpano.",
            "Heikkous: nuori CM-pari Mendolin + Paananen — pysyvätkö liigavauhdissa? Potentiaalia, mutta riskialtis duo.",
            "Jokelainen saa nyt kokeneita kavereita ympärilleen (Pirinen, Karjalainen, Santos) — taakkaa vähemmän.",
            "Tavoite: yläpuolisko. Kymppisija kaudelta 2026 tarkoittaisi epäonnistumista.",
            "Uusi stadion valmistuu kauden puolivälissä — iso motivaatiotekijä koko organisaatiolle.",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Karjalainen"],
                ["Kallio", "Jokelainen", "Ghezali"],
                ["Mendolin", "Paananen"],
                ["Kaukua", "Pirinen", "Pitkänen", "Kemppainen"],
                ["Santos"],
            ],
        },
    },

    650: {  # VPS
        "tahdet": 2,
        "kategoria": "Iso luuta lakaisi",
        "sijoitus_2025": "9.",
        "siirrot": {
            "in":  ["Okereke", "Piispa", "Turfkruier", "Ali", "Lima"],
            "out": ["Marttinen", "Ahiabu", "Cicale", "Justiniano", "Fall"],
        },
        "muistiinpanot": [
            "Viime kauden loppu surullinen: tappioita käytännössä kaikille heti Nuorelan jatkosopimuksen julkaisun jälkeen.",
            "Lähes kahden joukkueen verran pelaajia lähtenyt — rosteri vedetty lähes kokonaan uusiksi.",
            "Nuorela jatkaa: tunnistettava pelityyli, joka klikatessaan toimii hyvin mutta synnyttää pitkiä tappioputkia.",
            "Paljon uusia pelaajia → joukkue vaikuttaa vielä sekaiselta, avoimia kysymysmerkkejä runsaasti.",
            "Ali (kaksimetrinen hyökkääjä) — potentiaalinen kulttihahmo, mutta ei nähty talvella lainkaan.",
            "Duivenbooden myös isokokoinen kärki. Isoilla hyökkääjillä erikoistilanteet ase — ei toistaiseksi näytetty.",
            "Musinga mahdollinen kärkipelaaja: Islannin pääsarjajoukkue kiinnostunut — potentiaalia, mutta tasaisuus puuttuu.",
            "Maalivahtiosaston täysi uusinta: Piispa (20v) ja Jalloh (19v) — hyvin kokematon duo Veikkausliigaan.",
            "Räisänen ja Kouassivi poissa talvella (armeija?) — rinki ollut kapeahko.",
            "Joudin Daussi pelannut kymppipaikalla harjoituspeleissä — merkki rosteri-ongelmista.",
            "Hämmentävä 6-0 voitto SJK:sta talvella — paras peli pitkään aikaan, täysin puskista.",
        ],
        "kokoonpano": {
            "muodostelma": "3-4-1-2",
            "rivit": [
                ["Ali", "Duivenbooden"],
                ["Lindholm"],
                ["Turfkruier", "Lima", "Räisänen", "Kouassivi"],
                ["Rönnberg", "Haukioja", "Okereke"],
                ["Jalloh"],
            ],
        },
    },

    587: {  # IFK Mariehamn
        "tahdet": 1.5,
        "kategoria": "Putoamispeikkoa pakoon",
        "sijoitus_2025": "8.",
        "siirrot": {
            "in":  ["Larsson", "Pearce", "Dosis"],
            "out": ["Okereke", "Kujasalo", "David"],
        },
        "muistiinpanot": [
            "Perinne jatkuu: aina putoamisehdokas, ei koskaan putoa — Interin ja HJK:n jälkeen pisimpään Veikkausliigassa.",
            "Gary Williams jatkaa — tuli kesken toissa kauden, nihilistinen pelityyli toimii vaikka ei näytä hyvältä.",
            "Viime kausi hiuskarvan varassa: 6 peliä joissa päästettiin 4+ maalia, mutta vahva loppusarja siivitti turvalliseen säilymiseen.",
            "Cody David lähti (Slovakia) mutta korvattu kahdella: Larsson + Pearce.",
            "Adam Larsson palaa IFK:hon — 'lähes takuuvarma' maalintekijä Veikkausliigaan, maalit tulevat ryppäässä.",
            "Luke Pearce lainalle Cardifista — Liigacupissa 2 maalia Lahtea vastaan, vakuuttava viimeistely. Kaksikko Larsson–Pearce iso odotus.",
            "Dosis tuli keskikentän pohjalle — vaikuttanut hyvältä talvella.",
            "Pelitapa muuttuu: timantti (diamond) keskikentässä + kärki-kaksikko. Ei enää klassisia laitahyökkääjiä (Reed, Cardoso lähteneet).",
            "Aktiivisempaa pallonhallintaa tavoitellaan — positiivisia merkkejä Liigacupissa pitkästä aikaa.",
            "Tuomas Koivisto (ex-SJK) — odottamaton vahvistus topparilinjaan, jäi mieleen TPS-harjoitusottelusta.",
            "Noas Nurmi pitkä loukkaantuminen takana — todennäköisesti ottaa topparin roolin.",
            "Pontus Lindgren jatkaa mutta todennäköisesti löytää itsensä penkiltä.",
        ],
        "kokoonpano": {
            "muodostelma": "4-4-2 (timantti)",
            "rivit": [
                ["Pearce", "Larsson"],
                ["Dahlström"],
                ["Van der Heyden", "Dosis", "Huttunen"],
                ["Soiniemi", "Amankwah", "Nurmi", "Nissine"],
                ["Riikonen"],
            ],
        },
    },

    2075: {  # FF Jaro
        "tahdet": 1.5,
        "kategoria": "Vaikea toinen kausi ylhäällä tiedossa?",
        "sijoitus_2025": "7.",
        "siirrot": {
            "in":  ["Sjögrell", "Vits", "Pedersen", "Skau", "Zetterström"],
            "out": ["Santos", "Cissoko", "Kusu", "Björkskog", "S. Eremenko"],
        },
        "muistiinpanot": [
            "Upea debyyttikausi: 7. sija vaikka kaikki ennustivat suoraa putoamista.",
            "Koko vahva keskiakseli hajosi: Santos (MV→Oulu), Kusu (CM), Sissoko (hyökkäys) — kaikki lähteneet.",
            "Vides Cook lähti → Jens Carlson uudeksi valmentajaksi. Kyseenalainen ratkaisu: miksi korjata jotain, mikä ei ole rikki?",
            "Carlson vie pelitapaa pallollisesti eteenpäin ja aggressiivisempaan hyökkäyssuuntaan — riskaabelimpaa kuin Vides Cookin kurinaläinen tyyli.",
            "Rudy Vikström (18v) — kauden seuratuimpia pelaajia. Tekee maaleja kaikkialla, U19-maajoukkueessa 5 maalia 7 pelissä. Optiovuosi otettu → siirtokorvaus Ruotsiin tulossa.",
            "Kaius Harden (HJK/Klubi04 → Jaro, 21v) — monipuolinen, pystyy usealla pelipaikalla, yksi maalin Liigacupissa.",
            "Vits (MV) kärsinyt polvivammasta talvella — todellinen taso testaamatta. Varavahtina kokenematon pelaaja.",
            "Toppariosasto pysynyt pääosin samana — yksi vahvemmista osastoista.",
            "Uudet pelaajat (Pedersen, Skau, Sjögrell) — ulkomailta tuotuja, hankala arvioida etukäteen. Kusu-tason korvaajaa ei näkyvissä.",
            "Johtajuus kysymysmerkki: Gunnarsson tärkein johtaja, mutta poissa joistain harjoituspeleistä.",
            "Pietarsaari (20 000 as.) — pieni seura, ei varaa isille riskeille. Valmentajavaihdos siksi rohkea peliliike.",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Vikström"],
                ["Weckström", "Pedersen", "Sjögrell"],
                ["Vidjeskog", "Skau"],
                ["Ness", "Ogungbaro", "Gunnarsson", "Bjonbäck"],
                ["Vits"],
            ],
        },
    },

    2082: {  # IF Gnistan
        "tahdet": 2.5,
        "kategoria": "Riittääkö yläloppusarjaan?",
        "sijoitus_2025": "6.",
        "siirrot": {
            "in":  ["Akinyemi", "Ylätupa", "Obileye", "Perez", "Jouhi"],
            "out": ["Raitala", "Pettersson", "Heiskanen", "Väyrynen", "Kabashi"],
        },
        "muistiinpanot": [
            "Historiallinen kausi 2025: ensimmäistä kertaa yläloppusarjassa (6.). Pääkaupunkiseudun mestaruus — voitti HJK:n keskinäisessä vertailussa.",
            "Leppälahti jatkaa valmentajana — jatkuvuus iso etu.",
            "Roma Eremenko jatkaa — kauden tärkein uutinen. Kapellimestari keskikentällä.",
            "Cranix (= Gran) pelikiellossa kauden alussa (punainen kortti 2025) → Almeida aloittaa MV:nä.",
            "Talvi tuloksellisesti heikko, mutta Leppälahti kierrätti kokoonpanoa — ei paniikkia.",
            "Akinyemi (ex-Ilves) — joko tykkikausi tai täysi floppi, ei siltä väliltä. Sopii Gnistanin tyyliin paremmin kuin Ilvekseen.",
            "Ylätupa — 26v, poissa Veikkausliigasta ~6 vuotta (lyhyt IFK-laina 2020). Suuri kysymysmerkki.",
            "Perez (Danny) — 26v, koko ura Etelä-Amerikassa, ensimmäinen Eurooppa-kokemus. Arpa.",
            "Jouhi (ex-KäPa) — kypsä esiintyminen, saa peliaikaa erityisesti jos Baskirov sivussa pitkään.",
            "Europaeus — tutkan alla lentänyt parikymppinen, isoja minuutteja jo nyt. Selkeästi eteenpäin menevä pelaaja.",
            "Obileye (ex-SJK) — iso toppari, vahvistaa puolustusta.",
            "Hyökkäyskolmikko (Akinyemi, Perez, Ylätupa) täynnä kysymysmerkkejä — epätodennäköistä, että kaikki onnistuvat.",
            "Tavoite: yläloppusarjapaikka kolmatta kautta putkeen. Eurooppa-paikat epärealistisia.",
        ],
        "kokoonpano": {
            "muodostelma": "4-3-3",
            "rivit": [
                ["Perez", "Akinyemi", "Ylätupa"],
                ["Eremenko R.", "Hänninen", "Europaeus"],
                ["Arko-Mensah", "Gnanou", "Ojala", "Bjuström"],
                ["Cranix"],
            ],
        },
    },

    649: {  # HJK Helsinki
        "tahdet": 4.5,
        "kategoria": "Menetetty etumatka",
        "sijoitus_2025": "5.",
        "siirrot": {
            "in":  ["Cicale", "Borchers", "Cissokho", "Kirilov", "Lappalainen"],
            "out": ["Hostikka", "Anzoulas", "Kanellopoullos", "Michel"],
        },
        "muistiinpanot": [
            "2025: 5. sija — historiallinen pettymys, mestaruus menetettiin. Rantanen uudeksi päävalmentajaksi.",
            "Cicale (Alfie) — loukkaantui harjoituspelissä TPS:ää vastaan (takareisi?), loukkaantumishistoriaa. Kunnossa ollessaan yksi liigan parhaista laituritta.",
            "Lappalainen (Lassi) — suuri kysymysmerkki, ei pysynyt kunnossa viime vuosina. Vasemman laidan ykkönen jos pelaa.",
            "Laituriosasto isoin ongelma: jos Cicale + Lappalainen sivussa, vaihtoehdot ovat Toivo Mero (18v) ja Kirilov joka ei ole varsinainen laituri.",
            "Kirilov (Martin, 18v) — yksi kauden mielenkiintoisimmista pelaajista. Pystyy pelaamaan usealla pelipaikalla.",
            "Pukki (Teemu) — hyökkäyksen ankkuri. Borchers tuli viimein kunnon varamieheksi kärkeen.",
            "Cicale–Borchers-tandemi tunnetaan jo VPS:stä — kemia voi olla iso etu.",
            "Ring (Alexander) — avainpelaaja keskikentällä.",
            "Mentu (Pyry, 19v) ja Toivo Mero (18v) — nuoret lupaukset, HJK:n tulevaisuus. Molemmille toivotaan peliaikaa.",
            "Vaihtoehto: timantti + kaksi kärkeä, jos laitureista puutetta.",
            "Mestaruustaistelu — ehdokas mutta ei enää selkeä suosikki. Puolustus ollut ongelma sarjan topseuroja vastaan.",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Pukki"],
                ["Cicale", "Ring", "Lappalainen"],
                ["Lingman", "Mentu"],
                ["Montano", "Cissokho", "Tikkanen", "Ylitolva"],
                ["Markovic"],
            ],
        },
    },

    689: {  # SJK
        "tahdet": 3,
        "kategoria": "Kaaoksen aikakausi ohi",
        "sijoitus_2025": "4.",
        "siirrot": {
            "in":  ["Boström", "Mömmö", "Djalo"],
            "out": ["Fati", "Gasc", "Karjalainen", "Laine", "Vargas"],
        },
        "muistiinpanot": [
            "Stevie Greve lähti → Jarkko Viss uudeksi valmentajaksi. Iso muutos pelityylissä: kaaosfutis vähenee, kontrolloidumpaa ja defensiivisempää.",
            "Paananen jatkaa — maalipörssivoittaja, kauden selkeä tähtipelaaja. Saattaa lähteä kesällä → Djalo hankittu varautumisena.",
            "Isot lähtijät: Fati (parhaat liigassa pelipaikkansa pelissä), Karjalainen (→Oulu), Laine (loistava loppukausi), Vargas (tuskin palaa lainalta).",
            "Piers Cook hankittu mutta sai polvivamman TPS-harjoituspelissä — pidempi sivussa.",
            "Mömmö (ex-Haka) — hyvä rekry, yksi Hakan loppukauden onnistujista.",
            "Boström (ex-TPS) — mielenkiintoinen profiili, todennäköisesti avauksessa heti alusta.",
            "Streng kärkipelaajana — saanut kritiikkiä kannattajilta maalimäärästä, mutta teki maaleja Grevenin järjestelmässä. Rangel (ex-KTP) huhuissa vahvistukseksi.",
            "Talvi tuloksellisesti heikko: 6-0 tappio VPS:lle — häpeällinen tulos, mutta Viss peluutti laajaa kokoonpanoa.",
            "Pires voi olla MM-kisoissa kesällä (~kuukausi pois) — toppariosasto jo valmiiksi ohkainen (Pires, Chukwudi).",
            "Nippu heikentynyt kokonaisuutena. Yläloppusarjaan pitäisi päästä, mutta europaikkataistelua vaikea toistaa.",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Streng"],
                ["Mastokangas", "Paananen", "Tessilimi"],
                ["Boström", "Arsalo"],
                ["Mömmö", "Chukwudi", "Pires", "Yussif"],
                ["Paunio"],
            ],
        },
    },

    1163: {  # Ilves
        "tahdet": 4.5,
        "kategoria": "Mestaruutta metsästämään",
        "sijoitus_2025": "3.",
        "siirrot": {
            "in":  ["Pettersson", "Bamba", "Baranov"],
            "out": ["Jukkola", "Söderbäck", "Mäenpää"],
        },
        "muistiinpanot": [
            "Rantanen lähti HJK:hon ja urheilutoimenjohtaja Takkula AIK:hon — iso shokki, mutta Joni Lehtonen päävalmentajaksi seuran sisältä. Jatkuvuus säilyy.",
            "Jukkola, Söderbäck ja Mäenpää etenivät ulkomaille. Korvaajat (Raymond, Kanga) hankittiin jo viime kauden aikana — varautuminen onnistui.",
            "Europeleihin — leveyttä pakko olla. Runko pysynyt hyvin kasassa.",
            "Hytönen (Teemu) — monipuolinen, pelaa sekä kärkessä että laidalla. Talven vahvin esiintyjä, tärkein palanen hyökkäyksessä.",
            "Kanga (Sharel) — Ruotsin U21-vakio, suuri kehityspotentiaali. Hintalappu kasvaa jos onnistuu.",
            "Raymond — ei vielä vakuuttanut, epätasainen. Paljon parannettavaa.",
            "Riski — ys-paikka. Baranov (ex-Klubi04) — epätasainen, tehot tuli rypähtenä ykkösliigatason alussa.",
            "MV: Virtanen vs Kalic — pelanneet puoliksi, selkeää ykköstä ei lukittu. Parempi saada selkeys.",
            "Väisänen vahva ykköstoppari. Viereen kilpailua: Miettunen, Kumpu (18v, lupaava), Pettersson.",
            "Veteli loukkaantuneena mutta palaamassa. Alamyllymäki samoin — keskilinja vahvistuu kauden edetessä.",
            "Mestaruustaistoon mukaan — 4. sija tai huonompi olisi pettymys.",
        ],
        "kokoonpano": {
            "muodostelma": "4-2-3-1",
            "rivit": [
                ["Riski"],
                ["Raymond", "Kanga", "Stjopin"],
                ["Popovitch", "Veteli"],
                ["Rale", "Väisänen", "Miettunen", "Pettersson"],
                ["Virtanen"],
            ],
        },
    },

    1164: {  # FC Inter Turku
        "tahdet": 4.5,
        "kategoria": "Riittääkö bensa loppuun saakka?",
        "sijoitus_2025": "2.",
        "siirrot": {
            "in":  ["Ahiabu", "Laine", "Salomaa", "Conteh", "Ulundu"],
            "out": ["Krebs", "Legbo", "Kouame", "Straalman"],
        },
        "muistiinpanot": [
            "2025: hopea. Runkosarjan vakuuttavin joukkue — mestaruus meni kun Kuome myytiin kesällä ja Essomba loukkaantui loppusarjaan.",
            "Liigacupin voittaja kolmatta kertaa putkeen. Europeleihin — kausi on raskas.",
            "Vesa Vasara jatkaa. Pallohallintafutis + poikkeuksellisen vahva puolustusrakenne — yksilötasolla ja joukkueena.",
            "Puolustus sarjan paras: Huuhtanen erinomainen MV, Kuittinen+Kangasniemi (18v!) topparipari, Niska+Granlund laitapakkeina.",
            "Krebs lähti → erikoistilanteet iso menetys. Korvaaja: Kiiskilä (18v) — Interin viimeiset 3 maalia tulleet hänen syötöistään (Liigacup + kulmapotkut). Voiko vakituiseen?",
            "Legbo lähti (tykkikausi). Korvaajiksi Salomaa (Italia → Suomi) ja Ulundu (ex-Ilves, pieni siirtokorvaus).",
            "Conteh (Norja, laina, osto-optio) — ys-paikka, kysymysmerkki.",
            "Ahiabu (ex-VPS) — puolustava vaihtoehto Kuomeen pallolliseen tilalle. Pystyykö kehittämään pallollista peliä Vasaran alaisuudessa?",
            "Ampofo ja Järvinen loukkaantuneena kauden alussa — Kiiskilälle avautuu mahdollisuus.",
            "Viki Savonen (ex-KuPS skautti) pelaajatarkkailun päälliköksi — iso organisatorinen vahvistus, tulevaisuuden hankinnat paranevat.",
            "Mestaruustaistoon selvä ehdokas — ei enää yllätys vaan odotus.",
        ],
        "kokoonpano": {
            "muodostelma": "4-3-3",
            "rivit": [
                ["Salomaa", "Conteh", "Essomba"],
                ["Laine", "Ahiabu", "Ampofo"],
                ["Niska", "Kuittinen", "Kangasniemi", "Granlund"],
                ["Huuhtanen"],
            ],
        },
    },

    # KuPS — Kaksoismestari hakee kolmatta
    1165: {
        "tahdet": 4.5,
        "kategoria": "Kaksoismestari hakee kolmatta",
        "sijoitus_2025": 1,
        "siirrot": {
            "in":  ["Adams", "Heiskanen", "Engvall", "Gasc", "Kabuye"],
            "out": ["Oksanen", "Arifi", "Cisse", "Miettinen", "Toure"],
        },
        "muistiinpanot": [
            "Kaksoismestari 2025. Eurooppalainen huippukausi: liigavaiheeseen ja sieltä jatkoon — merkittävä tulo kassaan.",
            "Tuure ja Ruoppi molemmat myytiin yli miljoona siirtosummalla. Ruoppi jäi lainalle kesäkuun loppuun.",
            "Uusi päävalmentaja Miika Nuutinen (hoiti HJK:n lopun 2025). Nuori valmentaja kovassa paikassa — fiksua kopioida Booströmin ja Visin rakentama pelitapa.",
            "Kasim Adams — ghanalais-toppari kovalla CV:llä: Bundesliiga, Eurooppa-liiga, Konferenssiliiga. Kolmekymppinen, mutta selvästi sarjan tasoinen hankinta.",
            "Valentin Gasc SJK:sta — 'tekee ympärillä olevista parempia'. Tunteikkaat jäähyväiset SJK:ssa, motivaatio näyttämiseen kova.",
            "Kalvin Kabuye — nopea laitahaastaja, profiili jota Kupsissa ei ole ollut vuosiin.",
            "Gustav Engvall 29v, ruotsalainen, tuli Puolasta. Vähän maalitilastoja urallaan — kysymysmerkki.",
            "Ruopin lopullinen lähtö kesällä odotettavissa — pitää varautua korvaajaan siirtoikkunassa.",
            "Voutilainen ja Pasanen pitkään sivussa — käytännössä ulkona kaudelta.",
            "Booström siirtyi sporting directoriksi, Erik Baggerfeld uusi chief scout (Ruotsista) — korvaa Viki Savosen, joka lähti Interiin.",
        ],
        "kokoonpano": {
            "muodostelma": "4-3-3",
            "rivit": [
                ["Kabuye", "Engvall", "Ruoppi"],
                ["Gasc", "Pennanen", "Kujasalo"],
                ["Antwi", "Hämäläinen", "Adams", "Armah"],
                ["Kreidl"],
            ],
        },
    },

}
