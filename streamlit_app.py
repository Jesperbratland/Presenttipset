import re
from urllib.parse import quote_plus

import streamlit as st

from produkter import INTRESSEN, PRODUKTER, SYNONYMER

st.set_page_config(page_title="Presenttipset", page_icon=":material/redeem:", layout="centered")


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


STOPPORD = {"och", "till", "som", "med", "för", "gillar", "älskar", "tycker", "om", "hen", "han", "hon",
            "min", "mitt", "mina", "sin", "den", "det", "att", "väldigt", "mycket", "lite", "present"}


def ord_i(text):
    """Delar upp text i små bokstäver utan skiljetecken och utfyllnadsord."""
    return [o for o in re.split(r"[^a-zåäöéü0-9-]+", text.lower()) if len(o) >= 3 and o not in STOPPORD]


def liknar(a, b):
    """Två ord räknas som lika om det ena börjar med det andra (skidor ~ skidåkning, hund ~ hundar)."""
    kort, lang = sorted((a, b), key=len)
    return lang.startswith(kort) and len(kort) >= 3 or (len(kort) >= 5 and lang.startswith(kort[:5]))


def tolka_fritext(text):
    """Översätter fritext till intressen och sökord."""
    ord_lista = ord_i(text)
    intressen = {i for i, syn in SYNONYMER.items()
                 for o in ord_lista for s in ord_i(syn + " " + i) if liknar(o, s)}
    return ord_lista, intressen


def poang(p, s):
    """Poängsätter en produkt. None betyder att den inte passar alls."""
    if not (s["bmin"] <= p["pris"] <= s["bmax"]) or not (p["alder_min"] <= s["alder"] <= p["alder_max"]):
        return None
    if s["kon"] != "Spelar ingen roll" and p["kon"] not in ("alla", s["kon"].lower()):
        return None

    intr = p["intressen"].split("|")
    onskade = set(s["intressen"]) | s["fritext_intressen"]
    traffar = [i for i in intr if i in onskade]
    sc = 4 * len(traffar)
    if onskade and not traffar:
        sc -= 3

    # Fritext som träffar produktens namn, sökord eller beskrivning väger tyngst
    produktord = ord_i(" ".join([p["namn"], p["sokord"], p["beskrivning"]]))
    ordtraffar = [o for o in s["fritext_ord"] if any(liknar(o, w) for w in produktord)]
    sc += 6 * len(ordtraffar)

    mott, till = p["mottagare"].split("|"), p["tillfallen"].split("|")
    sc += 3 if s["mottagare"] in mott else (1 if "alla" in mott else 0)
    sc += 2 if s["tillfalle"] in till else (1 if "alla" in till else 0)
    if s["bmax"] < 99999:
        sc += 1.5 * p["pris"] / s["bmax"]
    return sc, traffar, ordtraffar


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
.rubrik.liten {font-size: 1.4rem; color: #7a7068; margin-top: 2rem;}
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

def visa_kort(lista, start=0):
    """Ritar produktkorten i ett rutnät som anpassar sig efter skärmen."""
    kort = []
    for i, ((sc, traffar, ordtraffar), p) in enumerate(lista, start=start):
        paket, snore = FARGER[i % len(FARGER)]
        lank = p["lank"] or "https://www.google.com/search?tbm=shop&q=" + quote_plus(p["namn"])
        visas = [t.lower() for t in traffar] + [o for o in ordtraffar if o not in " ".join(traffar).lower()]
        match = f'<div class="match">Matchar {", ".join(visas)}</div>' if visas else ""
        bild = (f'<img class="bild" src="{p["bild"]}" alt="{p["namn"]}">' if p["bild"]
                else present(56, paket, snore))
        butik = f'<span class="butik"> · {p["butik"]}</span>' if p["butik"] else ""
        pris = format(p["pris"], ",").replace(",", " ")
        kort.append(f"""
<div class="kort">
  {bild}
  <h4>{p["namn"]}</h4>
  <p class="besk">{p["beskrivning"]}</p>
  <div class="pris">{pris} kr{butik}</div>
  {match}
  <a href="{lank}" target="_blank" rel="sponsored noopener">Se presenten</a>
</div>""")
    st.markdown(html('<div class="rutnat">' + "".join(kort) + "</div>"), unsafe_allow_html=True)


with st.form("fragor"):
    fritext = st.text_input("Sök fritt", placeholder="T.ex. skidor, whisky, hund, gym …")
    c1, c2 = st.columns(2)
    mottagare = c1.selectbox("Till vem", MOTTAGARE)
    tillfalle = c2.selectbox("Tillfälle", TILLFALLEN)
    budget = c1.selectbox("Budget", list(BUDGET), index=2)
    kon = c2.selectbox("Kön", ["Spelar ingen roll", "Kvinna", "Man"])
    alder = st.slider("Ålder", 0, 100, 35)
    intressen = st.pills("Intressen", INTRESSEN, selection_mode="multi") or []
    skicka = st.form_submit_button("Hitta presenter")

if skicka:
    fritext_ord, fritext_intressen = tolka_fritext(fritext)
    s = {"mottagare": mottagare, "alder": alder, "tillfalle": tillfalle, "kon": kon,
         "intressen": intressen, "fritext_ord": fritext_ord, "fritext_intressen": fritext_intressen,
         "bmin": BUDGET[budget][0], "bmax": BUDGET[budget][1]}
    res = [(r, p) for p in PRODUKTER if (r := poang(p, s))]
    res.sort(key=lambda x: x[0][0], reverse=True)

    # Dela upp i det som matchar intressen/fritext och övriga förslag
    soker = bool(intressen or fritext_ord)
    traffade = [x for x in res if x[0][1] or x[0][2]] if soker else [x for x in res if x[0][0] >= 4]
    ovriga = [x for x in res if x not in traffade]
    traffade = traffade[:12]
    fler = ovriga[:max(0, 6 - len(traffade))]

    if not res:
        st.info("Inga träffar. Prova en annan budget eller ålder.")
    else:
        if traffade:
            st.markdown(f'<div class="rubrik">{len(traffade)} förslag till {mottagare.lower()}</div>',
                        unsafe_allow_html=True)
            visa_kort(traffade)
        else:
            sokt = fritext.strip() or ", ".join(intressen).lower()
            st.info(f"Vi hittade inget som matchar ”{sokt}” i den här budgeten.")
        if fler:
            st.markdown('<div class="rubrik liten">Fler idéer</div>', unsafe_allow_html=True)
            visa_kort(fler, start=len(traffade))

st.markdown('<div class="reklam">Reklamlänkar · Presenttipset kan få provision när du handlar via länkarna</div>',
            unsafe_allow_html=True)
