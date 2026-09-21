"""
Hand-author a neofetch-style info card SVG: title bar + colored key/value rows
that fade and slide in on a short stagger so the panel looks like it's printing
next to the portrait.

Content is Osmoti-forward and accomplishment-heavy (see rahul-mehta.me / osmoti.com).

    python scripts/make_info_card.py
    STATIC=1 python scripts/make_info_card.py   # frozen frame for Quick Look
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

HOST = "rahul@github"
W, H = 490, 875  # matches portrait canvas (make_ascii_svg.py CANVAS_H)

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
CYAN = "#22d3ee"
GREEN = "#3fb950"
PURPLE = "#a371f7"
GOLD = "#f2cc60"
ORANGE = "#ffa657"
PINK = "#f778ba"

PAD = 22
TITLEBAR_H = 30
LINE_H = 26
START_Y = TITLEBAR_H + 36

# (label_color, label, value_color, value) — None label = section spacer / bare line
ROWS = [
    (CYAN, "user", INK, "Rahul Mehta"),
    (CYAN, "title", INK, "Co-Founder & CTO @ Osmoti"),
    (CYAN, "school", INK, "BS Data Science · GT '27 · 4.0"),
    (None, None, MUTED, "-----------------------------"),
    (GREEN, "osmoti", GOLD, "Autonomous Marketing Dept"),
    (GREEN, "build", INK, "iMessage + multi-channel growth"),
    (GREEN, "runs", INK, "ads · social · search · follow-up"),
    (GREEN, "loop", INK, "lead in seconds -> book -> attribute"),
    (None, None, MUTED, "-----------------------------"),
    (PURPLE, "impact", GOLD, "$3M+ efficiency @ Southwire"),
    (PURPLE, "impact", GOLD, "$100K hotel partnership"),
    (PURPLE, "impact", INK, "5K+ AI users · 8 prod prompts"),
    (None, None, MUTED, "-----------------------------"),
    (ORANGE, "prev", INK, "Agent eval infra @ Manhattan"),
    (ORANGE, "also", INK, "Keep Safe / Beach Box Safe"),
    (None, None, MUTED, "-----------------------------"),
    (PINK, "ship", INK, "Smart-Legal-Contracts · NCRC '25"),
    (PINK, "ship", INK, "analytics-pro · MARA · MARTA"),
    (PINK, "pub", INK, "ACMSE '24 synthetic media"),
    (None, None, MUTED, "-----------------------------"),
    (GOLD, "stack", INK, "TS · Python · agents · growth"),
    (GOLD, "up", INK, "Shipping Osmoti to owners"),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" '
    f'fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
    f'text-anchor="middle">{HOST}: ~$ neofetch --osmoti</text>'
)

header_y = START_Y
parts.append(
    f'<text x="{PAD}" y="{header_y}" fill="{CYAN}" font-size="16" font-weight="700">'
    f'{HOST}</text>'
)
parts.append(
    f'<text x="{PAD}" y="{header_y + 20}" fill="{MUTED}" font-size="12">'
    f'-------------------------</text>'
)

row_start = header_y + 44
STAGGER = 0.10
DUR = 0.32

for i, (lcol, label, vcol, value) in enumerate(ROWS):
    y = row_start + i * LINE_H
    delay = 0.2 + i * STAGGER
    safe_value = html.escape(value)
    if label is None:
        text = f'<text x="{PAD}" y="{y}" fill="{vcol}" font-size="12">{safe_value}</text>'
    else:
        text = (
            f'<text x="{PAD}" y="{y}" font-size="12">'
            f'<tspan fill="{lcol}" font-weight="700">{html.escape(label)}</tspan>'
            f'<tspan fill="{MUTED}">:  </tspan>'
            f'<tspan fill="{vcol}">{safe_value}</tspan></text>'
        )

    if STATIC:
        parts.append(text)
        continue

    parts.append(
        f'<g opacity="0" transform="translate(0,8)">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
        f'dur="{DUR:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 8" to="0 0" begin="{delay:.2f}s" dur="{DUR:.2f}s" fill="freeze"/>'
        f'{text}</g>'
    )

prompt_y = H - 28
parts.append(
    f'<text x="{PAD}" y="{prompt_y}" fill="{MUTED}" font-size="12">'
    f'{HOST}:~$ <tspan fill="{INK}">open https://osmoti.com</tspan></text>'
)
parts.append(
    f'<rect x="{PAD + 292}" y="{prompt_y - 11}" width="8" height="13" fill="{INK}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/></rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H)
