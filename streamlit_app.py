import streamlit as st
from urllib.parse import quote_plus

st.set_page_config(page_title="Presenttipset", page_icon="🎁", layout="wide")

# Produkt: namn, emoji, pris, minålder, maxålder, kön, intressen, mottagare, tillfällen, typ, beskrivning, affiliatelänk
P = [
    ("Gjutjärnsgryta", "🍲", 899, 25, 99, "alla", "Matlagning", "Partner|Mamma|Pappa|Svärförälder", "Jul|Födelsedag|Inflyttning", "sak", "Håller livet ut, perfekt för långkok.", ""),
    ("Japansk kockkniv", "🔪", 1290, 25, 99, "alla", "Matlagning", "Partner|Pappa|Vän", "Jul|Födelsedag|Fars dag", "sak", "Rakbladsvass och rolig att laga mat med.", ""),
    ("Matlagningskurs för två", "👩‍🍳", 1695, 20, 80, "alla", "Matlagning|Dryck", "Partner|Mamma|Pappa|Vän", "alla", "upplevelse", "Lär er ett nytt kök tillsammans.", ""),
    ("Surdegskit", "🍞", 299, 18, 99, "alla", "Matlagning", "alla", "alla", "sak", "Jäskorg, degskrapa och surdegsgrund.", ""),
    ("Handkvarn för kaffe", "☕", 599, 20, 99, "alla", "Kaffe & te", "alla", "alla", "sak", "Nymalet kaffe varje morgon.", ""),
    ("Teprovning-ask", "🍵", 279, 16, 99, "alla", "Kaffe & te|Avkoppling", "alla", "alla", "sak", "24 sorters te i fin ask.", ""),
    ("Whiskyprovning", "🥃", 795, 20, 99, "alla", "Dryck", "Pappa|Partner|Vän|Svärförälder", "Födelsedag|Fars dag|Jul", "upplevelse", "Guidad provning med expert.", ""),
    ("Smart träningsklocka", "⌚", 2490, 15, 75, "alla", "Träning|Teknik", "Partner|Barn|Syskon|Mamma|Pappa", "Jul|Födelsedag|Student", "sak", "Puls, GPS och sömnanalys.", ""),
    ("Massagepistol", "💪", 999, 18, 80, "alla", "Träning|Avkoppling", "alla", "alla", "sak", "Mjukar upp stela muskler.", ""),
    ("Pannlampa 1000 lumen", "🔦", 399, 12, 99, "alla", "Friluftsliv|Träning", "alla", "alla", "sak", "Stark och laddbar.", ""),
    ("Övernattning i trädkoja", "🌲", 3490, 18, 80, "alla", "Friluftsliv|Resor|Avkoppling", "Partner|Mamma|Pappa", "Födelsedag|Alla hjärtans dag|Jul", "upplevelse", "En natt i naturen för två.", ""),
    ("Brusreducerande hörlurar", "🎧", 1990, 12, 80, "alla", "Teknik|Musik|Resor", "alla", "Jul|Födelsedag|Student", "sak", "Stäng ute världen.", ""),
    ("Bluetooth-högtalare", "🔊", 799, 10, 70, "alla", "Musik|Teknik|Friluftsliv", "alla", "alla", "sak", "Vattentålig, för bryggan och duschen.", ""),
    ("Gaming-headset", "🎮", 899, 10, 45, "alla", "Gaming|Teknik", "Barn|Syskon|Partner|Vän", "Jul|Födelsedag", "sak", "Tydligt ljud och mikrofon.", ""),
    ("Digital fotoram", "🖼️", 1290, 40, 99, "alla", "Teknik|Inredning", "Mor-/farförälder|Mamma|Pappa|Svärförälder", "Jul|Födelsedag|Mors dag|Fars dag", "personlig", "Skicka bilder direkt från mobilen.", ""),
    ("Escape room", "🔐", 1200, 12, 70, "alla", "Spel & pussel|Gaming", "Vän|Syskon|Kollega|Barn", "Födelsedag|Student", "upplevelse", "60 minuter att ta sig ut.", ""),
    ("E-boksläsare", "📚", 1590, 12, 99, "alla", "Läsning|Resor", "alla", "Jul|Födelsedag|Student", "sak", "Tusentals böcker i fickan.", ""),
    ("Ljudbokprenumeration", "🎙️", 507, 12, 99, "alla", "Läsning|Avkoppling", "alla", "alla", "upplevelse", "Obegränsat i tre månader.", ""),
    ("Pussel 1000 bitar", "🧩", 229, 10, 99, "alla", "Spel & pussel|Avkoppling", "alla", "alla", "sak", "Mysigt pussel med vackert motiv.", ""),
    ("Sällskapsspel", "🎲", 349, 16, 80, "alla", "Spel & pussel", "alla", "alla", "rolig", "Garanterade skratt.", ""),
    ("Akvarellkit", "🎨", 449, 10, 99, "alla", "Kreativt", "alla", "alla", "sak", "Kom igång direkt.", ""),
    ("Keramikkurs", "🏺", 995, 16, 80, "alla", "Kreativt|Inredning", "Partner|Mamma|Syskon|Vän", "Födelsedag|Mors dag|Jul", "upplevelse", "Dreja din egen kopp.", ""),
    ("Doftljus", "🕯️", 299, 16, 99, "alla", "Inredning|Avkoppling", "alla", "alla", "sak", "Mysigt för vinterkvällar.", ""),
    ("Tyngdtäcke", "🛌", 1290, 15, 99, "alla", "Avkoppling", "Partner|Mamma|Pappa|Syskon|Barn", "Jul|Födelsedag", "sak", "Hjälper många att sova bättre.", ""),
    ("Spa-dag för två", "🧖", 2390, 18, 90, "alla", "Avkoppling|Skönhet", "Partner|Mamma|Syskon|Vän", "alla", "upplevelse", "En hel dag av lugn.", ""),
    ("Inomhusodling med LED", "🌱", 899, 18, 99, "alla", "Odling|Matlagning", "alla", "alla", "sak", "Färska örter året runt.", ""),
    ("Stjärnkarta", "✨", 449, 16, 99, "alla", "Inredning", "Partner|Barn|Mamma|Pappa", "Alla hjärtans dag|Födelsedag|Jul", "personlig", "Himlen från er speciella dag.", ""),
    ("Hudvårdsset", "🧴", 549, 16, 90, "kvinna", "Skönhet", "Partner|Mamma|Syskon|Vän", "alla", "sak", "Rengöring, serum och kräm.", ""),
    ("Skäggvårdskit", "🧔", 399, 18, 90, "man", "Skönhet|Mode", "Partner|Pappa|Syskon|Vän", "alla", "sak", "Olja, balm och kam.", ""),
    ("Kashmirhalsduk", "🧣", 1190, 20, 99, "alla", "Mode", "Partner|Mamma|Pappa|Mor-/farförälder", "Jul|Födelsedag", "sak", "Mjuk och varm i många år.", ""),
    ("Smycke med initialer", "💍", 690, 15, 99, "kvinna", "Mode", "Partner|Mamma|Barn|Syskon", "alla", "personlig", "Halsband med valfria initialer.", ""),
    ("Roliga strumpor", "🧦", 179, 5, 99, "alla", "Mode", "alla", "alla", "rolig", "Klassikern, fast roligare.", ""),
    ("Skivspelare", "💿", 2290, 18, 99, "alla", "Musik|Inredning", "Partner|Pappa|Mamma|Vän", "Jul|Födelsedag", "sak", "Retro med Bluetooth.", ""),
    ("Skrapkarta över världen", "🗺️", 299, 12, 99, "alla", "Resor", "alla", "alla", "rolig", "Skrapa fram länder du besökt.", ""),
    ("Porträtt av husdjuret", "🐶", 599, 12, 99, "alla", "Djur", "alla", "alla", "personlig", "Tecknat från ett foto.", ""),
    ("Experimentlåda", "🧪", 349, 6, 14, "alla", "Kreativt|Teknik", "Barn|Syskon", "Jul|Födelsedag", "sak", "20 roliga experiment.", ""),
    ("Byggsats robot", "🤖", 599, 8, 16, "alla", "Teknik|Gaming", "Barn|Syskon", "Jul|Födelsedag", "sak", "Bygg och programmera.", ""),
    ("Gosedjur med namn", "🧸", 299, 0, 8, "alla", "Djur", "Barn", "Jul|Födelsedag", "personlig", "Med barnets namn.", ""),
    ("Choklad från chokladeri", "🍫", 199, 10, 99, "alla", "Matlagning|Kaffe & te", "alla", "alla", "sak", "Säkert kort som tack.", ""),
]

INTRESSEN = sorted({i for p in P for i in p[6].split("|")})
MOTTAGARE = ["Partner", "Mamma", "Pappa", "Syskon", "Vän", "Kollega", "Barn", "Mor-/farförälder", "Svärförälder"]
TILLFALLEN = ["Jul", "Födelsedag", "Alla hjärtans dag", "Mors dag", "Fars dag", "Student", "Inflyttning"]
BUDGET = {"Under 200 kr": (0, 200), "200–500 kr": (200, 500), "500–1 000 kr": (500, 1000),
          "1 000–2 000 kr": (1000, 2000), "Över 2 000 kr": (2000, 99999), "Spelar ingen roll": (0, 99999)}


def poang(p, s):
    namn, em, pris, amin, amax, kon, intr, mott, till, typ, besk, url = p
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


st.title("🎁 Presenttipset")
st.write("Svara på några snabba frågor så hittar vi den perfekta presenten.")

with st.form("fragor"):
    c1, c2, c3 = st.columns(3)
    mottagare = c1.selectbox("Vem är presenten till?", MOTTAGARE)
    alder = c1.slider("Ålder", 0, 100, 35)
    tillfalle = c2.selectbox("Tillfälle", TILLFALLEN)
    kon = c2.radio("Kön", ["Spelar ingen roll", "Kvinna", "Man"], horizontal=True)
    budget = c3.selectbox("Budget", list(BUDGET), index=2)
    intressen = st.multiselect("Vad gillar hen? (välj 1–3)", INTRESSEN)
    skicka = st.form_submit_button("🔎 Hitta presenter", type="primary")

if skicka:
    s = {"mottagare": mottagare, "alder": alder, "tillfalle": tillfalle, "kon": kon,
         "intressen": intressen, "bmin": BUDGET[budget][0], "bmax": BUDGET[budget][1]}
    res = [(r, p) for p in P if (r := poang(p, s))]
    res.sort(key=lambda x: x[0][0], reverse=True)
    bra = [x for x in res if x[0][0] >= 4]
    res = (bra if len(bra) >= 3 else res[:6])[:12]

    if not res:
        st.warning("Inga träffar. Prova en annan budget.")
    else:
        st.subheader(f"{len(res)} presenttips till {mottagare.lower()}, {alder} år")
        cols = st.columns(3)
        for i, ((sc, traffar), p) in enumerate(res):
            namn, em, pris, *_, besk, url = p
            with cols[i % 3].container(border=True):
                st.markdown(f"<div style='font-size:3rem;text-align:center'>{em}</div>", unsafe_allow_html=True)
                st.markdown(f"**{namn}**")
                st.caption(besk)
                st.markdown(f"**{pris} kr**")
                if traffar:
                    st.caption("✓ Matchar: " + ", ".join(traffar))
                lank = url or "https://www.google.com/search?tbm=shop&q=" + quote_plus(namn)
                st.link_button("Se presenten →", lank, use_container_width=True)
    st.caption("Reklamlänkar: Presenttipset kan få provision när du handlar via länkarna.")
