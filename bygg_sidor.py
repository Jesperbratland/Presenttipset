"""
Bygger SEO-sidor för Presenttipset.

Skapar vanliga HTML-sidor i mappen docs/ som Google kan läsa, t.ex.
  /julklapp-till-pappa/   /julklapp-under-500-kr/   /present-till-skidakare/
Sidorna publiceras gratis med GitHub Pages (Settings → Pages → Branch: main, mapp: /docs).

Kör:  python bygg_sidor.py
Kör skriptet igen varje gång produkter.py ändras, så uppdateras sidorna.
"""

import html
import json
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus

from produkter import PRODUKTER

# ---------- Inställningar ----------
BAS_URL = "https://jesperbratland.github.io/Presenttipset"   # byt när du har egen domän, t.ex. https://presenttipset.se
APP_URL = "https://presenttipset.streamlit.app"              # länk till frågeappen i Streamlit
AR = date.today().year                                      # årtalet i rubrikerna, t.ex. "Julklapp till pappa 2026"
UT = Path(__file__).parent / "docs"

# ---------- Sidorna ----------
# typ: "mottagare", "intresse" eller "budget". alder = typisk ålder för mottagaren.
SIDOR = [
    # Mottagare
    {"slug": "julklapp-till-pappa", "typ": "mottagare", "varde": "Pappa", "alder": 60,
     "h1": "Julklapp till pappa", "kort": "pappa",
     "intro": "Pappor är kända för att säga att de inte önskar sig något. Här är julklappar som faktiskt används – "
              "från bra köksprylar till upplevelser han inte skulle köpa åt sig själv."},
    {"slug": "julklapp-till-mamma", "typ": "mottagare", "varde": "Mamma", "alder": 58,
     "h1": "Julklapp till mamma", "kort": "mamma",
     "intro": "Mamma förtjänar något genomtänkt. Vi har samlat julklappar som ger både mys, egen tid och minnen – "
              "i olika prisklasser."},
    {"slug": "julklapp-till-partner", "typ": "mottagare", "varde": "Partner", "alder": 35,
     "h1": "Julklapp till partner", "kort": "din partner",
     "intro": "Letar du julklapp till flickvän, pojkvän, fru eller man? Här är personliga presenter och upplevelser "
              "ni kan göra tillsammans."},
    {"slug": "julklapp-till-barn", "typ": "mottagare", "varde": "Barn", "alder": 9,
     "h1": "Julklapp till barn", "kort": "barn",
     "intro": "Julklappar till barn som håller längre än till annandagen – kreativa, roliga och lärorika presenter "
              "för skolbarn."},
    {"slug": "julklapp-till-mormor-morfar", "typ": "mottagare", "varde": "Mor-/farförälder", "alder": 75,
     "h1": "Julklapp till mormor, morfar, farmor och farfar", "kort": "mor- och farföräldrar",
     "intro": "Mor- och farföräldrar har ofta allt de behöver. Satsa på minnen, mys och sådant som för familjen närmare."},
    {"slug": "julklapp-till-van", "typ": "mottagare", "varde": "Vän", "alder": 32,
     "h1": "Julklapp till en vän", "kort": "en vän",
     "intro": "Julklappar till kompisen – från roliga småsaker till upplevelser ni kan göra tillsammans."},
    {"slug": "julklapp-till-kollega", "typ": "mottagare", "varde": "Kollega", "alder": 40,
     "h1": "Julklapp till kollega", "kort": "en kollega",
     "intro": "Julklappsspel på jobbet eller en tack-present till kollegan? Här är säkra kort som passar de flesta."},
    {"slug": "julklapp-till-svarmor-svarfar", "typ": "mottagare", "varde": "Svärförälder", "alder": 60,
     "h1": "Julklapp till svärmor och svärfar", "kort": "svärföräldrar",
     "intro": "Svärföräldrar kan vara knepiga att köpa till. De här julklapparna är genomtänkta utan att vara för personliga."},

    # Budget
    {"slug": "julklapp-under-200-kr", "typ": "budget", "varde": 200,
     "h1": "Julklapp under 200 kr", "kort": "under 200 kr",
     "intro": "Billiga julklappar som inte känns billiga. Perfekt till julklappsspel, kollegor och strumpfyllning."},
    {"slug": "julklapp-under-500-kr", "typ": "budget", "varde": 500,
     "h1": "Julklapp under 500 kr", "kort": "under 500 kr",
     "intro": "Den vanligaste julklappsbudgeten – här är presenter under 500 kronor som känns genomtänkta."},
    {"slug": "julklapp-under-1000-kr", "typ": "budget", "varde": 1000,
     "h1": "Julklapp under 1000 kr", "kort": "under 1000 kr",
     "intro": "Lite större julklappar till de närmaste – kvalitet och upplevelser under tusenlappen."},

    # Intressen
    {"slug": "present-till-skidakare", "typ": "intresse", "varde": "Vintersport",
     "h1": "Present till skidåkare", "kort": "skidåkare",
     "intro": "Julklappar till den som längtar till fjällen. Prylar som gör skiddagen bekvämare – och återhämtningen efteråt."},
    {"slug": "present-till-kaffealskare", "typ": "intresse", "varde": "Kaffe & te",
     "h1": "Present till kaffeälskare", "kort": "kaffeälskare",
     "intro": "För den som tar sitt kaffe – eller te – på allvar. Presenter som gör morgonen lite bättre."},
    {"slug": "present-till-nagon-som-gillar-matlagning", "typ": "intresse", "varde": "Matlagning",
     "h1": "Present till någon som gillar matlagning", "kort": "matälskare",
     "intro": "Köksprylar och matupplevelser för hemmakocken som har det mesta men alltid vill ha mer."},
    {"slug": "present-till-gamer", "typ": "intresse", "varde": "Gaming",
     "h1": "Present till gamer", "kort": "gamers",
     "intro": "Julklappar till den som spelar – på PlayStation, Xbox, Switch eller dator."},
    {"slug": "present-till-nagon-som-tranar", "typ": "intresse", "varde": "Träning",
     "h1": "Present till någon som tränar", "kort": "träningsfantaster",
     "intro": "Presenter till löparen, gymråttan och yogautövaren – för både träning och återhämtning."},
    {"slug": "present-till-bokmal", "typ": "intresse", "varde": "Läsning",
     "h1": "Present till någon som gillar att läsa", "kort": "bokälskare",
     "intro": "Julklappar för bokmalen – för fler böcker, bättre läsmys och läsning på resande fot."},
    {"slug": "present-till-hundagare", "typ": "intresse", "varde": "Djur",
     "h1": "Present till hundägare och djurvänner", "kort": "djurvänner",
     "intro": "Presenter till den som älskar sin hund eller katt – personliga och roliga."},
    {"slug": "present-for-avkoppling", "typ": "intresse", "varde": "Avkoppling",
     "h1": "Present för avkoppling och mys", "kort": "den som behöver vila",
     "intro": "Julklappar som ger lugn, sömn och egentid. Perfekt till den som har haft ett stressigt år."},
    {"slug": "upplevelsepresent", "typ": "upplevelse", "varde": "upplevelse",
     "h1": "Upplevelsepresenter", "kort": "upplevelser",
     "intro": "Ge minnen i stället för saker. Upplevelsepresenter passar den som har allt – och tar ingen plats."},
]

# ---------- Urval ----------

def passar(p, sida):
    """Avgör om en produkt hör hemma på sidan och ger den en poäng för sorteringen."""
    mott, till, intr = p["mottagare"].split("|"), p["tillfallen"].split("|"), p["intressen"].split("|")
    if "Jul" not in till and "alla" not in till:
        return None
    sc = 0
    if sida["typ"] == "mottagare":
        if not (p["alder_min"] <= sida["alder"] <= p["alder_max"]):
            return None
        if sida["varde"] in mott:
            sc += 3
        elif "alla" in mott:
            sc += 1
        else:
            return None
    elif sida["typ"] == "budget":
        if p["pris"] > sida["varde"]:
            return None
        sc += p["pris"] / sida["varde"]
    elif sida["typ"] == "intresse":
        if sida["varde"] not in intr:
            return None
        sc += 3 - intr.index(sida["varde"]) * 0.5
    elif sida["typ"] == "upplevelse":
        if p["typ"] != "upplevelse":
            return None
    if p["lank"]:
        sc += 5   # riktiga produkter med länk först
    return sc


def urval(sida, max_antal=12):
    lista = [(s, p) for p in PRODUKTER if (s := passar(p, sida)) is not None]
    lista.sort(key=lambda x: (-x[0], x[1]["pris"]))
    return [p for _, p in lista[:max_antal]]

# ---------- HTML ----------

FARGER = [("#9b1c1c", "#d4af5a"), ("#1f4d3a", "#c8312b"), ("#f3ece0", "#9b1c1c"),
          ("#c8a24a", "#1f4d3a"), ("#1f4d3a", "#d4af5a"), ("#9b1c1c", "#f3ece0")]


def present(storlek=64, paket="#9b1c1c", snore="#d4af5a"):
    return (f'<svg width="{storlek}" height="{storlek}" viewBox="0 0 64 64" aria-hidden="true">'
            f'<path d="M32 18 C24 6 12 10 18 17 C21 20 28 19 32 18 Z" fill="none" stroke="{snore}" stroke-width="2.5"/>'
            f'<path d="M32 18 C40 6 52 10 46 17 C43 20 36 19 32 18 Z" fill="none" stroke="{snore}" stroke-width="2.5"/>'
            f'<rect x="10" y="18" width="44" height="11" rx="2" fill="{paket}"/>'
            f'<rect x="13" y="29" width="38" height="27" rx="2" fill="{paket}"/>'
            f'<rect x="13" y="29" width="38" height="3" fill="#000" opacity=".12"/>'
            f'<rect x="28.5" y="18" width="7" height="38" fill="{snore}"/>'
            f'<circle cx="32" cy="18" r="3.2" fill="{snore}"/></svg>')


CSS = """
:root{--bg:#faf6ef;--ink:#1e2a24;--muted:#7a7068;--line:#ebe2d4;--red:#9b1c1c;--green:#1f4d3a;--gold:#c8a24a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif}
a{color:inherit}.wrap{max-width:980px;margin:0 auto;padding:0 18px}
.top{display:flex;align-items:center;justify-content:space-between;padding:18px 0}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font:600 1.5rem 'Cormorant Garamond',serif}
.cta{background:var(--red);color:#fff;text-decoration:none;padding:.55rem 1.2rem;border-radius:99px;font-size:.9rem}
.hero{text-align:center;padding:30px 0 10px}
h1{font:600 clamp(2.2rem,6vw,3.4rem)/1.1 'Cormorant Garamond',serif;margin:0 0 .6rem}
.hero p{color:var(--muted);max-width:640px;margin:0 auto}
.linje{display:flex;justify-content:center;align-items:center;gap:.8rem;color:var(--gold);margin:1.4rem 0}
.linje:before,.linje:after{content:"";width:70px;height:1px;background:var(--gold);opacity:.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:10px 0 30px}
.kort{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 14px;text-align:center;display:flex;flex-direction:column}
.kort svg{margin:0 auto}
.kort img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;background:#f3ece0}
.kort h2,.kort h3{font:600 1.3rem 'Cormorant Garamond',serif;margin:.5rem 0 .2rem}
.kort p{color:var(--muted);font-size:.9rem;margin:0;flex:1}
.pris{color:var(--red);font-weight:500;margin:.6rem 0 .2rem}.pris span{color:#a39a90;font-weight:400;font-size:.85rem}
.kort a.kop{margin-top:.6rem;padding:.5rem 1rem;border:1px solid var(--ink);border-radius:99px;text-decoration:none;font-size:.88rem}
.kort a.kop:hover{background:var(--ink);color:#fff}
.box{background:#fff;border:1px solid var(--line);border-radius:18px;padding:26px;text-align:center;margin:20px 0 34px}
.box h2{font:600 1.8rem 'Cormorant Garamond',serif;margin:0 0 .3rem}.box p{color:var(--muted);margin:0 0 1rem}
.box .cta{display:inline-block;padding:.8rem 2rem;font-size:1rem}
.text h2{font:600 1.7rem 'Cormorant Garamond',serif;margin:1.6rem 0 .4rem}.text{max-width:720px;margin:0 auto}
.lankar{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:12px 0 30px}
.lankar a{background:#fff;border:1px solid var(--line);padding:.4rem .9rem;border-radius:99px;text-decoration:none;font-size:.88rem}
.lankar a:hover{border-color:var(--red);color:var(--red)}
footer{text-align:center;color:#a39a90;font-size:.8rem;padding:30px 0 40px}
@media(max-width:600px){.grid{grid-template-columns:1fr 1fr;gap:10px}.kort{padding:12px 9px}.kort h2,.kort h3{font-size:1.1rem}
.kort p{font-size:.8rem}.top .cta{font-size:.8rem;padding:.45rem .9rem}}
"""


def sida_html(titel, beskrivning, kanonisk, kropp, schema):
    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(beskrivning)}">
<link rel="canonical" href="{kanonisk}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(titel)}">
<meta property="og:description" content="{html.escape(beskrivning)}">
<meta property="og:url" content="{kanonisk}">
<meta property="og:locale" content="sv_SE">
<link rel="icon" href="data:image/svg+xml,{quote_plus(present(64)).replace('+', '%20')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="logo" href="{BAS_URL}/">{present(34)} Presenttipset</a>
  <a class="cta" href="{APP_URL}">Hitta presenten</a>
</header>
{kropp}
<footer>Reklamlänkar: Presenttipset kan få provision när du handlar via länkarna. Det kostar inget extra för dig.<br>
Priser kan ändras – kontrollera alltid aktuellt pris hos butiken. © {date.today().year} Presenttipset</footer>
</div>
</body>
</html>
"""


def produktkort(p, i, rubriknivå="h3"):
    lank = p["lank"] or "https://www.google.com/search?tbm=shop&q=" + quote_plus(p["namn"])
    paket, snore = FARGER[i % len(FARGER)]
    bild = (f'<img src="{html.escape(p["bild"])}" alt="{html.escape(p["namn"])}" loading="lazy">'
            if p["bild"] else present(56, paket, snore))
    butik = f' <span>· {html.escape(p["butik"])}</span>' if p["butik"] else ""
    pris = format(p["pris"], ",").replace(",", " ")
    return (f'<article class="kort">{bild}<{rubriknivå}>{html.escape(p["namn"])}</{rubriknivå}>'
            f'<p>{html.escape(p["beskrivning"])}</p><div class="pris">{pris} kr{butik}</div>'
            f'<a class="kop" href="{html.escape(lank)}" target="_blank" rel="sponsored nofollow noopener">Se presenten</a></article>')


def aktiva_sidor():
    """Sidor med tillräckligt många produkter för att publiceras."""
    return [s for s in SIDOR if len(urval(s)) >= 4]


def lankrad(utom=None):
    return '<nav class="lankar">' + "".join(
        f'<a href="{BAS_URL}/{s["slug"]}/">{html.escape(s["h1"])}</a>' for s in aktiva_sidor() if s["slug"] != utom
    ) + "</nav>"


def faq(sida, produkter):
    billigast = min(produkter, key=lambda p: p["pris"])
    fragor = [
        (f"Vad är en bra julklapp till {sida['kort']}?",
         f"Populära val är {', '.join(p['namn'].lower() for p in produkter[:3])}. "
         f"Använd gärna vårt presenttest för förslag utifrån intressen och budget."),
        (f"Finns det billiga julklappar till {sida['kort']}?",
         f"Ja – till exempel {billigast['namn'].lower()} för cirka {billigast['pris']} kr."),
        ("Hur hittar jag en personlig present?",
         "Svara på några frågor om mottagarens ålder, intressen och din budget i presenttestet så får du skräddarsydda tips."),
    ]
    html_fragor = "".join(f"<h3>{html.escape(f)}</h3><p>{html.escape(s)}</p>" for f, s in fragor)
    schema = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f, "acceptedAnswer": {"@type": "Answer", "text": s}} for f, s in fragor]}
    return f'<section class="text"><h2>Vanliga frågor</h2>{html_fragor}</section>', schema


def bygg():
    if UT.exists():
        shutil.rmtree(UT)
    UT.mkdir()
    byggda = []

    for sida in SIDOR:
        produkter = urval(sida)
        if len(produkter) < 4:          # tunna sidor gör mer skada än nytta på Google
            print(f"Hoppar över {sida['slug']} – bara {len(produkter)} produkter")
            continue
        url = f"{BAS_URL}/{sida['slug']}/"
        titel = f"{sida['h1']} – {len(produkter)} tips {AR} | Presenttipset"
        beskrivning = (f"{sida['h1']}: {len(produkter)} utvalda presenttips {AR}, från "
                       f"{min(p['pris'] for p in produkter)} kr. {sida['intro'].split('.')[0]}.")[:158]
        faq_html, faq_schema = faq(sida, produkter)
        kropp = f"""
<section class="hero">
  <h1>{html.escape(sida['h1'])} {AR}</h1>
  <p>{html.escape(sida['intro'])}</p>
  <div class="linje">✦</div>
</section>
<section class="grid">{''.join(produktkort(p, i) for i, p in enumerate(produkter))}</section>
<section class="box">
  <h2>Hittade du inte rätt?</h2>
  <p>Svara på några snabba frågor så får du personliga tips på trettio sekunder.</p>
  <a class="cta" href="{APP_URL}">Starta presenttestet</a>
</section>
{faq_html}
<section class="text"><h2>Fler presenttips</h2></section>
{lankrad(sida['slug'])}
"""
        schema = {"@context": "https://schema.org", "@graph": [
            {"@type": "ItemList", "name": sida["h1"], "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": p["namn"]} for i, p in enumerate(produkter)]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Presenttipset", "item": f"{BAS_URL}/"},
                {"@type": "ListItem", "position": 2, "name": sida["h1"], "item": url}]},
            faq_schema]}
        mapp = UT / sida["slug"]
        mapp.mkdir()
        (mapp / "index.html").write_text(sida_html(titel, beskrivning, url, kropp, schema), encoding="utf-8")
        byggda.append((sida, len(produkter)))
        print(f"Byggde /{sida['slug']}/ ({len(produkter)} produkter)")

    # Startsida
    def grupp(typ, rubrik):
        lankar = "".join(f'<a href="{BAS_URL}/{s["slug"]}/">{html.escape(s["h1"])}</a>'
                         for s, _ in byggda if s["typ"] in typ)
        return f'<section class="text" style="text-align:center"><h2>{rubrik}</h2></section><nav class="lankar">{lankar}</nav>'

    populara = sorted(PRODUKTER, key=lambda p: (not p["lank"], -p["pris"] if p["typ"] == "upplevelse" else 0))[:8]
    kropp = f"""
<section class="hero">
  {present(84)}
  <h1>Julklappstips {AR}</h1>
  <p>Hitta den perfekta julklappen på trettio sekunder. Svara på några frågor om mottagaren – eller bläddra bland våra utvalda listor.</p>
  <div class="linje">✦</div>
</section>
<section class="box">
  <h2>Presenttestet</h2>
  <p>Ålder, intressen och budget – vi gör resten.</p>
  <a class="cta" href="{APP_URL}">Hitta presenten</a>
</section>
{grupp(["mottagare"], "Julklapp till …")}
{grupp(["budget"], "Julklapp efter budget")}
{grupp(["intresse", "upplevelse"], "Present efter intresse")}
<section class="text" style="text-align:center"><h2>Populära julklappar</h2></section>
<section class="grid">{''.join(produktkort(p, i) for i, p in enumerate(populara))}</section>
"""
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": "Presenttipset", "url": f"{BAS_URL}/",
              "inLanguage": "sv-SE"}
    (UT / "index.html").write_text(
        sida_html(f"Julklappstips {AR} – hitta den perfekta presenten | Presenttipset",
                  f"Julklappstips {AR} till pappa, mamma, partner, barn och kollegor. Svara på några frågor och få "
                  f"personliga presenttips efter intressen och budget.", f"{BAS_URL}/", kropp, schema),
        encoding="utf-8")

    # Sitemap, robots och .nojekyll (gör att GitHub Pages visar filerna som de är)
    idag = date.today().isoformat()
    urls = [f"{BAS_URL}/"] + [f"{BAS_URL}/{s['slug']}/" for s, _ in byggda]
    (UT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{idag}</lastmod></url>\n" for u in urls) + "</urlset>\n",
        encoding="utf-8")
    (UT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BAS_URL}/sitemap.xml\n", encoding="utf-8")
    (UT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Klart: {len(urls)} sidor i {UT}")


if __name__ == "__main__":
    bygg()
