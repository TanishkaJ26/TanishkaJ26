"""Builds the README panels: header, section headers, BGPShield card, project cards, footer.

Run from the repo root:  python assets/gen_readme_svgs.py
The star map has its own generator (gen_starmap.py).
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"

INK = "#f1f5ff"      # primary text
INK2 = "#b8c2d9"     # body text
MUTED = "#6b7590"    # small print
LINE = "#232b40"     # borders and rules
BLUE, AMBER, TEAL = "#9cc2ff", "#ffd28a", "#8ff0d6"

BASE_CSS = f"""
    .pop {{ animation: pop .9s ease-out both; }}
    .rise {{ animation: rise 1s cubic-bezier(.2,.7,.2,1) both; }}
    .grow {{ transform-box: fill-box; transform-origin: left center; animation: grow 1.3s cubic-bezier(.2,.7,.2,1) both; }}
    .beacon {{ transform-box: fill-box; transform-origin: center; animation: beacon 2.4s ease-out infinite; }}
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
    @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @keyframes beacon {{ 0% {{ transform: scale(1); opacity: .9; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
"""
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def svg(w, h, title, desc, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  <defs>
    <linearGradient id="surface" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#111626"/><stop offset="1" stop-color="#0b0e18"/></linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  </defs>
  <style>{BASE_CSS}{css}
    {REDUCED}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#surface)"/>
{body}
    <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>
  </g>
</svg>
"""


def live_dot(x, y, color, delay=0.0):
    return f"""<circle cx="{x}" cy="{y}" r="3.2" fill="{color}" class="beacon" style="animation-delay:{delay}s"/>
    <circle cx="{x}" cy="{y}" r="3.2" fill="{color}"/>"""


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- header
def header():
    W, H = 900, 230
    phrase = "Routing research. Shipped products."
    n = len(phrase)
    char_w = 10.8
    L = n * char_w
    x0 = 450 - L / 2
    caret_kt = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    caret_xs = ";".join(f"{x0 + 1 + i * char_w:.1f}" for i in range(n + 1))
    css = f"""
    .shine {{ animation: shine 7s ease-in-out 1.6s infinite both; }}
    .type {{ transform-origin: {x0:.1f}px 0; animation: type 2.4s steps({n}) 1.1s both; }}
    .blink {{ animation: blink 1s steps(1) 3.5s infinite; }}
    @keyframes shine {{ 0% {{ transform: translateX(0); }} 45%, 100% {{ transform: translateX(1100px); }} }}
    @keyframes type {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}"""
    name_attrs = f'x="450" y="112" text-anchor="middle" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="1.5"'
    body = f"""
    <defs>
      <linearGradient id="nameFill" x1="0" x2="0" y1="56" y2="118" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#b9cff5"/></linearGradient>
      <linearGradient id="shineGrad" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <clipPath id="nameClip"><text {name_attrs}>Tanishka Jangir</text></clipPath>
      <clipPath id="typeClip"><rect class="type" x="{x0 - 1:.1f}" y="134" width="{L + 2:.1f}" height="32"/></clipPath>
    </defs>

    <g class="rise" style="animation-delay:.2s">
      <text {name_attrs} fill="url(#nameFill)">Tanishka Jangir</text>
      <g clip-path="url(#nameClip)"><rect class="shine" x="-240" y="44" width="140" height="90" fill="url(#shineGrad)" transform="skewX(-20)"/></g>
    </g>

    <text x="{x0:.1f}" y="156" font-family="{MONO}" font-size="18" fill="{INK2}" textLength="{L:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#typeClip)">{phrase}</text>
    <g class="blink"><rect x="{x0 + L + 2:.1f}" y="140" width="9" height="20" fill="{BLUE}" opacity=".85">
      <animate attributeName="x" values="{caret_xs}" keyTimes="{caret_kt}" dur="2.4s" begin="1.1s" calcMode="discrete"/>
      <set attributeName="x" to="{x0 + L + 2:.1f}" begin="3.5s" fill="freeze"/>
      <set attributeName="x" to="{x0 + 1:.1f}" begin="0s" dur="1.1s"/>
    </rect></g>

    <text x="450" y="200" text-anchor="middle" class="mono pop" font-size="9.5" letter-spacing="3" fill="{MUTED}" style="animation-delay:3.4s">NEW DELHI</text>
    <g class="mono" font-size="9" letter-spacing="2.5" fill="{MUTED}">
      <text x="24" y="28">TANISHKAJ26</text>
      <text x="862" y="28" text-anchor="end">OPEN TO SUMMER INTERNSHIPS</text>
    </g>
    {live_dot(874, 25, TEAL)}"""
    write("header.svg", svg(W, H, "Tanishka Jangir",
                            "Tanishka Jangir. Routing research. Shipped products. New Delhi. Open to summer internships.",
                            css, body))


# ---------------------------------------------------------------- section headers
def section(fname, number, title, tagline, accent):
    W, H = 900, 64
    body = f"""
    <g class="rise" style="animation-delay:.1s">
      <text x="26" y="40" class="mono" font-size="12" letter-spacing="2" fill="{accent}">{number}</text>
      <text x="62" y="41" class="sans" font-size="22" font-weight="700" fill="{INK}">{title}</text>
    </g>
    <text x="874" y="39" text-anchor="end" class="sans pop" font-size="14" font-style="italic" fill="{INK2}" style="animation-delay:.6s">{tagline}</text>
    <rect x="0" y="{H - 2}" width="{W}" height="2" fill="{accent}" opacity=".7" class="grow" style="animation-delay:.2s"/>"""
    write(fname, svg(W, H, title, f"{title}. {tagline}", "", body))


# ---------------------------------------------------------------- BGPShield card
def bgpshield():
    W, H = 900, 260
    track = 380
    stats = [
        (40, "2.87%", 0.0287, "of routed networks publish an ASPA record"),
        (480, "5.41%", 0.0541, "of routes contain two adjacent publishers"),
    ]
    stat_svg = ""
    for i, (x, num, frac, label) in enumerate(stats):
        d = 0.4 + i * 0.3
        stat_svg += f"""
    <g class="rise" style="animation-delay:{d:.2f}s">
      <text x="{x}" y="146" class="sans" font-size="48" font-weight="800" fill="{INK}">{num}</text>
      <text x="{x}" y="172" class="sans" font-size="14" fill="{INK2}">{label}</text>
    </g>
    <rect x="{x}" y="186" width="{track}" height="8" rx="4" fill="#1a2135"/>
    <rect x="{x}" y="186" width="{max(track * frac, 8):.1f}" height="8" rx="4" fill="{BLUE}" class="grow" style="animation-delay:{d + 0.4:.2f}s"/>
    <g class="mono" font-size="9" fill="{MUTED}"><text x="{x}" y="210">0</text><text x="{x + track}" y="210" text-anchor="end">100%</text></g>"""
    body = f"""
    <g class="rise" style="animation-delay:.1s">
      <text x="40" y="52" class="sans" font-size="26" font-weight="800" fill="{INK}">BGPShield</text>
      <text x="40" y="74" class="mono" font-size="9.5" letter-spacing="2.5" fill="{MUTED}">RPKI ROV + ASPA ADOPTION · PASSIVE-ONLY MEASUREMENT</text>
    </g>
    <text x="852" y="47" text-anchor="end" class="mono" font-size="9" letter-spacing="2.5" fill="{MUTED}">DASHBOARD REBUILT DAILY</text>
    {live_dot(866, 44, BLUE)}
    <path d="M40 92H860" stroke="{LINE}"/>
    <path d="M450 110V210" stroke="{LINE}"/>
    {stat_svg}
    <path d="M40 224H860" stroke="{LINE}"/>
    <g class="mono" font-size="9" letter-spacing="1.8" fill="{MUTED}">
      <text x="40" y="244">PYTHON 3.12 · 386 TESTS PASSING · CI · EVERY NUMBER RE-DERIVES WITH ONE COMMAND</text>
      <text x="860" y="244" text-anchor="end" fill="{BLUE}">LIVE DASHBOARD ↗</text>
    </g>"""
    write("bgpshield.svg", svg(W, H, "BGPShield",
                               "BGPShield. 2.87% of routed networks publish an ASPA record. 5.41% of routes contain two adjacent publishers. Python 3.12, 386 tests passing, CI, dashboard rebuilt daily.",
                               "", body))


# ---------------------------------------------------------------- project cards
def project(fname, name, accent, lines, chips, repo):
    W, H = 440, 224
    chip_svg, x = "", 28
    for i, c in enumerate(chips):
        w = len(c) * 6.4 + 20
        chip_svg += f"""<g class="pop" style="animation-delay:{0.6 + i * 0.1:.2f}s">
      <rect x="{x}" y="156" width="{w:.1f}" height="22" rx="11" fill="none" stroke="{LINE}" stroke-width="1.2"/>
      <text x="{x + w / 2:.1f}" y="171" text-anchor="middle" class="mono" font-size="10" fill="{INK2}">{c}</text>
    </g>"""
        x += w + 8
    desc = "".join(f'<text x="28" y="{92 + i * 21}">{l}</text>' for i, l in enumerate(lines))
    body = f"""
    <rect x="0" y="0" width="{W}" height="3" fill="{accent}" class="grow"/>
    <text x="28" y="54" class="sans rise" font-size="24" font-weight="800" fill="{INK}" style="animation-delay:.15s">{name}</text>
    <text x="398" y="47" text-anchor="end" class="mono" font-size="9" letter-spacing="3" fill="{MUTED}">LIVE</text>
    {live_dot(410, 44, accent, 0.6)}
    <g class="sans rise" font-size="13.5" fill="{INK2}" style="animation-delay:.35s">{desc}</g>
    {chip_svg}
    <text x="28" y="206" class="mono" font-size="9" letter-spacing="1" fill="{MUTED}">{repo}</text>
    <text x="412" y="206" text-anchor="end" class="mono" font-size="9" letter-spacing="2" fill="{accent}">REPO ↗</text>"""
    write(fname, svg(W, H, name, f"{name}. {' '.join(lines)} Built with {', '.join(chips)}.", "", body))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 160
    body = f"""
    <defs>
      <linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
    </defs>
    <g class="rise" style="animation-delay:.1s">
      <text x="442" y="46" text-anchor="middle" class="mono" font-size="10" letter-spacing="5" fill="{MUTED}">AVAILABLE</text>
      <text x="450" y="86" text-anchor="middle" class="sans" font-size="26" font-weight="800" fill="{INK}">Looking for a summer internship.</text>
      <text x="450" y="114" text-anchor="middle" class="sans" font-size="15" font-style="italic" fill="{INK2}">Bring a hard problem.</text>
    </g>
    {live_dot(502, 42, TEAL, 0.4)}
    <rect x="330" y="134" width="240" height="1.5" fill="url(#rule)" class="grow" style="animation-delay:.6s"/>"""
    write("footer.svg", svg(W, H, "Available",
                            "Looking for a summer internship. Bring a hard problem.", "", body))


if __name__ == "__main__":
    header()
    section("section-security.svg", "01", "Internet Security", "The main event.", BLUE)
    section("section-fullstack.svg", "02", "Full Stack", "Shipped and live.", AMBER)
    bgpshield()
    project("spotlight.svg", "Spotlight", AMBER,
            ["AI webinar SaaS. Hosts stream live from OBS,",
             "with VAPI voice agents users configure",
             "themselves. Recordings and Stripe subscriptions."],
            ["Next.js 15", "TypeScript", "Prisma", "Neon Postgres"],
            "github.com/TanishkaJ26/Spotlight")
    project("wanderlust.svg", "WanderLust", TEAL,
            ["Airbnb-inspired rentals. List, edit and browse",
             "properties with auth, Mapbox geocoding,",
             "search, category filters, Cloudinary uploads."],
            ["Node.js", "Express", "MongoDB Atlas", "Passport.js"],
            "github.com/TanishkaJ26/wanderlust")
    footer()
