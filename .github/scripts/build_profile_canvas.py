"""Build unified 880x1340 Japanese Neon Sunset GitHub profile SVG with big neon GitHub logo & live Platane/snk snake."""

import base64
import re
import sys
from pathlib import Path

BG_PATH = Path(__file__).resolve().parent / "tokyo_sunset_bg.jpg"

FONT_5X7 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "00000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "00000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "@": ["01110", "10001", "10111", "10101", "10110", "10000", "01110"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
}

JP_7X7 = {
    "東": ["0001000", "1111111", "0111110", "0101010", "0111110", "0011100", "1101011"],
    "京": ["0001000", "1111111", "0111110", "0100010", "0111110", "0001000", "1011001"],
    "ア": ["1111111", "0000010", "0001100", "0001000", "0001000", "0010000", "0100000"],
    "リ": ["0100010", "0100010", "0100010", "0100010", "0000010", "0000100", "0001000"],
    "ガ": ["0010011", "1111100", "0010010", "0010010", "0100010", "1000100", "0000000"],
    "ト": ["0010000", "0010000", "0011000", "0010100", "0010010", "0010000", "0010000"],
    "ウ": ["0001000", "0111110", "0100010", "0100010", "0000010", "0000100", "0011000"],
}

MINI_SNAKE_ICON = [
    "..CCCC..",
    ".CCWCCC.",
    ".CCCCCC.",
    "..PPPP..",
    "...PPP..",
    "..VVV...",
    ".GGG....",
    "..GG....",
]


def text_width(text: str, scale: int = 2, gap: int = 1) -> int:
    if not text:
        return 0
    return len(text) * 5 * scale + (len(text) - 1) * gap * scale


def pixel_text_path(text: str, x: int, y: int, scale: int = 2, gap: int = 1) -> str:
    cmds = []
    cx = x
    step = (5 + gap) * scale
    for ch in text.upper():
        glyph = FONT_5X7.get(ch, FONT_5X7[" "])
        for r, row in enumerate(glyph):
            c = 0
            while c < 5:
                if row[c] == "1":
                    start = c
                    while c < 5 and row[c] == "1":
                        c += 1
                    w = (c - start) * scale
                    cmds.append(f"M{cx + start * scale},{y + r * scale}h{w}v{scale}h-{w}z")
                else:
                    c += 1
        cx += step
    return "".join(cmds)


def jp_text_path(text: str, x: int, y: int, scale: int = 2, gap: int = 2) -> str:
    cmds = []
    cx = x
    step = (7 + gap) * scale
    for ch in text:
        glyph = JP_7X7.get(ch)
        if glyph:
            for r, row in enumerate(glyph):
                c = 0
                while c < 7:
                    if row[c] == "1":
                        start = c
                        while c < 7 and row[c] == "1":
                            c += 1
                        w = (c - start) * scale
                        cmds.append(f"M{cx + start * scale},{y + r * scale}h{w}v{scale}h-{w}z")
                    else:
                        c += 1
        cx += step
    return "".join(cmds)


def render_sprite(grid: list[str], palette: dict[str, str], x: int, y: int, px: int = 3) -> str:
    by_col: dict[str, list[str]] = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in palette:
                by_col.setdefault(palette[ch], []).append(f"M{x + c * px},{y + r * px}h{px}v{px}h-{px}z")
    return "".join(
        f'<path d="{"".join(cmds)}" fill="{color}" shape-rendering="crispEdges"/>'
        for color, cmds in by_col.items()
    )


def sakura_petals_svg(petals: list[tuple[int, int, str, str, int]]) -> str:
    elems = []
    for px, py, col, dur, dx in petals:
        elems.append(
            f'<g shape-rendering="crispEdges">'
            f'<rect x="{px}" y="{py}" width="4" height="4" fill="{col}" opacity="0.88">'
            f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx},70;{dx*2},140" dur="{dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.9;0" dur="{dur}" repeatCount="indefinite"/>'
            f'</rect>'
            f'<rect x="{px+3}" y="{py+3}" width="3" height="3" fill="#ffd6ea" opacity="0.72">'
            f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx},70;{dx*2},140" dur="{dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.75;0.75;0" dur="{dur}" repeatCount="indefinite"/>'
            f'</rect>'
            f'</g>'
        )
    return "".join(elems)


def divider_bar(y: int, W: int = 880) -> str:
    blocks = []
    colors = ["#ff2a85", "#ff7eb6", "#ffd166", "#00f5d4", "#9d4edd", "#00f5d4", "#ffd166", "#ff7eb6"]
    cx = 30
    idx = 0
    while cx < W - 38:
        col = colors[idx % len(colors)]
        blocks.append(f'<rect x="{cx}" y="{y}" width="12" height="5" fill="{col}" opacity="0.9"/>')
        cx += 18
        idx += 1
    return (
        f'<line x1="20" y1="{y+2}" x2="{W-20}" y2="{y+2}" stroke="#4a1c7a" stroke-opacity="0.65" stroke-width="1.5"/>'
        f'<g shape-rendering="crispEdges">{"".join(blocks)}</g>'
        f'<rect x="20" y="{y-2}" width="32" height="9" fill="#ff7eb6" opacity="0.95" shape-rendering="crispEdges">'
        f'<animate attributeName="x" values="20;{W-52};20" dur="5.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )


def neon_github_sign_svg(cx: int, cy: int, scale: float = 9.2) -> str:
    """Build a big Neon Pink GitHub Octocat tube sign (modeled on Reference 2)."""
    # Official GitHub Octocat mark in 24x24 viewBox (center ~12,12)
    octocat_d = (
        "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385"
        ".6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61"
        "-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084"
        "-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998"
        ".108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465"
        "-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23"
        ".96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285"
        "-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22"
        " 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015"
        " 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297"
        "c0-6.627-5.373-12-12-12"
    )
    tx = cx - 12 * scale
    ty = cy - 12 * scale
    r_disc = 12.6 * scale
    r_ring = 11.8 * scale

    return f'''  <!-- BIG NEON GITHUB OCTOCAT TUBE SIGN (Centerpiece) -->
  <g>
    <!-- Ambient Magenta Halo & Frosted Acrylic Disc -->
    <circle cx="{cx}" cy="{cy}" r="{r_disc + 18:.1f}" fill="#ff2a85" opacity="0.16" filter="url(#bigNeonHalo)"/>
    <circle cx="{cx}" cy="{cy}" r="{r_disc:.1f}" fill="#140724" fill-opacity="0.52" stroke="#ff7ce5" stroke-opacity="0.55" stroke-width="1.6"/>
    <!-- Outer Neon Circle Tube -->
    <circle cx="{cx}" cy="{cy}" r="{r_ring:.1f}" fill="none" stroke="#ff2a85" stroke-width="10" filter="url(#neonTubeGlow)"/>
    <circle cx="{cx}" cy="{cy}" r="{r_ring:.1f}" fill="none" stroke="#ffe6fa" stroke-width="3.6"/>
    <!-- Octocat Neon Tube Outline (Dark inner mask + Outer pink glow + White-hot tube core) -->
    <g transform="translate({tx:.1f},{ty:.1f}) scale({scale:.3f})">
      <path d="{octocat_d}" fill="#0d061c" fill-opacity="0.72" stroke="#ff2a85" stroke-width="1.35" stroke-linejoin="round" filter="url(#neonTubeGlow)"/>
      <path d="{octocat_d}" fill="none" stroke="#fff0fc" stroke-width="0.46" stroke-linejoin="round">
        <animate attributeName="opacity" values="0.92;1;0.88;1" dur="3.2s" repeatCount="indefinite"/>
      </path>
    </g>
  </g>'''


def build_profile_canvas(raw_snake_svg: str) -> str:
    W, H = 880, 1340
    bg_b64 = base64.b64encode(BG_PATH.read_bytes()).decode("ascii")

    # Parse Platane/snk snake SVG
    vb_match = re.search(r'viewBox="([^"]+)"', raw_snake_svg)
    view_box = vb_match.group(1) if vb_match else "-16 -32 880 192"
    inner_match = re.search(r"<svg[^>]*>(.*)</svg>", raw_snake_svg, flags=re.DOTALL)
    if not inner_match:
        raise ValueError("Invalid snake SVG input: missing <svg> wrapper")
    snake_inner = inner_match.group(1)
    snake_inner = re.sub(r"<desc>.*?</desc>", "", snake_inner, flags=re.DOTALL)
    snake_inner = re.sub(r'\s+r[xy]="[0-9.]+"', "", snake_inner)

    override_css = (
        "<style>"
        ":root{--ce:#0e1024;--cb:#3a215e;--c0:#0e1024;--c1:#4a0e4e;--c2:#9d4edd;--c3:#ff7eb6;--c4:#ffd166}"
        ".c{shape-rendering:crispEdges !important;stroke-width:1px;stroke:var(--cb);fill-opacity:0.68}"
        ".c.c1,.c.c2,.c.c3,.c.c4{stroke:#ffffff30;fill-opacity:1}"
        ".u{shape-rendering:crispEdges !important}"
        ".s{shape-rendering:crispEdges !important}"
        ".s.s0{fill:#00f5d4 !important;filter:url(#snakeGlow)}"
        ".s.s1{fill:#ff2a85 !important;filter:url(#snakeGlow)}"
        ".s.s2{fill:#ff7eb6 !important}"
        ".s.s3{fill:#ffd166 !important}"
        "</style>"
    )
    snake_inner = snake_inner.replace("</style>", "</style>" + override_css, 1)

    # --- SECTION 1: HERO (y = 14..210) ---
    title = "CAHYO WISANGGENI"
    tw = text_width(title, 5, 1)
    tx = (W - tw) // 2
    ty = 76
    sub = "STATISTICS STUDENT // ML & LOCAL AI BUILDER"
    sw = text_width(sub, 2, 1)
    sx = (W - sw) // 2
    sy = 132
    hud_l = "P1:@CAHYO-WISANGGENI"
    hud_r = "TOKYO-NET // SYS:ONLINE"
    press = "> PRESS START TO EXPLORE REPOS _"
    pw = text_width(press, 2, 1)
    px = (W - pw) // 2

    # --- SECTION 2: PLAYER CARD (y = 224..394, centered cleanly over upper sky) ---
    card_w = 460
    card_x = (W - card_w) // 2
    card_header = pixel_text_path("PLAYER CARD // NEO-TOKYO ARCADE", card_x + 18, 240, scale=2, gap=1)
    card_jp = jp_text_path("東京", card_x + card_w - 52, 240, scale=2, gap=4)
    card_rows = []
    cy = 278
    for label, val, col in [
        ("NAME", "CAHYO WISANGGENI", "#00f5d4"),
        ("ROLE", "STATISTICS STUDENT", "#f8f9fa"),
        ("BASE", "EARTH (UTC+7)", "#ff2a85"),
    ]:
        card_rows.append(f'<path d="{pixel_text_path(label + ":", card_x + 22, cy, 2, 1)}" fill="#ffd166"/>')
        card_rows.append(f'<path d="{pixel_text_path(val, card_x + 108, cy, 2, 1)}" fill="{col}"/>')
        cy += 36
    hanko_jp = jp_text_path("東京", card_x + card_w - 64, 353, scale=2, gap=2)

    # --- SECTION 3: BIG NEON GITHUB LOGO CENTERPIECE (y = 416..684) ---
    github_center = neon_github_sign_svg(cx=440, cy=548, scale=9.2)

    # --- SECTION 4: CONTRIBUTION SNAKE ARCADE (y = 706..964) ---
    snake_title = pixel_text_path("SNAKE.EXE // TOKYO ARCADE", 64, 726, scale=2, gap=1)
    mini_snake = render_sprite(
        MINI_SNAKE_ICON,
        {"C": "#00f5d4", "W": "#ffffff", "P": "#ff2a85", "V": "#ff7eb6", "G": "#ffd166"},
        30,
        721,
        px=3,
    )
    legend_colors = ["#0e1024", "#4a0e4e", "#9d4edd", "#ff7eb6", "#ffd166"]
    legend_elems = [f'<path d="{pixel_text_path("LESS", 564, 726, 2, 1)}" fill="#cbd5e1"/>']
    lx = 618
    for col in legend_colors:
        legend_elems.append(f'<rect x="{lx}" y="727" width="12" height="12" fill="{col}" stroke="#4a1c7a" stroke-width="1"/>')
        lx += 16
    legend_elems.append(f'<path d="{pixel_text_path("MORE", lx + 4, 726, 2, 1)}" fill="#cbd5e1"/>')
    badge_x = lx + 4 + text_width("MORE", 2, 1) + 16
    legend_elems.append(
        f'<rect x="{badge_x}" y="722" width="48" height="22" rx="3" fill="#170f2e" stroke="#ff2a85" stroke-width="1.5"/>'
        f'<path d="{jp_text_path("東京", badge_x + 8, 726, scale=2, gap=2)}" fill="#ffd166">'
        f'<animate attributeName="opacity" values="1;0.45;1" dur="1.6s" repeatCount="indefinite"/>'
        f'</path>'
    )
    foot_l = pixel_text_path("GRID: 52W X 7D", 32, 937, scale=2, gap=1)
    foot_c = pixel_text_path("SAKURA-SERPENT MK.II", 262, 937, scale=2, gap=1)
    foot_r_txt = "STATUS: HUNTING COMMITS"
    foot_r_x = W - 46 - text_width(foot_r_txt, 2, 1)
    foot_r = pixel_text_path(foot_r_txt, foot_r_x, 937, scale=2, gap=1)

    # --- SECTION 5: TOKYO ALLEYWAY ENDING (y = 1030..1120, keeping Torii & lanterns visible below!) ---
    end_txt = "STAGE CLEAR //"
    arigatou = "アリガトウ"
    etw = text_width(end_txt, 2, 1)
    eaw = len(arigatou) * 18 - 4
    etotal = etw + 12 + eaw
    etx = (W - etotal) // 2
    eax = etx + etw + 12

    sub_end = "> SEE YOU NEXT COMMIT _"
    esw = text_width(sub_end, 2, 1)
    esx = (W - esw) // 2

    all_petals = sakura_petals_svg([
        (210, 48, "#ff7eb6", "4.8s", 20),
        (640, 52, "#ffd166", "5.2s", 16),
        (330, 420, "#ff7eb6", "5.0s", 18),
        (560, 430, "#ff2a85", "4.6s", 14),
        (260, 990, "#ff7eb6", "4.9s", 14),
        (610, 1000, "#ffd166", "5.3s", 16),
    ])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cahyo Wisanggeni Neo-Tokyo Neon Sunset Profile">
  <defs>
    <linearGradient id="neonBorder" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff2a85"/>
      <stop offset="50%" stop-color="#ffd166"/>
      <stop offset="100%" stop-color="#00f5d4"/>
    </linearGradient>
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowPink" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="neonTubeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="blur1"/>
      <feGaussianBlur stdDeviation="2.2" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="blur2"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="bigNeonHalo" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="snakeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="canvasClip">
      <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14"/>
    </clipPath>
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000000" opacity="0.12"/>
    </pattern>
  </defs>

  <!-- Full-Canvas Japanese Neon Pixel Sunset Cityscape -->
  <g clip-path="url(#canvasClip)">
    <image href="data:image/jpeg;base64,{bg_b64}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
    <!-- Subtle top vignette for crisp Hero legibility -->
    <rect x="0" y="0" width="{W}" height="220" fill="#060412" opacity="0.24"/>

    <!-- ==================== SECTION 1: HERO ==================== -->
    <rect x="16" y="14" width="{W-32}" height="30" rx="4" fill="#09071a" fill-opacity="0.82" stroke="#4a1c7a" stroke-width="1.5"/>
    <path d="{pixel_text_path(hud_l, 28, 22, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges"/>
    <path d="{pixel_text_path(hud_r, W - 28 - text_width(hud_r, 2, 1) - 18, 22, 2, 1)}" fill="#00f5d4" shape-rendering="crispEdges"/>
    <rect x="{W-38}" y="23" width="10" height="10" fill="#00f5d4" shape-rendering="crispEdges">
      <animate attributeName="opacity" values="1;0.15;1" dur="1.2s" repeatCount="indefinite"/>
    </rect>

    <path d="{pixel_text_path(title, tx, ty, 5, 1)}" fill="#070514" stroke="#070514" stroke-width="6" stroke-linejoin="miter" shape-rendering="crispEdges"/>
    <path d="{pixel_text_path(title, tx+4, ty+4, 5, 1)}" fill="#ff2a85" opacity="0.95" shape-rendering="crispEdges" filter="url(#glowPink)"/>
    <path d="{pixel_text_path(title, tx, ty, 5, 1)}" fill="#00f5d4" shape-rendering="crispEdges" filter="url(#glowCyan)"/>

    <rect x="{sx - 18}" y="{sy - 10}" width="{sw + 36}" height="34" rx="4" fill="#09071a" fill-opacity="0.88" stroke="#ff2a85" stroke-width="2"/>
    <path d="{pixel_text_path(sub, sx, sy, 2, 1)}" fill="#f8f9fa" shape-rendering="crispEdges"/>

    <rect x="{px - 16}" y="178" width="{pw + 32}" height="24" rx="4" fill="#09071a" fill-opacity="0.88" stroke="#4a1c7a" stroke-width="1"/>
    <path d="{pixel_text_path(press, px, 183, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges">
      <animate attributeName="opacity" values="1;1;0.68;1" dur="1.8s" repeatCount="indefinite"/>
    </path>

    <!-- ==================== SECTION 2: PLAYER CARD ==================== -->
    <rect x="{card_x}" y="224" width="{card_w}" height="168" rx="10" fill="#09071a" fill-opacity="0.88" stroke="url(#neonBorder)" stroke-width="2"/>
    <rect x="{card_x + 10}" y="233" width="{card_w - 20}" height="28" rx="4" fill="#110d29" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1"/>
    <path d="{card_header}" fill="#00f5d4" shape-rendering="crispEdges"/>
    <path d="{card_jp}" fill="#ff7eb6" shape-rendering="crispEdges"/>
    <g shape-rendering="crispEdges">{"".join(card_rows)}</g>
    <rect x="{card_x + card_w - 74}" y="347" width="48" height="28" rx="3" fill="#170a24" stroke="#ff2a85" stroke-width="1.5"/>
    <path d="{hanko_jp}" fill="#ff2a85" shape-rendering="crispEdges"/>

    <!-- ==================== SECTION 3: BIG NEON GITHUB LOGO CENTERPIECE ==================== -->
{github_center}

    <!-- ==================== SECTION 4: CONTRIBUTION SNAKE ARCADE ==================== -->
    <rect x="16" y="706" width="{W-32}" height="258" rx="10" fill="#09071a" fill-opacity="0.82" stroke="url(#neonBorder)" stroke-width="2"/>
    <rect x="26" y="716" width="{W-52}" height="34" rx="4" fill="#0d0f22" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
    {mini_snake}
    <path d="{snake_title}" fill="#00f5d4" shape-rendering="crispEdges"/>
    <g shape-rendering="crispEdges">{"".join(legend_elems)}</g>

    <rect x="26" y="756" width="{W-52}" height="172" rx="6" fill="#080716" fill-opacity="0.72" stroke="#4a1c7a" stroke-width="1.5"/>
    <rect x="41" y="913" width="798" height="15" rx="2" fill="#0d1024" fill-opacity="0.88" stroke="#4a1c7a" stroke-width="1"/>

    <svg x="28" y="750" width="824" height="180" viewBox="{view_box}">
      {snake_inner}
    </svg>

    <rect x="26" y="932" width="{W-52}" height="24" rx="4" fill="#0d0f22" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
    <g shape-rendering="crispEdges">
      <path d="{foot_l}" fill="#ff7eb6"/>
      <path d="{foot_c}" fill="#ffd166"/>
      <path d="{foot_r}" fill="#00f5d4"/>
      <rect x="{W - 38}" y="939" width="10" height="10" fill="#ff2a85">
        <animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/>
      </rect>
    </g>

    {divider_bar(982, W)}

    <!-- ==================== SECTION 5: ALLEYWAY ENDING ==================== -->
    <rect x="{(W - etotal - 44)//2}" y="1030" width="{etotal + 44}" height="34" rx="4" fill="#09071a" fill-opacity="0.88" stroke="#ff2a85" stroke-width="1.5"/>
    <path d="{pixel_text_path(end_txt, etx, 1040, 2, 1)}" fill="#00f5d4" shape-rendering="crispEdges"/>
    <path d="{jp_text_path(arigatou, eax, 1040, scale=2, gap=2)}" fill="#ff7eb6" shape-rendering="crispEdges"/>

    <rect x="{esx - 18}" y="1076" width="{esw + 36}" height="26" rx="4" fill="#070614" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.2"/>
    <path d="{pixel_text_path(sub_end, esx, 1082, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges">
      <animate attributeName="opacity" values="1;1;0.68;1" dur="1.8s" repeatCount="indefinite"/>
    </path>

    {all_petals}
    <rect x="4" y="4" width="{W-8}" height="{H-8}" rx="12" fill="url(#scanlines)" pointer-events="none"/>
  </g>

  <!-- Outer Arcade Neon Frame -->
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="none" stroke="url(#neonBorder)" stroke-width="3"/>
  <g shape-rendering="crispEdges">
    <rect x="10" y="10" width="5" height="5" fill="#ff2a85"/>
    <rect x="{W-15}" y="10" width="5" height="5" fill="#00f5d4"/>
    <rect x="10" y="{H-15}" width="5" height="5" fill="#00f5d4"/>
    <rect x="{W-15}" y="{H-15}" width="5" height="5" fill="#ff2a85"/>
  </g>
</svg>'''


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: build_profile_canvas.py <raw_snake.svg> <output.svg>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.write_text(build_profile_canvas(src.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Unified Neon Tokyo GitHub Profile SVG written to {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
