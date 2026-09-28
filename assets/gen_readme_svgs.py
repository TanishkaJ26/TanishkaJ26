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
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .comet, .comet-tail { display: none; } }"


def rounded_rect_path(w, h, r):
    a, b = 0.5, r + 0.5
    return (f"M{b} {a}H{w - b}A{r} {r} 0 0 1 {w - a} {b}V{h - b}A{r} {r} 0 0 1 {w - b} {h - a}"
            f"H{b}A{r} {r} 0 0 1 {a} {h - b}V{b}A{r} {r} 0 0 1 {b} {a}Z")


def svg(w, h, title, desc, css, body, comet=None, comet_dur=10):
    """A card. `comet` is the colour of the light that travels around the border, or None."""
    trail = ""
    if comet:
        d = rounded_rect_path(w, h, 14)
        P = round(2 * (w + h) - 8 * 14 + 2 * 3.14159 * 14)  # perimeter of the rounded rect
        core, tail, lag = 36, 110, 70
        css += f"""
    .comet {{ animation: comet {comet_dur}s linear infinite; }}
    .comet-tail {{ animation: comet-tail {comet_dur}s linear infinite; }}
    @keyframes comet {{ from {{ stroke-dashoffset: 0; }} to {{ stroke-dashoffset: -{P}; }} }}
    @keyframes comet-tail {{ from {{ stroke-dashoffset: {lag}; }} to {{ stroke-dashoffset: {lag - P}; }} }}"""
        trail = f"""
    <path d="{d}" fill="none" stroke="{comet}" stroke-width="3" stroke-opacity=".2" stroke-dasharray="{tail} {P - tail}" class="comet-tail"/>
    <path d="{d}" fill="none" stroke="{comet}" stroke-width="1.5" stroke-dasharray="{core} {P - core}" stroke-linecap="round" class="comet"/>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  <defs>
    <linearGradient id="surface" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#111626"/><stop offset="1" stop-color="#0b0e18"/></linearGradient>
    <linearGradient id="glint" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  </defs>
  <style>{BASE_CSS}{css}
    {REDUCED}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="url(#surface)"/>
{body}
    <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>{trail}
  </g>
</svg>
"""


def glint(uid, x, y, w, h, every=6.0, begin=1.5, size=120):
    """A highlight that sweeps along the rectangle (x, y, w, h), then rests until the next pass."""
    travel = w + size
    move = min(1.6, every * 0.4)
    k = move / every
    return f"""<clipPath id="{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>
    <g clip-path="url(#{uid})"><rect x="{x - size}" y="{y}" width="{size}" height="{h}" fill="url(#glint)" opacity=".8">
      <animateTransform attributeName="transform" type="translate" values="0 0;{travel} 0;{travel} 0" keyTimes="0;{k:.3f};1" dur="{every}s" begin="{begin}s" repeatCount="indefinite"/>
    </rect></g>"""


def live_dot(x, y, color, delay=0.0):
    return f"""<circle cx="{x}" cy="{y}" r="3.2" fill="{color}" class="beacon" style="animation-delay:{delay}s"/>
    <circle cx="{x}" cy="{y}" r="3.2" fill="{color}"/>"""


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- header
def typing_frames(phrases, type_dt=0.07, erase_dt=0.025, hold=3.2, gap=0.45):
    """(time, phrase index, visible chars) for one full type/hold/erase cycle over all phrases."""
    frames, t = [], 0.0
    for i, p in enumerate(phrases):
        for k in range(len(p) + 1):
            frames.append((t, i, k)); t += type_dt
        t += hold
        for k in range(len(p) - 1, -1, -1):
            frames.append((t, i, k)); t += erase_dt
        t += gap
    return frames, t


def header():
    W, H = 900, 230
    phrases = ["Routing research. Shipped products.", "Passive measurement. Every number re-derivable."]
    cw, y = 10.8, 156
    x0s = [450 - len(p) * cw / 2 for p in phrases]
    frames, total = typing_frames(phrases)
    kt = ";".join(f"{t / total:.4f}" for t, _, _ in frames)
    anim = f'keyTimes="{kt}" dur="{total:.2f}s" begin="0s" calcMode="discrete" repeatCount="indefinite"'

    typed = ""
    for j, p in enumerate(phrases):
        L = len(p) * cw
        widths = ";".join(f"{k * cw + 1 if i == j else 0:.1f}" for _, i, k in frames)
        typed += f"""
    <clipPath id="type{j}"><rect x="{x0s[j] - 1:.1f}" y="{y - 22}" width="{L + 2 if j == 0 else 0:.1f}" height="32">
      <animate attributeName="width" values="{widths}" {anim}/>
    </rect></clipPath>
    <text x="{x0s[j]:.1f}" y="{y}" font-family="{MONO}" font-size="18" fill="{INK2}" textLength="{L:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#type{j})">{p}</text>"""
    caret_xs = ";".join(f"{x0s[i] + k * cw + 2:.1f}" for _, i, k in frames)
    end0 = x0s[0] + len(phrases[0]) * cw + 2

    css = """
    .shine { animation: shine 7s ease-in-out 1.6s infinite both; }
    .blink { animation: blink 1s steps(1) infinite; }
    @keyframes shine { 0% { transform: translateX(0); } 45%, 100% { transform: translateX(1100px); } }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } }"""
    name_attrs = f'x="450" y="112" text-anchor="middle" font-family="{SANS}" font-size="58" font-weight="800" letter-spacing="1.5"'
    body = f"""
    <defs>
      <linearGradient id="nameFill" x1="0" x2="0" y1="56" y2="118" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#b9cff5"/></linearGradient>
      <clipPath id="nameClip"><text {name_attrs}>Tanishka Jangir</text></clipPath>
    </defs>

    <g class="rise" style="animation-delay:.2s">
      <text {name_attrs} fill="url(#nameFill)">Tanishka Jangir</text>
      <g clip-path="url(#nameClip)"><rect class="shine" x="-240" y="44" width="140" height="90" fill="url(#glint)" opacity=".85" transform="skewX(-20)"/></g>
    </g>
    {typed}
    <g class="blink"><rect x="{end0:.1f}" y="{y - 16}" width="9" height="20" fill="{BLUE}" opacity=".85">
      <animate attributeName="x" values="{caret_xs}" {anim}/>
    </rect></g>

    <text x="450" y="200" text-anchor="middle" class="mono pop" font-size="9.5" letter-spacing="3" fill="{MUTED}" style="animation-delay:1s">NEW DELHI</text>
    <g class="mono" font-size="9" letter-spacing="2.5" fill="{MUTED}">
      <text x="24" y="28">TANISHKAJ26</text>
      <text x="862" y="28" text-anchor="end">OPEN TO WORK</text>
    </g>
    {live_dot(874, 25, TEAL)}"""
    write("header.svg", svg(W, H, "Tanishka Jangir",
                            "Tanishka Jangir. Routing research. Shipped products. Passive measurement. Every number re-derivable. New Delhi. Open to work.",
                            css, body, comet=BLUE, comet_dur=12))


# ---------------------------------------------------------------- section headers
def section(fname, number, title, tagline, accent):
    W, H = 900, 64
    body = f"""
    <g class="rise" style="animation-delay:.1s">
      <text x="26" y="40" class="mono" font-size="12" letter-spacing="2" fill="{accent}">{number}</text>
      <text x="62" y="41" class="sans" font-size="22" font-weight="700" fill="{INK}">{title}</text>
    </g>
    <text x="874" y="39" text-anchor="end" class="sans pop" font-size="14" font-style="italic" fill="{INK2}" style="animation-delay:.6s">{tagline}</text>
    <rect x="0" y="{H - 2}" width="{W}" height="2" fill="{accent}" opacity=".7" class="grow" style="animation-delay:.2s"/>
    {glint("g", 0, H - 2, W, 2, every=5, begin=1.6, size=180)}"""
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
        fill = max(track * frac, 8)
        stat_svg += f"""
    <g class="rise" style="animation-delay:{d:.2f}s">
      <text x="{x}" y="146" class="sans" font-size="48" font-weight="800" fill="{INK}">{num}</text>
      <text x="{x}" y="172" class="sans" font-size="14" fill="{INK2}">{label}</text>
    </g>
    <rect x="{x}" y="186" width="{track}" height="8" rx="4" fill="#1a2135"/>
    {glint(f"t{i}", x, 186, track, 8, every=6, begin=2.2 + i * 0.25, size=90)}
    <rect x="{x}" y="186" width="{fill:.1f}" height="8" rx="4" fill="{BLUE}" class="grow" style="animation-delay:{d + 0.4:.2f}s"/>
    <circle cx="{x + fill - 4:.1f}" cy="190" r="4" fill="{BLUE}" class="beacon" style="animation-delay:{1.4 + i * 0.4:.1f}s"/>
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
                               "", body, comet=BLUE, comet_dur=14))


# ---------------------------------------------------------------- project cards
def project(fname, name, accent, chips, repo, offset=0.0, live=True):
    W, H = 440, 150
    cycle = 8
    css = f"""
    .chip {{ animation: chip {cycle}s ease-in-out infinite; }}
    @keyframes chip {{ 0%, 16%, 100% {{ stroke: {LINE}; }} 7% {{ stroke: {accent}; }} }}"""
    chip_svg, x = "", 28
    for i, c in enumerate(chips):
        c = c if len(c) <= 18 else c[:17] + "…"
        w = len(c) * 6.4 + 20
        if x + w > W - 28:
            break
        chip_svg += f"""<g class="pop" style="animation-delay:{0.6 + i * 0.1:.2f}s">
      <rect x="{x}" y="80" width="{w:.1f}" height="22" rx="11" fill="none" stroke="{LINE}" stroke-width="1.2" class="chip" style="animation-delay:{1.5 + offset + i * 0.45:.2f}s"/>
      <text x="{x + w / 2:.1f}" y="95" text-anchor="middle" class="mono" font-size="10" fill="{INK2}">{c}</text>
    </g>"""
        x += w + 8
    live_marker = ""
    if live:
        live_marker = f"""<text x="398" y="47" text-anchor="end" class="mono" font-size="9" letter-spacing="3" fill="{MUTED}">LIVE</text>
    {live_dot(410, 44, accent, 0.6 + offset)}"""
    body = f"""
    <rect x="0" y="0" width="{W}" height="3" fill="{accent}" class="grow"/>
    {glint("g", 0, 0, W, 3, every=6, begin=1.4 + offset, size=110)}
    <text x="28" y="54" class="sans rise" font-size="24" font-weight="800" fill="{INK}" style="animation-delay:.15s">{name if len(name) <= 22 else name[:21] + "…"}</text>
    {live_marker}
    {chip_svg}
    <text x="28" y="130" class="mono" font-size="9" letter-spacing="1" fill="{MUTED}">{repo}</text>
    <text x="412" y="130" text-anchor="end" class="mono" font-size="9" letter-spacing="2" fill="{accent}">REPO ↗</text>"""
    write(fname, svg(W, H, name, f"{name}. Built with {', '.join(chips)}.", css, body,
                     comet=accent, comet_dur=9 + offset * 2))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 900, 120
    text_w = 200  # fixed via textLength so the dot sits right beside the words in any font
    x0 = 450 - text_w / 2 + 12
    body = f"""
    <defs>
      <linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
    </defs>
    <g class="rise" style="animation-delay:.1s">
      <text x="{x0}" y="66" class="sans" font-size="30" font-weight="800" fill="{INK}" textLength="{text_w}" lengthAdjust="spacingAndGlyphs">Open to work</text>
    </g>
    {live_dot(x0 - 20, 56, TEAL, 0.4)}
    <rect x="330" y="92" width="240" height="1.5" fill="url(#rule)" class="grow" style="animation-delay:.6s"/>
    {glint("g", 330, 91, 240, 3.5, every=5, begin=1.8, size=80)}"""
    write("footer.svg", svg(W, H, "Open to work", "Open to work.", "", body,
                            comet=TEAL, comet_dur=12))


if __name__ == "__main__":
    header()
    section("section-security.svg", "01", "Internet Security", "The main event.", BLUE)
    section("section-fullstack.svg", "02", "Full Stack", "Shipped and live.", AMBER)
    section("section-more.svg", "03", "More Work", "Newest first. Added automatically.", TEAL)
    bgpshield()
    project("spotlight.svg", "Spotlight", AMBER,
            ["Next.js 15", "TypeScript", "Prisma", "Neon Postgres"],
            "github.com/TanishkaJ26/Spotlight")
    project("wanderlust.svg", "WanderLust", TEAL,
            ["Node.js", "Express", "MongoDB Atlas", "Passport.js"],
            "github.com/TanishkaJ26/wanderlust", offset=0.8)
    footer()
