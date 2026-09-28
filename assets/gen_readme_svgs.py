"""Builds the README panels: header, section headers, BGPShield card, project cards, footer.

Run from the repo root:  python assets/gen_readme_svgs.py
The star map has its own generator (gen_starmap.py).
"""
import os
import random

OUT = os.path.dirname(os.path.abspath(__file__))

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"

INK = "#f1f5ff"      # primary text
INK2 = "#c3cde6"     # body text
MUTED = "#6f7fa6"    # chart furniture
LABEL = "#7f95c8"    # small caps labels
BLUE, AMBER, TEAL, ROSE = "#9cc2ff", "#ffd28a", "#8ff0d6", "#c88fa9"

BASE_CSS = f"""
    .pop {{ animation: pop .9s ease-out both; }}
    .rise {{ animation: rise 1s cubic-bezier(.2,.7,.2,1) both; }}
    .cl {{ fill: none; stroke: #8fa9dc; stroke-width: 1; stroke-opacity: .55; stroke-dasharray: 1; animation: draw 1.1s ease-out both; }}
    .tw {{ animation: twinkle 4s ease-in-out infinite; }}
    .tw2 {{ animation-duration: 5.5s; }}
    .tw3 {{ animation-duration: 7s; }}
    .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 5s ease-in-out infinite; }}
    .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 30s linear infinite; }}
    .beacon {{ transform-box: fill-box; transform-origin: center; animation: beacon 2.4s ease-out infinite; }}
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
    @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes twinkle {{ 0%, 100% {{ opacity: .9; }} 50% {{ opacity: .15; }} }}
    @keyframes pulse {{ 0%, 100% {{ transform: scale(.88); opacity: .8; }} 50% {{ transform: scale(1.12); opacity: 1; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes beacon {{ 0% {{ transform: scale(1); opacity: .9; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
"""
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def sky_defs(w, h):
    return f"""
    <radialGradient id="sky" cx="38%" cy="40%" r="85%">
      <stop offset="0" stop-color="#141c33"/><stop offset=".55" stop-color="#0a0f1e"/><stop offset="1" stop-color="#04060c"/>
    </radialGradient>
    <radialGradient id="neb-blue"><stop offset="0" stop-color="#3b5bdb" stop-opacity=".24"/><stop offset="1" stop-color="#3b5bdb" stop-opacity="0"/></radialGradient>
    <radialGradient id="neb-rose"><stop offset="0" stop-color="#b8487a" stop-opacity=".18"/><stop offset="1" stop-color="#b8487a" stop-opacity="0"/></radialGradient>
    <radialGradient id="neb-amber"><stop offset="0" stop-color="#c9822f" stop-opacity=".2"/><stop offset="1" stop-color="#c9822f" stop-opacity="0"/></radialGradient>
    <radialGradient id="neb-teal"><stop offset="0" stop-color="#1f9c84" stop-opacity=".2"/><stop offset="1" stop-color="#1f9c84" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow-blue"><stop offset="0" stop-color="#bcd6ff" stop-opacity=".55"/><stop offset=".35" stop-color="#6f9eff" stop-opacity=".18"/><stop offset="1" stop-color="#6f9eff" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow-amber"><stop offset="0" stop-color="#ffe2b0" stop-opacity=".55"/><stop offset=".4" stop-color="#ffb04a" stop-opacity=".14"/><stop offset="1" stop-color="#ffb04a" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow-teal"><stop offset="0" stop-color="#c4fff0" stop-opacity=".55"/><stop offset=".4" stop-color="#3fd9b0" stop-opacity=".14"/><stop offset="1" stop-color="#3fd9b0" stop-opacity="0"/></radialGradient>
    <filter id="haze" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="24"/></filter>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="16"/></clipPath>"""


def starfield(w, h, n, seed, keep_out=()):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        x, y = rnd.uniform(6, w - 6), rnd.uniform(6, h - 6)
        if any(a <= x <= c and b <= y <= d for a, b, c, d in keep_out):
            continue
        r = rnd.choice([0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2])
        o = round(rnd.uniform(0.2, 0.8), 2)
        tint = rnd.choice(["#ffffff"] * 6 + ["#cfe0ff", "#ffe9c9", "#dcd4ff"])
        cls = ""
        if rnd.random() < 0.3:
            cls = f' class="tw tw{rnd.randint(1, 3)}" style="animation-delay:{rnd.uniform(0, 6):.1f}s"'
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{tint}" opacity="{o}"{cls}/>')
    return "".join(out)


def frame(w, h):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="#2a3558" stroke-opacity=".8"/>'


def svg(w, h, title, desc, css, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  <defs>{sky_defs(w, h)}
  </defs>
  <style>{BASE_CSS}{css}
    {REDUCED}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#sky)"/>
{body}
    {frame(w, h)}
  </g>
</svg>
"""


def star(x, y, color, glow, core, delay=0.0):
    return f"""<g class="pop" style="animation-delay:{delay:.2f}s">
      <circle cx="{x}" cy="{y}" r="{glow}" fill="url(#glow-{color})" class="pulse"/>
      <circle cx="{x}" cy="{y}" r="{core * 2}" fill="{dict(blue=BLUE, amber=AMBER, teal=TEAL)[color]}" opacity=".35"/>
      <circle cx="{x}" cy="{y}" r="{core}" fill="#fff"/>
    </g>"""


def live_dot(x, y, color, delay=0.0):
    return f"""<circle cx="{x}" cy="{y}" r="3.2" fill="{color}" class="beacon" style="animation-delay:{delay}s"/>
    <circle cx="{x}" cy="{y}" r="3.2" fill="{color}"/>"""


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- header
def header():
    W, H = 900, 250
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
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
"""
    name_attrs = f'x="450" y="118" text-anchor="middle" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="1.5"'
    body = f"""
    <circle cx="200" cy="120" r="230" fill="url(#neb-blue)"/>
    <circle cx="720" cy="140" r="240" fill="url(#neb-rose)"/>

    <defs>
      <linearGradient id="nameFill" x1="0" x2="0" y1="60" y2="124" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#b9cff5"/></linearGradient>
      <linearGradient id="shineGrad" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <clipPath id="nameClip"><text {name_attrs}>Tanishka Jangir</text></clipPath>
      <clipPath id="typeClip"><rect class="type" x="{x0 - 1:.1f}" y="140" width="{L + 2:.1f}" height="32"/></clipPath>
    </defs>

    <g class="rise" style="animation-delay:.2s">
      <text {name_attrs} fill="url(#nameFill)">Tanishka Jangir</text>
      <g clip-path="url(#nameClip)"><rect class="shine" x="-240" y="50" width="140" height="90" fill="url(#shineGrad)" transform="skewX(-20)"/></g>
    </g>

    <text x="{x0:.1f}" y="162" font-family="{MONO}" font-size="18" fill="{INK2}" textLength="{L:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#typeClip)">{phrase}</text>
    <g class="blink"><rect x="{x0 + L + 2:.1f}" y="146" width="9" height="20" fill="{BLUE}" opacity=".85">
      <animate attributeName="x" values="{caret_xs}" keyTimes="{caret_kt}" dur="2.4s" begin="1.1s" calcMode="discrete"/>
      <set attributeName="x" to="{x0 + L + 2:.1f}" begin="3.5s" fill="freeze"/>
      <set attributeName="x" to="{x0 + 1:.1f}" begin="0s" dur="1.1s"/>
    </rect></g>

    <g class="mono pop" font-size="9.5" letter-spacing="3" fill="{MUTED}" style="animation-delay:3.4s">
      <text x="450" y="212" text-anchor="middle">NEW DELHI</text>
    </g>
    <g class="mono" font-size="9" letter-spacing="2.5" fill="{MUTED}">
      <text x="24" y="28">TANISHKAJ26</text>
      <text x="862" y="28" text-anchor="end">OPEN TO SUMMER INTERNSHIPS</text>
    </g>
    {live_dot(874, 25, TEAL)}"""
    write("header.svg", svg(W, H, "Tanishka Jangir",
                            "Tanishka Jangir. Routing research. Shipped products. New Delhi. Open to summer internships.",
                            css, body))


# ---------------------------------------------------------------- section headers
def section(fname, numeral, title, tagline, pts, lines, named, nebula):
    W, H = 900, 76
    ox, oy = 26, 9
    P = [(ox + x, oy + y) for x, y in pts]
    ls = "".join(
        f'<path d="M{P[a][0]} {P[a][1]}L{P[b][0]} {P[b][1]}" pathLength="1" class="cl" style="animation-delay:{0.2 + i * 0.12:.2f}s"/>'
        for i, (a, b) in enumerate(lines))
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1.5" fill="#dfe8ff" class="pop" style="animation-delay:{0.1 + i * 0.05:.2f}s"/>'
        for i, (x, y) in enumerate(P) if i not in named)
    stars = "".join(star(P[i][0], P[i][1], c, 14, 2.4, 0.6 + k * 0.2) for k, (i, c) in enumerate(named.items()))
    body = f"""
    <circle cx="60" cy="38" r="160" fill="url(#{nebula})"/>
    <g>{starfield(W, H, 60, len(title), [(20, 0, 520, 76), (560, 20, 890, 60)])}</g>
    <g>{ls}</g><g>{dots}</g>{stars}
    <g class="rise" style="animation-delay:.3s">
      <text x="104" y="31" class="mono" font-size="9.5" letter-spacing="4" fill="{LABEL}">CONSTELLATION {numeral}</text>
      <text x="104" y="57" class="sans" font-size="24" font-weight="700" fill="{INK}">{title}</text>
    </g>
    <text x="874" y="44" text-anchor="end" class="sans pop" font-size="15" font-style="italic" fill="{INK2}" style="animation-delay:.9s">{tagline}</text>"""
    write(fname, svg(W, H, f"Constellation {numeral}: {title}", f"{title}. {tagline}", "", body))


# ---------------------------------------------------------------- BGPShield card
def bgpshield():
    W, H = 900, 280
    track = 380
    stats = [
        (40, "2.87%", 0.0287, "of routed networks publish an ASPA record"),
        (480, "5.41%", 0.0541, "of routes contain two adjacent publishers"),
    ]
    css = """
    .grow { transform-box: fill-box; transform-origin: left center; animation: grow 1.4s cubic-bezier(.2,.7,.2,1) both; }
    .sweep { opacity: 0; animation: sweep 9s linear 1s infinite both; }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @keyframes sweep { from { transform: translateX(-120px); opacity: 1; } to { transform: translateX(1020px); opacity: 1; } }"""
    stat_svg = ""
    for i, (x, num, frac, label) in enumerate(stats):
        d = 0.5 + i * 0.35
        stat_svg += f"""
    <g class="rise" style="animation-delay:{d:.2f}s">
      <text x="{x}" y="164" class="sans" font-size="48" font-weight="800" fill="{INK}">{num}</text>
      <text x="{x}" y="190" class="sans" font-size="14" fill="{INK2}">{label}</text>
    </g>
    <rect x="{x}" y="204" width="{track}" height="8" rx="4" fill="#1c2644"/>
    <rect x="{x}" y="204" width="{max(track * frac, 8):.1f}" height="8" rx="4" fill="{BLUE}" class="grow" style="animation-delay:{d + 0.4:.2f}s"/>
    <g class="mono" font-size="9" fill="{MUTED}"><text x="{x}" y="228">0</text><text x="{x + track}" y="228" text-anchor="end">100%</text></g>"""
    body = f"""
    <defs>
      <linearGradient id="sweepGrad" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".92" stop-color="{BLUE}" stop-opacity=".10"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".45"/></linearGradient>
    </defs>
    <circle cx="120" cy="60" r="260" fill="url(#neb-blue)"/>
    <g>{starfield(W, H, 90, 11, [(24, 20, 560, 96), (600, 34, 890, 62), (30, 120, 880, 236), (24, 244, 890, 266)])}</g>
    <rect class="sweep" x="0" y="0" width="120" height="{H}" fill="url(#sweepGrad)"/>

    <g class="pop">
      <circle cx="46" cy="54" r="30" fill="url(#glow-blue)" class="pulse"/>
      <path d="M22 54H70M46 30V78" stroke="#dbe7ff" stroke-width="1" opacity=".6"/>
      <circle cx="46" cy="54" r="6" fill="{BLUE}" opacity=".4"/><circle cx="46" cy="54" r="3.2" fill="#fff"/>
      <circle cx="46" cy="54" r="15" fill="none" stroke="{BLUE}" stroke-width=".8" stroke-dasharray="2 4" opacity=".7" class="spin"/>
    </g>
    <g class="rise" style="animation-delay:.15s">
      <text x="80" y="60" class="sans" font-size="28" font-weight="800" fill="{INK}">BGPShield</text>
      <text x="80" y="82" class="mono" font-size="9.5" letter-spacing="2.5" fill="{LABEL}">RPKI ROV + ASPA ADOPTION · PASSIVE-ONLY MEASUREMENT</text>
    </g>
    <text x="852" y="52" text-anchor="end" class="mono" font-size="9" letter-spacing="2.5" fill="{MUTED}">DASHBOARD REBUILT DAILY</text>
    {live_dot(866, 49, BLUE)}
    <path d="M40 106H860" stroke="#9fb3e0" stroke-opacity=".14"/>
    <path d="M450 124V228" stroke="#9fb3e0" stroke-opacity=".12"/>
    {stat_svg}
    <path d="M40 242H860" stroke="#9fb3e0" stroke-opacity=".14"/>
    <g class="mono" font-size="9" letter-spacing="1.8" fill="{MUTED}">
      <text x="40" y="262">PYTHON 3.12 · 386 TESTS PASSING · CI · EVERY NUMBER RE-DERIVES WITH ONE COMMAND</text>
      <text x="860" y="262" text-anchor="end" fill="{BLUE}">LIVE DASHBOARD ↗</text>
    </g>"""
    write("bgpshield.svg", svg(W, H, "BGPShield",
                               "BGPShield. 2.87% of routed networks publish an ASPA record. 5.41% of routes contain two adjacent publishers. Python 3.12, 386 tests passing, CI, dashboard rebuilt daily.",
                               css, body))


# ---------------------------------------------------------------- project cards
def project(fname, name, color, accent, nebula, lines, chips, repo):
    W, H = 440, 232
    chip_svg, x = "", 28
    for i, c in enumerate(chips):
        w = len(c) * 6.4 + 20
        chip_svg += f"""<g class="pop" style="animation-delay:{0.7 + i * 0.1:.2f}s">
      <rect x="{x}" y="164" width="{w:.1f}" height="22" rx="11" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".35"/>
      <text x="{x + w / 2:.1f}" y="179" text-anchor="middle" class="mono" font-size="10" fill="{INK2}">{c}</text>
    </g>"""
        x += w + 8
    desc = "".join(f'<text x="28" y="{100 + i * 21}">{l}</text>' for i, l in enumerate(lines))
    body = f"""
    <circle cx="40" cy="40" r="220" fill="url(#{nebula})"/>
    <g>{starfield(W, H, 55, len(name) * 3, [(14, 14, 426, 206)])}</g>
    {star(44, 50, color, 30, 3.4, 0.1)}
    <circle cx="44" cy="50" r="15" fill="none" stroke="{accent}" stroke-width=".8" stroke-dasharray="2 4" opacity=".6" class="spin"/>
    <text x="72" y="59" class="sans rise" font-size="24" font-weight="800" fill="{INK}" style="animation-delay:.2s">{name}</text>
    <text x="398" y="47" text-anchor="end" class="mono" font-size="9" letter-spacing="3" fill="{MUTED}">LIVE</text>
    {live_dot(410, 44, accent, 0.6)}
    <g class="sans rise" font-size="13.5" fill="{INK2}" style="animation-delay:.4s">{desc}</g>
    {chip_svg}
    <text x="28" y="214" class="mono" font-size="9" letter-spacing="1" fill="{MUTED}">{repo}</text>
    <text x="412" y="214" text-anchor="end" class="mono" font-size="9" letter-spacing="2" fill="{accent}">REPO ↗</text>"""
    write(fname, svg(W, H, name, f"{name}. {' '.join(lines)} Built with {', '.join(chips)}.", "", body))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 170
    css = """
    .underline { transform-box: fill-box; transform-origin: center; animation: grow 1.2s cubic-bezier(.2,.7,.2,1) .6s both; }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }"""
    body = f"""
    <defs>
      <linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
    </defs>
    <circle cx="250" cy="170" r="260" fill="url(#neb-blue)"/>
    <circle cx="680" cy="0" r="240" fill="url(#neb-rose)"/>
    <g class="rise" style="animation-delay:.1s">
      <text x="442" y="50" text-anchor="middle" class="mono" font-size="10" letter-spacing="5" fill="{LABEL}">AVAILABLE</text>
      <text x="450" y="92" text-anchor="middle" class="sans" font-size="26" font-weight="800" fill="{INK}">Looking for a summer internship.</text>
      <text x="450" y="120" text-anchor="middle" class="sans" font-size="15" font-style="italic" fill="{INK2}">Bring a hard problem.</text>
    </g>
    {live_dot(502, 46, TEAL, 0.4)}
    <rect class="underline" x="330" y="140" width="240" height="1.5" fill="url(#rule)"/>"""
    write("footer.svg", svg(W, H, "Available",
                            "Looking for a summer internship. Bring a hard problem.", css, body))


if __name__ == "__main__":
    header()
    section("section-security.svg", "I", "Internet Security", "The bright one.",
            [(8, 10), (28, 5), (48, 10), (46, 34), (28, 54), (10, 34), (28, 28)],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 6)],
            {6: "blue"}, "neb-blue")
    section("section-fullstack.svg", "II", "Full Stack", "Smaller stars. Both live.",
            [(2, 54), (12, 42), (24, 30), (42, 18), (58, 26), (54, 48), (36, 52)],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 2)],
            {2: "amber", 5: "teal"}, "neb-rose")
    bgpshield()
    project("spotlight.svg", "Spotlight", "amber", AMBER, "neb-amber",
            ["AI webinar SaaS. Hosts stream live from OBS,",
             "with VAPI voice agents users configure",
             "themselves. Recordings and Stripe subscriptions."],
            ["Next.js 15", "TypeScript", "Prisma", "Neon Postgres"],
            "github.com/TanishkaJ26/Spotlight")
    project("wanderlust.svg", "WanderLust", "teal", TEAL, "neb-teal",
            ["Airbnb-inspired rentals. List, edit and browse",
             "properties with auth, Mapbox geocoding,",
             "search, category filters, Cloudinary uploads."],
            ["Node.js", "Express", "MongoDB Atlas", "Passport.js"],
            "github.com/TanishkaJ26/wanderlust")
    footer()
