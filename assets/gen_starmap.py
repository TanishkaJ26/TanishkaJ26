import random, math, sys

W, H = 900, 400
random.seed(26)

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ---------- background stars ----------
bg = []
# keep background stars off labels and named stars
KEEP_OUT = [(12, 16, 240, 38), (780, 16, 890, 38), (12, 362, 240, 388), (630, 362, 890, 388),
            (140, 38, 360, 60), (610, 64, 760, 86), (180, 220, 320, 266), (505, 150, 604, 176),
            (736, 268, 836, 294), (456, 322, 530, 346), (20, 222, 110, 242),
            (208, 138, 292, 222), (590, 150, 634, 194), (764, 234, 808, 278)]
bg_n = 0
while bg_n < 170:
    x, y = random.uniform(8, W - 8), random.uniform(8, H - 8)
    if any(a <= x <= c and b <= y <= d for a, b, c, d in KEEP_OUT):
        continue
    bg_n += 1
    r = random.choice([0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2])
    o = round(random.uniform(0.25, 0.85), 2)
    tint = random.choice(["#ffffff"] * 6 + ["#cfe0ff", "#ffe9c9", "#dcd4ff"])
    cls = ""
    if random.random() < 0.3:
        cls = f' class="tw tw{random.randint(1, 3)}" style="animation-delay:{random.uniform(0, 6):.1f}s"'
    bg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{tint}" opacity="{o}"{cls}/>')

# ---------- constellations ----------
# Internet Security: a shield outline, BGPShield at its heart
TM, TR, RM, TIP, LM, TL = (250, 80), (372, 98), (360, 204), (250, 312), (140, 204), (128, 98)
BGP = (250, 180)
sec_minor = [TM, TR, RM, TIP, LM, TL]
sec_lines = [(TL, TM), (TM, TR), (TR, RM), (RM, TIP), (TIP, LM), (LM, TL), (TM, BGP)]

# Full Stack: a dipper, Spotlight and WanderLust as its named stars
SPOT, WAND = (612, 172), (786, 256)
H1, H2 = (522, 280), (562, 226)
B1, B2, B3 = (716, 128), (814, 162), (676, 276)
fs_minor = [H1, H2, B1, B2, B3]
fs_lines = [(H1, H2), (H2, SPOT), (SPOT, B1), (B1, B2), (B2, WAND), (WAND, B3), (B3, SPOT)]

DSA = (466, 334)


def line(a, b, delay):
    return (f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" pathLength="1" class="cl" '
            f'style="animation-delay:{delay:.2f}s"/>')


def minor(p, delay):
    return (f'<circle cx="{p[0]}" cy="{p[1]}" r="1.9" fill="#dfe8ff" class="pop" '
            f'style="animation-delay:{delay:.2f}s"/>')


def bright(p, color, core, glow, delay):
    x, y = p
    return f'''<g class="pop" style="animation-delay:{delay:.2f}s">
    <circle cx="{x}" cy="{y}" r="{glow}" fill="url(#glow-{color})" class="pulse"/>
    <circle cx="{x}" cy="{y}" r="{core * 2}" fill="{COL[color]}" opacity=".35"/>
    <circle cx="{x}" cy="{y}" r="{core}" fill="#fff"/>
  </g>'''


COL = {"blue": "#9cc2ff", "amber": "#ffd28a", "teal": "#8ff0d6"}

lines_svg, d = [], 0.4
for a, b in sec_lines:
    lines_svg.append(line(a, b, d)); d += 0.18
d = 0.9
for a, b in fs_lines:
    lines_svg.append(line(a, b, d)); d += 0.18

minors = [minor(p, 0.2 + i * 0.07) for i, p in enumerate(sec_minor + fs_minor)]

# BGPShield: glow, spikes, rotating reticle
bx, by = BGP
bgp = f'''<g class="pop" style="animation-delay:.1s">
    <circle cx="{bx}" cy="{by}" r="62" fill="url(#glow-blue)" class="pulse"/>
    <g class="spikes">
      <path d="M{bx - 72} {by}H{bx + 72}" stroke="url(#spikeH)" stroke-width="1.8"/>
      <path d="M{bx} {by - 72}V{by + 72}" stroke="url(#spikeV)" stroke-width="1.8"/>
      <path d="M{bx - 22} {by - 22}L{bx + 22} {by + 22}M{bx - 22} {by + 22}L{bx + 22} {by - 22}" stroke="#cfe0ff" stroke-width=".6" opacity=".35"/>
    </g>
    <circle cx="{bx}" cy="{by}" r="11" fill="#9cc2ff" opacity=".35"/>
    <circle cx="{bx}" cy="{by}" r="5.2" fill="#fff"/>
    <g class="spin">
      <circle cx="{bx}" cy="{by}" r="30" fill="none" stroke="#9cc2ff" stroke-width=".8" stroke-dasharray="2 5" opacity=".7"/>
    </g>
    <g class="spin-rev">
      <circle cx="{bx}" cy="{by}" r="38" fill="none" stroke="#9cc2ff" stroke-width=".6" stroke-dasharray="26 34" opacity=".45"/>
    </g>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">TanishkaJ26 star chart</title>
  <desc id="d">Two constellations. Internet Security, shaped like a shield, holds BGPShield as its brightest star. Full Stack holds Spotlight and WanderLust. dsa-cpp is a faint star between them.</desc>
  <defs>
    <radialGradient id="sky" cx="38%" cy="40%" r="80%">
      <stop offset="0" stop-color="#141c33"/>
      <stop offset=".55" stop-color="#0a0f1e"/>
      <stop offset="1" stop-color="#04060c"/>
    </radialGradient>
    <radialGradient id="glow-blue"><stop offset="0" stop-color="#bcd6ff" stop-opacity=".55"/><stop offset=".35" stop-color="#6f9eff" stop-opacity=".18"/><stop offset="1" stop-color="#6f9eff" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow-amber"><stop offset="0" stop-color="#ffe2b0" stop-opacity=".5"/><stop offset=".4" stop-color="#ffb04a" stop-opacity=".12"/><stop offset="1" stop-color="#ffb04a" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow-teal"><stop offset="0" stop-color="#c4fff0" stop-opacity=".5"/><stop offset=".4" stop-color="#3fd9b0" stop-opacity=".12"/><stop offset="1" stop-color="#3fd9b0" stop-opacity="0"/></radialGradient>
    <radialGradient id="neb-blue"><stop offset="0" stop-color="#3b5bdb" stop-opacity=".22"/><stop offset="1" stop-color="#3b5bdb" stop-opacity="0"/></radialGradient>
    <radialGradient id="neb-rose"><stop offset="0" stop-color="#b8487a" stop-opacity=".16"/><stop offset="1" stop-color="#b8487a" stop-opacity="0"/></radialGradient>
    <linearGradient id="spikeH" x1="0" x2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="spikeV" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>
    <linearGradient id="tail" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
    <filter id="haze" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <style>
    .cl {{ fill: none; stroke: #8fa9dc; stroke-width: 1; stroke-opacity: .5; stroke-dasharray: 1; animation: draw 1.1s ease-out both; }}
    .pop {{ animation: pop .9s ease-out both; }}
    .tw {{ animation: twinkle 4s ease-in-out infinite; }}
    .tw2 {{ animation-duration: 5.5s; }}
    .tw3 {{ animation-duration: 7s; }}
    .pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 5s ease-in-out infinite; }}
    .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 40s linear infinite; }}
    .spin-rev {{ transform-box: fill-box; transform-origin: center; animation: spin 26s linear infinite reverse; }}
    .spikes {{ animation: shimmer 3.2s ease-in-out infinite; }}
    .meteor {{ opacity: 0; animation: meteor 11s ease-in 2.5s infinite both; }}
    .lbl {{ font-family: {MONO}; animation: pop 1.2s ease-out both; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes pop {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes twinkle {{ 0%, 100% {{ opacity: .9; }} 50% {{ opacity: .15; }} }}
    @keyframes pulse {{ 0%, 100% {{ transform: scale(.88); opacity: .8; }} 50% {{ transform: scale(1.12); opacity: 1; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes shimmer {{ 0%, 100% {{ opacity: .75; }} 50% {{ opacity: 1; }} }}
    @keyframes meteor {{
      0% {{ transform: translate(0, 0); opacity: 0; }}
      1.5% {{ opacity: 1; }}
      9% {{ transform: translate(250px, 125px); opacity: 0; }}
      100% {{ transform: translate(250px, 125px); opacity: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    <ellipse cx="450" cy="200" rx="520" ry="70" fill="#8a9cff" opacity=".07" filter="url(#haze)" transform="rotate(-14 450 200)"/>
    <circle cx="250" cy="190" r="190" fill="url(#neb-blue)"/>
    <circle cx="690" cy="210" r="200" fill="url(#neb-rose)"/>

    <!-- chart grid -->
    <g fill="none" stroke="#9fb3e0" stroke-opacity=".07" stroke-width="1">
      <path d="M0 100H{W}M0 200H{W}M0 300H{W}"/>
      <path d="M150 0Q170 200 150 {H}M300 0Q312 200 300 {H}M450 0V{H}M600 0Q588 200 600 {H}M750 0Q730 200 750 {H}"/>
    </g>
    <path d="M-10 250C200 150 420 360 640 250S860 160 910 190" fill="none" stroke="#c9a86a" stroke-opacity=".18" stroke-dasharray="3 6"/>
    <text x="26" y="234" fill="#c9a86a" fill-opacity=".45" font-size="8" letter-spacing="3" font-family="{MONO}">ECLIPTIC</text>

    <g>{"".join(bg)}</g>

    <!-- meteor -->
    <g class="meteor"><path d="M340 6L420 46" stroke="url(#tail)" stroke-width="1.4" stroke-linecap="round"/><circle cx="420" cy="46" r="1.6" fill="#fff"/></g>

    <!-- constellation lines -->
    <g>{"".join(lines_svg)}</g>
    <g>{"".join(minors)}</g>

    <!-- named stars -->
    {bgp}
    {bright(SPOT, "amber", 3.6, 30, 1.4)}
    {bright(WAND, "teal", 3.4, 28, 1.7)}
    <circle cx="{DSA[0]}" cy="{DSA[1]}" r="1.6" fill="#dfe8ff" class="tw tw3" style="animation-delay:2s"/>

    <!-- labels -->
    <g class="lbl" style="animation-delay:.6s">
      <text x="250" y="52" fill="#7f95c8" font-size="11" letter-spacing="5" text-anchor="middle">INTERNET SECURITY</text>
      <text x="686" y="78" fill="#c88fa9" font-size="11" letter-spacing="5" text-anchor="middle">FULL STACK</text>
    </g>
    <g class="lbl" style="animation-delay:1.2s">
      <text x="250" y="240" fill="#f1f5ff" font-size="19" font-weight="700" text-anchor="middle">BGPShield</text>
      <text x="250" y="258" fill="#9cb4e6" font-size="9.5" letter-spacing="2.5" text-anchor="middle">α · RPKI / ASPA</text>
      <text x="594" y="168" fill="#fff1dc" font-size="14" font-weight="600" text-anchor="end">Spotlight</text>
      <text x="786" y="286" fill="#dcfff6" font-size="14" font-weight="600" text-anchor="middle">WanderLust</text>
      <text x="478" y="338" fill="#8b98b8" font-size="10">dsa-cpp</text>
    </g>

    <!-- chart furniture -->
    <g font-family="{MONO}" font-size="8.5" letter-spacing="2" fill="#6f7fa6">
      <text x="22" y="30">STAR CHART · TANISHKAJ26</text>
      <text x="{W - 22}" y="30" text-anchor="end">EPOCH J2000</text>
      <text x="22" y="{H - 20}">OBSERVED FROM 28.61°N 77.21°E</text>
    </g>
    <g font-family="{MONO}" font-size="8.5" letter-spacing="1.5" fill="#6f7fa6">
      <circle cx="{W - 250}" cy="{H - 23}" r="4" fill="#fff"/><text x="{W - 240}" y="{H - 20}">RESEARCH</text>
      <circle cx="{W - 160}" cy="{H - 23}" r="2.6" fill="#fff"/><text x="{W - 151}" y="{H - 20}">LIVE</text>
      <circle cx="{W - 104}" cy="{H - 23}" r="1.4" fill="#fff"/><text x="{W - 96}" y="{H - 20}">IN PROGRESS</text>
    </g>
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#2a3558" stroke-opacity=".8"/>
  </g>
</svg>
'''

with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write(svg)
