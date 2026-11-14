"""Generate animated terminal-style banner.svg and footer.svg for the GitHub profile."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0D1117"
PANEL = "#161B22"
BORDER = "#30363D"
GREEN = "#39D353"
ORANGE = "#FF9F43"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
CW = 10.2  # approx char width at 17px monospace


def kt(t, total):
    return round(t / total, 4)


def typed_line(idx, x, y, segments, start, total, typing=True, cps=22, end_hold=None):
    """A line revealed char by char via an animated clip rect.
    segments: list of (text, color). Returns (svg, finish_time)."""
    text_len = sum(len(s) for s, _ in segments)
    width = text_len * CW + 14
    dur_type = text_len / cps if typing else 0.01
    finish = start + dur_type
    # discrete width steps
    if typing:
        steps = max(1, text_len)
        times = [0, kt(start, total)]
        widths = [0, 0]
        for i in range(1, steps + 1):
            t = start + dur_type * i / steps
            times.append(kt(t, total))
            widths.append(round(i * CW + 2, 1))
        times.append(1)
        widths.append(widths[-1])
    else:
        times = [0, kt(start, total), 1]
        widths = [0, width, width]
    # make sure keyTimes strictly non-decreasing and unique-ish
    vals = ";".join(str(w) for w in widths)
    kts = ";".join(str(t) for t in times)
    tspans = "".join(
        f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in segments
    )
    svg = (
        f'<clipPath id="c{idx}"><rect x="{x - 2}" y="{y - 16}" height="24" width="0">'
        f'<animate attributeName="width" values="{vals}" keyTimes="{kts}" '
        f'dur="{total}s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>'
        f'<text x="{x}" y="{y}" clip-path="url(#c{idx})" xml:space="preserve">{tspans}</text>'
    )
    return svg, finish


def banner():
    W, H = 1200, 340
    TOTAL = 16
    tx, ty0, lh = 72, 112, 27
    P = GREEN
    lines = [
        ([("naufal@cloud", P), (":", TEXT), ("~", "#58A6FF"), ("$ ", TEXT), ("whoami", TEXT)], True),
        ([("Naufal Rafif Hidayat", ORANGE), (" · Informatics @ Telkom University", TEXT)], False),
        ([("naufal@cloud", P), (":", TEXT), ("~", "#58A6FF"), ("$ ", TEXT), ("cat focus.txt", TEXT)], True),
        ([("cloud", TEXT), ("  /  ", MUTED), ("ai-ml", TEXT), ("  /  ", MUTED), ("automation", TEXT), ("   # what I care about", MUTED)], False),
        ([("naufal@cloud", P), (":", TEXT), ("~", "#58A6FF"), ("$ ", TEXT), ("./deploy.sh --profile", TEXT)], True),
    ]
    parts = []
    t = 0.6
    y = ty0
    for i, (segs, typing) in enumerate(lines):
        svg, fin = typed_line(i, tx, y, segs, t, TOTAL, typing=typing)
        parts.append(svg)
        t = fin + (0.5 if typing else 0.45)
        y += lh
    # progress bar line
    bar_y = y
    bar_start = t
    bar_end = t + 2.0
    bx = tx
    parts.append(
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
        f'keyTimes="0;{kt(bar_start, TOTAL)};{kt(bar_start + 0.01, TOTAL)};1" dur="{TOTAL}s" '
        f'repeatCount="indefinite" calcMode="discrete"/>'
        f'<text x="{bx}" y="{bar_y}" fill="{MUTED}">[</text>'
        f'<rect x="{bx + 14}" y="{bar_y - 12}" height="12" width="0" rx="2" fill="{GREEN}">'
        f'<animate attributeName="width" values="0;0;260;260" '
        f'keyTimes="0;{kt(bar_start, TOTAL)};{kt(bar_end, TOTAL)};1" dur="{TOTAL}s" repeatCount="indefinite"/></rect>'
        f'<text x="{bx + 280}" y="{bar_y}" fill="{MUTED}">]</text></g>'
    )
    done_svg, fin = typed_line(
        99, bx + 300, bar_y, [("[ ok ]", GREEN), (" deployed. welcome to my profile", TEXT)],
        bar_end + 0.2, TOTAL, typing=False,
    )
    parts.append(done_svg)
    # blinking cursor after done
    cur_y = bar_y + lh
    parts.append(
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
        f'keyTimes="0;{kt(fin + 0.4, TOTAL)};{kt(fin + 0.41, TOTAL)};1" dur="{TOTAL}s" '
        f'repeatCount="indefinite" calcMode="discrete"/>'
        f'<text x="{tx}" y="{cur_y}" xml:space="preserve"><tspan fill="{P}">naufal@cloud</tspan>'
        f'<tspan fill="{TEXT}">:</tspan><tspan fill="#58A6FF">~</tspan><tspan fill="{TEXT}">$ </tspan></text>'
        f'<rect x="{tx + 16 * CW}" y="{cur_y - 14}" width="10" height="18" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>'
    )

    # right side: cloud + server rack + packets
    cx, cy = 960, 120
    cloud = (
        f'<g transform="translate({cx - 110},{cy - 70})">'
        f'<path d="M60 120 h120 a40 40 0 0 0 0 -80 a55 55 0 0 0 -104 -12 a42 42 0 0 0 -16 92 z" '
        f'fill="{PANEL}" stroke="{ORANGE}" stroke-width="3" stroke-linejoin="round">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" '
        f'dur="4s" repeatCount="indefinite"/></path>'
        f'<text x="118" y="92" text-anchor="middle" fill="{ORANGE}" font-size="15" font-weight="700">'
        f'AWS · GCP<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" '
        f'dur="4s" repeatCount="indefinite"/></text></g>'
    )
    rack = []
    rx, ry = cx - 70, 205
    for i in range(3):
        yy = ry + i * 30
        rack.append(
            f'<rect x="{rx}" y="{yy}" width="140" height="24" rx="4" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>'
            f'<rect x="{rx + 12}" y="{yy + 10}" width="60" height="4" rx="2" fill="{BORDER}"/>'
        )
        for j, col in enumerate([GREEN, ORANGE]):
            rack.append(
                f'<circle cx="{rx + 110 + j * 14}" cy="{yy + 12}" r="4" fill="{col}">'
                f'<animate attributeName="opacity" values="1;0.2;1" dur="{0.8 + 0.3 * i + 0.25 * j}s" '
                f'repeatCount="indefinite"/></circle>'
            )
    link = (
        f'<line x1="{cx}" y1="200" x2="{cx}" y2="170" stroke="{BORDER}" stroke-width="2" stroke-dasharray="4 4"/>'
    )
    packets = "".join(
        f'<circle r="3.5" cx="{cx}" fill="{GREEN}"><animate attributeName="cy" values="200;168" '
        f'dur="1.2s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" '
        f'values="0;1;0" dur="1.2s" begin="{d}s" repeatCount="indefinite"/></circle>'
        for d in (0, 0.4, 0.8)
    )
    # small Telegram-ish bot bubble to the right
    bot = (
        f'<g transform="translate(1085,215)"><rect width="70" height="36" rx="10" fill="{PANEL}" stroke="{GREEN}" stroke-width="2"/>'
        f'<text x="35" y="23" text-anchor="middle" fill="{GREEN}" font-size="13">bot</text>'
        f'<animateTransform attributeName="transform" type="translate" values="1085 215;1085 209;1085 215" dur="3s" repeatCount="indefinite"/></g>'
        f'<path d="M1032 232 H1083" stroke="{BORDER}" stroke-width="2" stroke-dasharray="4 4"/>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated terminal: naufal@cloud deploying the profile">
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect x="24" y="20" width="{W - 48}" height="{H - 40}" rx="12" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
<path d="M24 32 a12 12 0 0 1 12 -12 h{W - 72} a12 12 0 0 1 12 12 v28 h-{W - 48} z" fill="#21262D"/>
<circle cx="50" cy="40" r="7" fill="#FF5F56"/><circle cx="74" cy="40" r="7" fill="#FFBD2E"/><circle cx="98" cy="40" r="7" fill="#27C93F"/>
<text x="{W / 2}" y="45" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="14">naufal@cloud: ~ — bash</text>
<line x1="790" y1="74" x2="790" y2="300" stroke="{BORDER}" stroke-width="1" stroke-dasharray="3 6"/>
<g font-family="{FONT}" font-size="17">
{''.join(parts)}
</g>
<g font-family="{FONT}">{cloud}{link}{packets}{''.join(rack)}{bot}</g>
</svg>
'''
    (OUT / "banner.svg").write_text(svg, encoding="utf-8")


def footer():
    W, H = 1200, 130
    TOTAL = 9
    tx = 72
    parts = []
    s1, f1 = typed_line(0, tx, 62, [("naufal@cloud", GREEN), (":", TEXT), ("~", "#58A6FF"), ("$ ", TEXT), ("exit", TEXT)], 0.6, TOTAL)
    s2, f2 = typed_line(1, tx, 90, [("logout", MUTED), ("  ·  thanks for stopping by, see you in the cloud", TEXT)], f1 + 0.6, TOTAL, typing=False)
    s3, f3 = typed_line(2, 760, 90, [("Connection to cloud closed. ", MUTED), ("exit 0", GREEN)], f2 + 0.8, TOTAL, typing=False)
    parts += [s1, s2, s3]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal session ending: exit 0">
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect x="24" y="16" width="{W - 48}" height="{H - 32}" rx="12" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
<rect x="24" y="16" width="5" height="{H - 32}" rx="2" fill="{GREEN}"/>
<g font-family="{FONT}" font-size="17">{''.join(parts)}</g>
<rect x="{1120}" y="48" width="10" height="18" fill="{ORANGE}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
</svg>
'''
    (OUT / "footer.svg").write_text(svg, encoding="utf-8")


banner()
footer()
print("ok")
