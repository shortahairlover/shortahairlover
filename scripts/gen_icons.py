"""Generate section header and project icon SVGs (replacing emoji in the README).

Usage: python scripts/gen_icons.py   (run from the repo root)
"""
import random
from pathlib import Path

BG = "#0D1117"
PANEL = "#161B22"
BORDER = "#30363D"
GREEN = "#39D353"
ORANGE = "#FF9F43"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

ROOT = Path(__file__).resolve().parent.parent
HEAD_DIR = ROOT / "assets" / "headers"
ICON_DIR = ROOT / "assets" / "icons"
HEAD_DIR.mkdir(parents=True, exist_ok=True)
ICON_DIR.mkdir(parents=True, exist_ok=True)

# ---- 24x24 line icons (stroke-based) ---------------------------------------
GLYPHS = {
    "terminal": '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M6.5 9.5l3 2.5-3 2.5M12 15h5"/>',
    "layers": '<path d="M12 3l9 4.5-9 4.5-9-4.5z"/><path d="M3 12l9 4.5 9-4.5"/><path d="M3 16.5l9 4.5 9-4.5"/>',
    "cube": '<path d="M12 2.8l8 4.6v9.2l-8 4.6-8-4.6V7.4z"/><path d="M4 7.4l8 4.6 8-4.6M12 12v9.2"/>',
    "branch": '<circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="8" r="2.2"/><path d="M6 7.2v9.6M18 10.2c0 4-4 4.5-10.2 7.4"/>',
    "chart": '<path d="M3.5 20.5h17"/><rect x="5" y="12" width="3" height="6" rx=".8"/><rect x="10.5" y="7" width="3" height="11" rx=".8"/><rect x="16" y="9.5" width="3" height="8.5" rx=".8"/>',
    "signal": '<circle cx="12" cy="11" r="1.8"/><path d="M12 12.8V21M8.2 7.2a5.4 5.4 0 0 0 0 7.6M15.8 7.2a5.4 5.4 0 0 1 0 7.6M5.4 4.4a9.4 9.4 0 0 0 0 13.2M18.6 4.4a9.4 9.4 0 0 1 0 13.2"/>',
}


def header(name, glyph, title, comment):
    W, H = 1000, 64
    title_w = len(title) * 14.4
    comment_x = 84 + title_w + 18
    rule_x = comment_x + len(comment) * 9.0 + 22
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
<rect x="4" y="8" width="48" height="48" rx="10" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
<g transform="translate(14 18) scale(1.17)" fill="none" stroke="{GREEN}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>
<text x="72" y="42" font-family="{FONT}" font-size="24" font-weight="700" fill="{TEXT}">{title}</text>
<text x="{comment_x:.0f}" y="41" font-family="{FONT}" font-size="15" fill="{MUTED}">{comment}</text>
<line x1="{min(rule_x, W - 40):.0f}" y1="35" x2="{W - 22}" y2="35" stroke="{BORDER}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
<circle cx="{W - 12}" cy="35" r="4" fill="{ORANGE}"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>
</svg>
'''
    (HEAD_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")


def tile(name, body, label):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="72" height="72" role="img" aria-label="{label}">
<rect x="1" y="1" width="70" height="70" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
{body}
</svg>
'''
    (ICON_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")


def icon_ddpm():
    # 6x6 pixel grid that "denoises" from random noise into a ring
    rnd = random.Random(11)
    n, size, gap, off = 6, 6.4, 1.6, 12.4
    parts = []
    for r in range(n):
        for c in range(n):
            dx, dy = c - 2.5, r - 2.5
            d = (dx * dx + dy * dy) ** 0.5
            target = 1.0 if 1.4 < d < 2.9 else 0.08
            color = ORANGE if (r + c) % 5 == 0 and target > 0.5 else GREEN
            a, b = round(rnd.uniform(0.1, 1), 2), round(rnd.uniform(0.1, 1), 2)
            x, y = off + c * (size + gap), off + r * (size + gap)
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" rx="1.4" fill="{color}" opacity="{target}">'
                f'<animate attributeName="opacity" values="{a};{b};{target};{target};{a}" keyTimes="0;.25;.55;.9;1" '
                f'dur="5s" repeatCount="indefinite"/></rect>'
            )
    return "".join(parts)


def icon_receipt():
    zig = "".join(f"l3 -3 l3 3" for _ in range(5))
    return (
        f'<path d="M21 14h30v40{zig.replace("l3 -3 l3 3", "l-3 -3 l-3 3")}z" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="M27 23h18M27 30h12M27 37h16" stroke="{MUTED}" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M27 45h8" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round"/><path d="M40 45h5" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round"/>'
        f'<rect x="15" y="16" width="42" height="2.4" rx="1.2" fill="{ORANGE}" opacity=".9">'
        f'<animate attributeName="y" values="16;52;16" dur="2.8s" repeatCount="indefinite"/></rect>'
    )


def icon_heart():
    heart = "M36 55 C20 44 13 36 13 27 a10 10 0 0 1 23 -5 a10 10 0 0 1 23 5 C59 36 52 44 36 55z"
    pulse = "M14 36h11l4 -8 6 15 5 -11 3 4h15"
    return (
        f'<path d="{heart}" fill="none" stroke="{BORDER}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="{pulse}" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" '
        f'stroke-dasharray="70" stroke-dashoffset="70"><animate attributeName="stroke-dashoffset" values="70;0;0;-70" '
        f'keyTimes="0;.45;.7;1" dur="2.4s" repeatCount="indefinite"/></path>'
        f'<circle cx="58" cy="36" r="2.6" fill="{ORANGE}"><animate attributeName="opacity" values="0;0;1;0" keyTimes="0;.4;.5;1" dur="2.4s" repeatCount="indefinite"/></circle>'
    )


def icon_music():
    bars = []
    for i, (lo, hi, d) in enumerate([(6, 18, 0.9), (10, 26, 1.1), (4, 14, 0.8), (8, 22, 1.3)]):
        x = 40 + i * 6
        bars.append(
            f'<rect x="{x}" width="3.4" rx="1.7" fill="{ORANGE if i == 1 else GREEN}" y="{52 - lo}" height="{lo}">'
            f'<animate attributeName="height" values="{lo};{hi};{lo}" dur="{d}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{52 - lo};{52 - hi};{52 - lo}" dur="{d}s" repeatCount="indefinite"/></rect>'
        )
    note = (
        f'<path d="M30 46V20l-12 3v26" fill="none" stroke="{GREEN}" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<ellipse cx="14.5" cy="49" rx="4.5" ry="3.6" fill="{GREEN}"/><ellipse cx="26.5" cy="46" rx="4.5" ry="3.6" fill="{GREEN}"/>'
    )
    return note + "".join(bars)


def icon_layout():
    blocks = [
        (28, 18, 16, 5, GREEN),
        (28, 26, 16, 9, MUTED),
        (28, 38, 7, 8, ORANGE),
        (37, 38, 7, 8, MUTED),
    ]
    parts = [
        f'<rect x="23" y="11" width="26" height="50" rx="5" fill="none" stroke="{GREEN}" stroke-width="2"/>',
        f'<path d="M32 56h8" stroke="{BORDER}" stroke-width="2" stroke-linecap="round"/>',
    ]
    for i, (x, y, w, h, c) in enumerate(blocks):
        t0 = 0.12 + i * 0.15
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="{c}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.2f};{t0 + 0.08:.2f};.9;1" dur="4s" repeatCount="indefinite"/></rect>'
        )
    return "".join(parts)


def icon_recommender():
    # bipartite user -> item graph; edges light up, then a star rating fills in
    users = [(18, 20), (18, 38)]
    items = [(52, 14), (52, 29), (52, 44)]
    edges = [(0, 0), (0, 2), (1, 1), (1, 2)]
    parts = []
    for i, (u, it) in enumerate(edges):
        (x1, y1), (x2, y2) = users[u], items[it]
        t0 = 0.1 + i * 0.12
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BORDER}" stroke-width="1.6"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="1.8" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.2f};{t0 + 0.08:.2f};.85;1" dur="4s" repeatCount="indefinite"/></line>'
        )
    for x, y in users:
        parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{PANEL}" stroke="{GREEN}" stroke-width="2"/>')
    for i, (x, y) in enumerate(items):
        col = ORANGE if i == 2 else MUTED
        parts.append(f'<rect x="{x - 4.5}" y="{y - 4.5}" width="9" height="9" rx="2" fill="{PANEL}" stroke="{col}" stroke-width="2"/>')
    star = "M0 -4.2 L1.2 -1.3 L4.2 -1.3 L1.8 0.6 L2.7 3.6 L0 1.9 L-2.7 3.6 L-1.8 0.6 L-4.2 -1.3 L-1.2 -1.3 Z"
    for i in range(5):
        cx = 20 + i * 8
        t0 = 0.55 + i * 0.05
        parts.append(
            f'<path d="{star}" transform="translate({cx} 58)" fill="{BORDER}"/>'
            f'<path d="{star}" transform="translate({cx} 58)" fill="{ORANGE}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.2f};{t0 + 0.04:.2f};.85;1" dur="4s" repeatCount="indefinite"/></path>'
        )
    return "".join(parts)


header("about", "terminal", "about_me", "// cat about_me.py")
header("toolbox", "layers", "toolbox", "// ls /usr/local/bin")
header("projects", "cube", "projects", "// things I've shipped")
header("career", "branch", "career", "// git log --oneline")
header("activity", "chart", "activity", "// github stats")
header("contact", "signal", "contact", "// ping naufal")

tile("ddpm", icon_ddpm(), "Diffusion model icon")
tile("sipdana", icon_receipt(), "Receipt scanner icon")
tile("wellnez", icon_heart(), "Heart pulse icon")
tile("lyricshub", icon_music(), "Music icon")
tile("layout", icon_layout(), "Mobile layout icon")
tile("recommender", icon_recommender(), "Recommender system icon")
print("ok")
