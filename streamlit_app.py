import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(page_title="Presenttipset", page_icon=":material/redeem:", layout="centered")

# Produkt: namn, pris, minålder, maxålder, kön, intressen, mottagare, tillfällen, typ, beskrivning, länk, butik, bild
P = [
    # --- Riktiga produkter ---
    ("SkiSoft – skydd för smalbenet i pjäxan", 399, 5, 80, "alla", "Vintersport|Sport|Friluftsliv|Träning",
     "alla", "Jul|Födelsedag", "sak",
     "Tunn strumpa med mjuk dyna mot pjäxan. Slut på ömma smalben i backen – passar både vuxna och barn.",
     "https://sivelo.se/products/skisoft", "Sivelo",
     "https://sivelo.se/cdn/shop/files/hf_20261114_120545_5c9eef6c-89eb-494f-befb-0263f336f921.png?v=1794657994&width=600"),

    # --- Exempelprodukter ---
    ("Gjutjärnsgryta", 899, 25, 99, "alla", "Matlagning", "Partner|Mamma|Pappa|Svärförälder", "Jul|Födelsedag|Inflyttning", "sak", "Håller livet ut, perfekt för långkok.", "", "", ""),
    ("Japansk kockkniv", 1290, 25, 99, "alla", "Matlagning", "Partner|Pappa|Vän", "Jul|Födelsedag|Fars dag", "sak", "Rakbladsvass och rolig att laga mat med.", "", "", ""),
    ("Matlagningskurs för två", 1695, 20, 80, "alla", "Matlagning|Dryck", "Partner|Mamma|Pappa|Vän", "alla", "upplevelse", "Lär er ett nytt kök tillsammans.", "", "", ""),
    ("Surdegskit", 299, 18, 99, "alla", "Matlagning", "alla", "alla", "sak", "Jäskorg, degskrapa och surdegsgrund.", "", "", ""),
    ("Handkvarn för kaffe", 599, 20, 99, "alla", "Kaffe & te", "alla", "alla", "sak", "Nymalet kaffe varje morgon.", "", "", ""),
    ("Teprovning-ask", 279, 16, 99, "alla", "Kaffe & te|Avkoppling", "alla", "alla", "sak", "24 sorters te i fin ask.", "", "", ""),
    ("Whiskyprovning", 795, 20, 99, "alla", "Dryck", "Pappa|Partner|Vän|Svärförälder", "Födelsedag|Fars dag|Jul", "upplevelse", "Guidad provning med expert.", "", "", ""),
    ("Smart träningsklocka", 2490, 15, 75, "alla", "Träning|Teknik", "Partner|Barn|Syskon|Mamma|Pappa", "Jul|Födelsedag|Student", "sak", "Puls, GPS och sömnanalys.", "", "", ""),
    ("Massagepistol", 999, 18, 80, "alla", "Träning|Avkoppling", "alla", "alla", "sak", "Mjukar upp stela muskler.", "", "", ""),
    ("Pannlampa 1000 lumen", 399, 12, 99, "alla", "Friluftsliv|Träning", "alla", "alla", "sak", "Stark och laddbar.", "", "", ""),
    ("Övernattning i trädkoja", 3490, 18, 80, "alla", "Friluftsliv|Resor|Avkoppling", "Partner|Mamma|Pappa", "Födelsedag|Alla hjärtans dag|Jul", "upplevelse", "En natt i naturen för två.", "", "", ""),
    ("Brusreducerande hörlurar", 1990, 12, 80, "alla", "Teknik|Musik|Resor", "alla", "Jul|Födelsedag|Student", "sak", "Stäng ute världen.", "", "", ""),
    ("Bluetooth-högtalare", 799, 10, 70, "alla", "Musik|Teknik|Friluftsliv", "alla", "alla", "sak", "Vattentålig, för bryggan och duschen.", "", "", ""),
    ("Gaming-headset", 899, 10, 45, "alla", "Gaming|Teknik", "Barn|Syskon|Partner|Vän", "Jul|Födelsedag", "sak", "Tydligt ljud och mikrofon.", "", "", ""),
    ("Digital fotoram", 1290, 40, 99, "alla", "Teknik|Inredning", "Mor-/farförälder|Mamma|Pappa|Svärförälder", "Jul|Födelsedag|Mors dag|Fars dag", "personlig", "Skicka bilder direkt från mobilen.", "", "", ""),
    ("Escape room", 1200, 12, 70, "alla", "Spel & pussel|Gaming", "Vän|Syskon|Kollega|Barn", "Födelsedag|Student", "upplevelse", "60 minuter att ta sig ut.", "", "", ""),
    ("E-boksläsare", 1590, 12, 99, "alla", "Läsning|Resor", "alla", "Jul|Födelsedag|Student", "sak", "Tusentals böcker i fickan.", "", "", ""),
    ("Ljudbokprenumeration", 507, 12, 99, "alla", "Läsning|Avkoppling", "alla", "alla", "upplevelse", "Obegränsat i tre månader.", "", "", ""),
    ("Pussel 1000 bitar", 229, 10, 99, "alla", "Spel & pussel|Avkoppling", "alla", "alla", "sak", "Mysigt pussel med vackert motiv.", "", "", ""),
    ("Sällskapsspel", 349, 16, 80, "alla", "Spel & pussel", "alla", "alla", "rolig", "Garanterade skratt.", "", "", ""),
    ("Akvarellkit", 449, 10, 99, "alla", "Kreativt", "alla", "alla", "sak", "Kom igång direkt.", "", "", ""),
    ("Keramikkurs", 995, 16, 80, "alla", "Kreativt|Inredning", "Partner|Mamma|Syskon|Vän", "Födelsedag|Mors dag|Jul", "upplevelse", "Dreja din egen kopp.", "", "", ""),
    ("Doftljus", 299, 16, 99, "alla", "Inredning|Avkoppling", "alla", "alla", "sak", "Mysigt för vinterkvällar.", "", "", ""),
    ("Tyngdtäcke", 1290, 15, 99, "alla", "Avkoppling", "Partner|Mamma|Pappa|Syskon|Barn", "Jul|Födelsedag", "sak", "Hjälper många att sova bättre.", "", "", ""),
    ("Spa-dag för två", 2390, 18, 90, "alla", "Avkoppling|Skönhet", "Partner|Mamma|Syskon|Vän", "alla", "upplevelse", "En hel dag av lugn.", "", "", ""),
    ("Inomhusodling med LED", 899, 18, 99, "alla", "Odling|Matlagning", "alla", "alla", "sak", "Färska örter året runt.", "", "", ""),
    ("Stjärnkarta", 449, 16, 99, "alla", "Inredning", "Partner|Barn|Mamma|Pappa", "Alla hjärtans dag|Födelsedag|Jul", "personlig", "Himlen från er speciella dag.", "", "", ""),
    ("Hudvårdsset", 549, 16, 90, "kvinna", "Skönhet", "Partner|Mamma|Syskon|Vän", "alla", "sak", "Rengöring, serum och kräm.", "", "", ""),
    ("Skäggvårdskit", 399, 18, 90, "man", "Skönhet|Mode", "Partner|Pappa|Syskon|Vän", "alla", "sak", "Olja, balm och kam.", "", "", ""),
    ("Kashmirhalsduk", 1190, 20, 99, "alla", "Mode", "Partner|Mamma|Pappa|Mor-/farförälder", "Jul|Födelsedag", "sak", "Mjuk och varm i många år.", "", "", ""),
    ("Smycke med initialer", 690, 15, 99, "kvinna", "Mode", "Partner|Mamma|Barn|Syskon", "alla", "personlig", "Halsband med valfria initialer.", "", "", ""),
    ("Roliga strumpor", 179, 5, 99, "alla", "Mode", "alla", "alla", "rolig", "Klassikern, fast roligare.", "", "", ""),
    ("Skivspelare", 2290, 18, 99, "alla", "Musik|Inredning", "Partner|Pappa|Mamma|Vän", "Jul|Födelsedag", "sak", "Retro med Bluetooth.", "", "", ""),
    ("Skrapkarta över världen", 299, 12, 99, "alla", "Resor", "alla", "alla", "rolig", "Skrapa fram länder du besökt.", "", "", ""),
    ("Porträtt av husdjuret", 599, 12, 99, "alla", "Djur", "alla", "alla", "personlig", "Tecknat från ett foto.", "", "", ""),
    ("Experimentlåda", 349, 6, 14, "alla", "Kreativt|Teknik", "Barn|Syskon", "Jul|Födelsedag", "sak", "20 roliga experiment.", "", "", ""),
    ("Byggsats robot", 599, 8, 16, "alla", "Teknik|Gaming", "Barn|Syskon", "Jul|Födelsedag", "sak", "Bygg och programmera.", "", "", ""),
    ("Gosedjur med namn", 299, 0, 8, "alla", "Djur", "Barn", "Jul|Födelsedag", "personlig", "Med barnets namn.", "", "", ""),
    ("Choklad från chokladeri", 199, 10, 99, "alla", "Matlagning|Kaffe & te", "alla", "alla", "sak", "Säkert kort som tack.", "", "", ""),
]

INTRESSEN = sorted({i for p in P for i in p[5].split("|")})
MOTTAGARE = ["Partner", "Mamma", "Pappa", "Syskon", "Vän", "Kollega", "Barn", "Mor-/farförälder", "Svärförälder"]
TILLFALLEN = ["Jul", "Födelsedag", "Alla hjärtans dag", "Mors dag", "Fars dag", "Student", "Inflyttning"]
BUDGET = {"Under 200 kr": (0, 200), "200–500 kr": (200, 500), "500–1 000 kr": (500, 1000),
          "1 000–2 000 kr": (1000, 2000), "Över 2 000 kr": (2000, 99999), "Spelar ingen roll": (0, 99999)}

# Färgpar för presentpaketen: (paket, snöre)
FARGER = [("#9b1c1c", "#d4af5a"), ("#1f4d3a", "#c8312b"), ("#f3ece0", "#9b1c1c"),
          ("#c8a24a", "#1f4d3a"), ("#1f4d3a", "#d4af5a"), ("#9b1c1c", "#f3ece0")]


def present(storlek=64, paket="#9b1c1c", snore="#d4af5a"):
    """Ritar ett minimalistiskt presentpaket som SVG."""
    return f"""<svg width="{storlek}" height="{storlek}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <path d="M32 18 C24 6 12 10 18 17 C21 20 28 19 32 18 Z" fill="none" stroke="{snore}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M32 18 C40 6 52 10 46 17 C43 20 36 19 32 18 Z" fill="none" stroke="{snore}" stroke-width="2.5" stroke-linejoin="round"/>
  <rect x="10" y="18" width="44" height="11" rx="2" fill="{paket}"/>
  <rect x="13" y="29" width="38" height="27" rx="2" fill="{paket}"/>
  <rect x="13" y="29" width="38" height="3" fill="#000" opacity=".12"/>
  <rect x="28.5" y="18" width="7" height="38" fill="{snore}"/>
  <circle cx="32" cy="18" r="3.2" fill="{snore}"/>
</svg>"""


def html(text):
    """Slår ihop HTML till en rad så att Streamlits markdown inte tolkar tomrader eller indrag."""
    return "".join(rad.strip() for rad in text.splitlines())


def poang(p, s):
    namn, pris, amin, amax, kon, intr, mott, till, typ, besk, url, butik, bild = p
    if not (s["bmin"] <= pris <= s["bmax"]) or not (amin <= s["alder"] <= amax):
        return None
    if s["kon"] != "Spelar ingen roll" and kon != "alla" and kon != s["kon"].lower():
        return None
    traffar = [i for i in intr.split("|") if i in s["intressen"]]
    sc = 4 * len(traffar) - (3 if s["intressen"] and not traffar else 0)
    sc += 3 if s["mottagare"] in mott.split("|") else (1 if mott == "alla" else 0)
    sc += 2 if s["tillfalle"] in till.split("|") else (1 if till == "alla" else 0)
    sc += 1.5 * pris / s["bmax"] if s["bmax"] < 99999 else 0
    return sc, traffar


# ---------- Utseende: minimalistisk jul ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500&display=swap');
#MainMenu, header, footer {visibility: hidden;}
.stApp {background: #faf6ef; color: #1e2a24;}
html, body, [class*="css"], .stApp p, .stApp label, .stApp span, .stApp div {font-family: 'Inter', sans-serif;}
.block-container {padding-top: 3rem; max-width: 780px;}

.topp {text-align: center; margin-bottom: 2.2rem;}
.topp h1 {font-family: 'Cormorant Garamond', serif !important; font-weight: 600; font-size: 3.2rem;
          letter-spacing: .02em; color: #1e2a24; margin: .6rem 0 0; padding: 0;}
.topp p {color: #7a7068; font-size: 1rem; margin: .3rem 0 0; letter-spacing: .04em;}
.linje {display: flex; align-items: center; justify-content: center; gap: .8rem; margin: 1.2rem auto 0; color: #c8a24a;}
.linje::before, .linje::after {content: ""; width: 70px; height: 1px; background: #c8a24a; opacity: .6;}

[data-testid="stForm"] {background: #ffffff; border: 1px solid #ebe2d4; border-radius: 18px;
                        padding: 1.8rem 1.8rem 1.4rem; box-shadow: 0 12px 34px -26px rgba(60,30,10,.45);}
.stApp label p {font-size: .78rem !important; text-transform: uppercase; letter-spacing: .1em; color: #7a7068 !important;}
[data-baseweb="select"] > div {background: #faf6ef; border: 1px solid #e4d9c8; border-radius: 10px;}
[data-baseweb="tag"] {background: #1f4d3a !important; border-radius: 99px !important;}
[data-testid="stSlider"] [role="slider"] {background: #9b1c1c; box-shadow: none;}
[data-testid="stSlider"] div[data-testid="stThumbValue"] {color: #9b1c1c;}

[data-testid="stBaseButton-pills"] {background: #faf6ef; border: 1px solid #e4d9c8; color: #1e2a24;
        border-radius: 99px; padding: .3rem .95rem;}
[data-testid="stBaseButton-pills"]:hover {border-color: #9b1c1c; color: #9b1c1c;}
[data-testid="stBaseButton-pillsActive"] {background: #1f4d3a !important; border: 1px solid #1f4d3a !important;
        color: #fff !important; border-radius: 99px; padding: .3rem .95rem;}
[data-testid="stBaseButton-pillsActive"] p {color: #fff !important;}
.stButton button, [data-testid="stFormSubmitButton"] button {background: #9b1c1c; color: #fff; border: 0;
        border-radius: 99px; padding: .65rem 2.2rem; font-weight: 500; letter-spacing: .05em; width: 100%;}
[data-testid="stFormSubmitButton"] button:hover {background: #7d1414; color: #fff;}

.kort {background: #fff; border: 1px solid #ebe2d4; border-radius: 16px; padding: 1.3rem 1.1rem 1rem;
       text-align: center; margin-bottom: 1rem; height: 100%;}
.kort h4 {font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; font-weight: 600; margin: .5rem 0 .2rem; color: #1e2a24;}
.kort .besk {color: #7a7068; font-size: .88rem; min-height: 2.6em; margin: 0;}
.kort .pris {color: #9b1c1c; font-weight: 500; margin: .6rem 0 .2rem;}
.kort .match {color: #1f4d3a; font-size: .78rem; letter-spacing: .03em;}
.kort a {display: inline-block; margin-top: .7rem; padding: .45rem 1.3rem; border: 1px solid #1e2a24;
         border-radius: 99px; color: #1e2a24 !important; text-decoration: none; font-size: .85rem;}
.kort a:hover {background: #1e2a24; color: #fff !important;}
.rubrik {font-family: 'Cormorant Garamond', serif; font-size: 2rem; text-align: center; margin: 2.4rem 0 1.2rem; color: #1e2a24;}
.reklam {text-align: center; color: #a39a90; font-size: .75rem; margin-top: 2rem;}
.kort img.bild {width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 10px; background: #f3ece0;}
.kort .butik {color: #a39a90; font-weight: 400; font-size: .85rem;}
.rutnat {display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 1rem;}
.rutnat .kort {margin-bottom: 0;}

/* ---------- Mobil ---------- */
@media (max-width: 640px) {
  .block-container {padding: 1.4rem .9rem 2rem !important;}
  .topp {margin-bottom: 1.4rem;}
  .topp svg {width: 64px; height: 64px;}
  .topp h1 {font-size: 2.4rem;}
  .topp p {font-size: .9rem;}
  [data-testid="stForm"] {padding: 1.2rem 1rem 1rem; border-radius: 14px;}
  [data-baseweb="select"] input, [data-baseweb="select"] div {font-size: 16px !important;}  /* hindrar iPhone från att zooma */
  [data-testid="stBaseButton-pills"], [data-testid="stBaseButton-pillsActive"] {padding: .45rem 1rem; min-height: 40px;}
  [data-testid="stFormSubmitButton"] button {padding: .85rem 1rem; font-size: 1rem;}
  .rubrik {font-size: 1.6rem; margin: 1.8rem 0 1rem;}
  .rutnat {grid-template-columns: 1fr 1fr; gap: .7rem;}
  .kort {padding: 1rem .7rem .9rem; border-radius: 14px;}
  .kort svg {width: 44px; height: 44px;}
  .kort img.bild {border-radius: 8px;}
  .kort h4 {font-size: 1.12rem;}
  .kort .besk {font-size: .8rem;}
  .kort a {display: block; padding: .6rem .5rem; font-size: .85rem;}
}
@media (max-width: 380px) {
  .rutnat {grid-template-columns: 1fr;}
}
</style>
""", unsafe_allow_html=True)

st.markdown(html(f"""
<div class="topp">
  {present(84)}
  <h1>Presenttipset</h1>
  <p>Årets julklappar, utvalda på trettio sekunder</p>
  <div class="linje">✦</div>
</div>
"""), unsafe_allow_html=True)

with st.form("fragor"):
    c1, c2 = st.columns(2)
    mottagare = c1.selectbox("Till vem", MOTTAGARE)
    tillfalle = c2.selectbox("Tillfälle", TILLFALLEN)
    budget = c1.selectbox("Budget", list(BUDGET), index=2)
    kon = c2.selectbox("Kön", ["Spelar ingen roll", "Kvinna", "Man"])
    alder = st.slider("Ålder", 0, 100, 35)
    intressen = st.pills("Intressen", INTRESSEN, selection_mode="multi") or []
    skicka = st.form_submit_button("Hitta presenter")

if skicka:
    s = {"mottagare": mottagare, "alder": alder, "tillfalle": tillfalle, "kon": kon,
         "intressen": intressen, "bmin": BUDGET[budget][0], "bmax": BUDGET[budget][1]}
    res = [(r, p) for p in P if (r := poang(p, s))]
    res.sort(key=lambda x: x[0][0], reverse=True)
    bra = [x for x in res if x[0][0] >= 4]
    res = (bra if len(bra) >= 3 else res[:6])[:12]

    if not res:
        st.info("Inga träffar. Prova en annan budget.")
    else:
        st.markdown(f'<div class="rubrik">{len(res)} förslag till {mottagare.lower()}</div>',
                    unsafe_allow_html=True)
        kort = []
        for i, ((sc, traffar), p) in enumerate(res):
            namn, pris, *_, besk, url, butik, bild = p
            paket, snore = FARGER[i % len(FARGER)]
            lank = url or "https://www.google.com/search?tbm=shop&q=" + quote_plus(namn)
            match = f'<div class="match">Matchar {", ".join(traffar).lower()}</div>' if traffar else ""
            kort.append(f"""
<div class="kort">
  {f'<img class="bild" src="{bild}" alt="{namn}">' if bild else present(56, paket, snore)}
  <h4>{namn}</h4>
  <p class="besk">{besk}</p>
  <div class="pris">{format(pris, ",").replace(",", " ")} kr{f'<span class="butik"> · {butik}</span>' if butik else ""}</div>
  {match}
  <a href="{lank}" target="_blank" rel="sponsored noopener">Se presenten</a>
</div>""")
        # Ett rutnät som anpassar antalet kolumner efter skärmen och behåller ordningen på mobilen
        st.markdown(html('<div class="rutnat">' + "".join(kort) + "</div>"), unsafe_allow_html=True)

st.markdown('<div class="reklam">Reklamlänkar · Presenttipset kan få provision när du handlar via länkarna</div>',
            unsafe_allow_html=True)
