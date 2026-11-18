"""Build a unified 880x1040 Japanese Neon Sunset GitHub profile SVG with live Platane/snk snake."""

import re
import sys
from pathlib import Path

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
    "ネ": ["0001000", "1111110", "0000100", "0011000", "1101100", "0001011", "0001000"],
    "オ": ["0001000", "1111111", "0001000", "0011000", "0101000", "1001000", "0011000"],
    "ン": ["0100000", "0010000", "0000001", "0000010", "0000100", "0011000", "1100000"],
}

TORII_SPRITE = [
    "PPPPPPPPPPPPPPPP",
    ".PPPPPPPPPPPPPP.",
    "..P..PPGGPP..P..",
    ".PPPPPPPPPPPPPP.",
    "...P...PP...P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "...P........P...",
    "..CCC......CCC..",
    "..CCC......CCC..",
    "CCCCCCCCCCCCCCCC",
]

PAGODA_SPRITE = [
    ".......GG.......",
    ".......GG.......",
    ".....CCCCCC.....",
    "...CCCCCCCCCC...",
    ".....PPWWPP.....",
    "....CCCCCCCC....",
    "..CCCCCCCCCCCC..",
    "....PPGGGGPP....",
    "...CCCCCCCCCC...",
    ".CCCCCCCCCCCCCC.",
    "...PP..WW..PP...",
    "...PP..WW..PP...",
    "..PPPPPPPPPPPP..",
    "..PPPPGGGGPPPP..",
    ".PPPPPPPPPPPPPP.",
    "CCCCCCCCCCCCCCCC",
]

LANTERN_SPRITE = [
    "...GG...",
    "...GG...",
    "..GGGG..",
    ".PPPPPP.",
    "PPGGGGPP",
    "PPGGGGPP",
    "PPGGGGPP",
    "PPPPPPPP",
    ".PPPPPP.",
    "..GGGG..",
    "...PP...",
    "...PP...",
]

FUJI_SPRITE = [
    "...........WWWWWW...........",
    "..........WWWWWWWW..........",
    ".........WWWWWWWWWW.........",
    "........WWWCWWWWCWWW........",
    ".......VVWVVVWWVVVWVV.......",
    "......VVVVVVVVVVVVVVVV......",
    ".....VVVVVVVVVVVVVVVVVV.....",
    "....VVVVVVVVVVVVVVVVVVVV....",
    "...VVVVVVVVVVVVVVVVVVVVVV...",
    "..VVVVVVVVVVVVVVVVVVVVVVVV..",
    ".VVVVVVVVVVVVVVVVVVVVVVVVVV.",
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVV",
]

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

JP_PALETTE = {
    "P": "#ff2a85",
    "C": "#00f5d4",
    "G": "#ffd166",
    "W": "#ffe5f1",
    "V": "#2c1654",
}


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


def jp_text_path(text: str, x: int, y: int, scale: int = 2, gap: int = 2, vertical: bool = False) -> str:
    cmds = []
    cx, cy = x, y
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
                        cmds.append(f"M{cx + start * scale},{cy + r * scale}h{w}v{scale}h-{w}z")
                    else:
                        c += 1
        if vertical:
            cy += step
        else:
            cx += step
    return "".join(cmds)


def render_sprite(grid: list[str], palette: dict[str, str], x: int, y: int, px: int = 4) -> str:
    by_color: dict[str, list[str]] = {}
    for r, row in enumerate(grid):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch in palette:
                start = c
                while c < len(row) and row[c] == ch:
                    c += 1
                w = (c - start) * px
                by_color.setdefault(palette[ch], []).append(f"M{x + start * px},{y + r * px}h{w}v{px}h-{w}z")
            else:
                c += 1
    return "".join(
        f'<path d="{"".join(cmds)}" fill="{color}" shape-rendering="crispEdges"/>'
        for color, cmds in by_color.items()
    )


def sakura_petals_svg(petals: list[tuple[int, int, str, str, int]]) -> str:
    elems = []
    for px, py, col, dur, dx in petals:
        elems.append(
            f'<g shape-rendering="crispEdges">'
            f'<rect x="{px}" y="{py}" width="4" height="4" fill="{col}" opacity="0.85">'
            f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx},60;{dx*2},120" dur="{dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.9;0.9;0" dur="{dur}" repeatCount="indefinite"/>'
            f'</rect>'
            f'<rect x="{px+3}" y="{py+3}" width="3" height="3" fill="#ffd6ea" opacity="0.7">'
            f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx},60;{dx*2},120" dur="{dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.75;0.75;0" dur="{dur}" repeatCount="indefinite"/>'
            f'</rect>'
            f'</g>'
        )
    return "".join(elems)


def divider_bar(y: int, W: int = 880) -> str:
    blocks = []
    colors = ["#ff2a85", "#ff7eb6", "#ffd166", "#00f5d4", "#9d4edd", "#00f5d4", "#ffd166", "#ff7eb6"]
    cx = 26
    idx = 0
    while cx < W - 34:
        col = colors[idx % len(colors)]
        blocks.append(f'<rect x="{cx}" y="{y}" width="12" height="5" fill="{col}" opacity="0.88"/>')
        cx += 18
        idx += 1
    return (
        f'<line x1="18" y1="{y+2}" x2="{W-18}" y2="{y+2}" stroke="#4a1c7a" stroke-opacity="0.55" stroke-width="1.5"/>'
        f'<g shape-rendering="crispEdges">{"".join(blocks)}</g>'
        f'<rect x="18" y="{y-2}" width="32" height="9" fill="#ff7eb6" opacity="0.95" shape-rendering="crispEdges">'
        f'<animate attributeName="x" values="18;{W-50};18" dur="5.5s" repeatCount="indefinite"/>'
        f'</rect>'
    )


def build_profile_canvas(raw_snake_svg: str) -> str:
    W, H = 880, 1040

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
        ".c{shape-rendering:crispEdges !important;stroke-width:1px;stroke:var(--cb);fill-opacity:0.62}"
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

    # --- GLOBAL SUNSET BACKDROP GRID & STARS ---
    global_grid = "".join(
        f'<line x1="{gx}" y1="4" x2="{gx}" y2="972" stroke="#5b21b6" stroke-opacity="0.16" stroke-width="1"/>'
        for gx in range(44, W, 44)
    ) + "".join(
        f'<line x1="4" y1="{gy}" x2="{W-4}" y2="{gy}" stroke="#5b21b6" stroke-opacity="0.14" stroke-width="1"/>'
        for gy in range(320, 960, 48)
    )
    stars = [
        (95, 52, "#00f5d4", "0s"), (170, 68, "#ffd166", "0.6s"), (245, 48, "#ff7eb6", "1.1s"),
        (635, 48, "#00f5d4", "0.4s"), (710, 62, "#ffd166", "1.3s"), (785, 54, "#ff7eb6", "0.8s"),
        (36, 336, "#ffd166", "0.3s"), (842, 338, "#00f5d4", "0.9s"),
        (36, 588, "#ff7eb6", "0.5s"), (842, 590, "#ffd166", "1.2s"),
    ]
    star_elems = "".join(
        f'<rect x="{sx}" y="{sy}" width="4" height="4" fill="{sc}" shape-rendering="crispEdges">'
        f'<animate attributeName="opacity" values="0.2;1;0.2" dur="2.5s" begin="{sd}" repeatCount="indefinite"/></rect>'
        for sx, sy, sc, sd in stars
    )

    # --- SECTION 1: HERO (y = 14..312) ---
    title = "CAHYO WISANGGENI"
    tw = text_width(title, 5, 1)
    tx = (W - tw) // 2
    ty = 104
    sub = "STATISTICS STUDENT // ML & LOCAL AI BUILDER"
    sw = text_width(sub, 2, 1)
    sx = (W - sw) // 2
    sy = 164
    hud_l = "P1:@CAHYO-WISANGGENI"
    hud_r = "TOKYO-NET // SYS:ONLINE"
    press = "> PRESS START TO EXPLORE REPOS _"
    pw = text_width(press, 2, 1)
    px = (W - pw) // 2

    horizon_hero = 216
    hero_grid = []
    for gx in range(-200, W + 240, 55):
        hero_grid.append(
            f'<line x1="{W//2 + (gx - W//2)//4}" y1="{horizon_hero}" x2="{gx}" y2="306" stroke="#9d4edd" stroke-opacity="0.34" stroke-width="1.5"/>'
        )
    for gy in [216, 228, 244, 264, 286]:
        hero_grid.append(
            f'<line x1="12" y1="{gy}" x2="{W-12}" y2="{gy}" stroke="#9d4edd" stroke-opacity="0.34" stroke-width="1.5"/>'
        )

    skyline = []
    for bx, by, bw, bh in [
        (16, 154, 34, 62), (54, 132, 28, 84), (86, 166, 26, 50), (116, 144, 32, 72),
        (732, 148, 32, 68), (768, 126, 30, 90), (802, 160, 28, 56), (834, 140, 30, 76),
    ]:
        skyline.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#0d0e22" stroke="#4a1c7a" stroke-width="1"/>')
        for wy in range(by + 8, by + bh - 8, 12):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if (wx + wy) % 3 == 0:
                    col = "#00f5d4" if (wx * wy) % 2 == 0 else "#ff2a85"
                    skyline.append(f'<rect x="{wx}" y="{wy}" width="4" height="4" fill="{col}" opacity="0.72"/>')

    hero_clouds = "".join([
        '<rect x="110" y="82" width="68" height="6" fill="#ff758f" opacity="0.68"/>',
        '<rect x="118" y="78" width="50" height="4" fill="#ffd166" opacity="0.58"/>',
        '<rect x="690" y="78" width="76" height="6" fill="#ff8e72" opacity="0.68"/>',
        '<rect x="698" y="74" width="56" height="4" fill="#ffd166" opacity="0.58"/>',
    ])

    hero_fuji = render_sprite(FUJI_SPRITE, JP_PALETTE, 328, 120, px=8)
    hero_torii = render_sprite(TORII_SPRITE, JP_PALETTE, 56, 218, px=4)
    hero_pagoda = render_sprite(PAGODA_SPRITE, JP_PALETTE, W - 56 - 64, 218, px=4)
    hero_lantern_l = render_sprite(LANTERN_SPRITE, JP_PALETTE, 20, 54, px=3)
    hero_lantern_r = render_sprite(LANTERN_SPRITE, JP_PALETTE, W - 44, 54, px=3)

    # --- SECTION 2: PLAYER CARD (y = 348..564) ---
    card_header = pixel_text_path("PLAYER CARD // NEO-TOKYO ARCADE", 34, 367, scale=2, gap=1)
    card_jp = jp_text_path("東京", W - 72, 367, scale=2, gap=4)
    card_rows = []
    cy = 424
    for label, val, col in [
        ("NAME", "CAHYO WISANGGENI", "#00f5d4"),
        ("ROLE", "STATISTICS STUDENT", "#f8f9fa"),
        ("BASE", "EARTH (UTC+7)", "#ff2a85"),
    ]:
        card_rows.append(f'<path d="{pixel_text_path(label + ":", 44, cy, 2, 1)}" fill="#ffd166"/>')
        card_rows.append(f'<path d="{pixel_text_path(val, 138, cy, 2, 1)}" fill="{col}"/>')
        cy += 44
    hanko_jp = jp_text_path("東京", 462, 515, scale=2, gap=2)
    scene_fuji = render_sprite(FUJI_SPRITE, JP_PALETTE, 562, 458, px=7)
    scene_torii = render_sprite(TORII_SPRITE, JP_PALETTE, 740, 478, px=4)
    scene_lantern_l = render_sprite(LANTERN_SPRITE, JP_PALETTE, 536, 404, px=3)
    scene_lantern_r = render_sprite(LANTERN_SPRITE, JP_PALETTE, 822, 404, px=3)

    # --- SECTION 3: SNAKE ARCADE (y = 602..860) ---
    snake_title = pixel_text_path("SNAKE.EXE // TOKYO ARCADE", 64, 622, scale=2, gap=1)
    mini_snake = render_sprite(
        MINI_SNAKE_ICON,
        {"C": "#00f5d4", "W": "#ffffff", "P": "#ff2a85", "V": "#ff7eb6", "G": "#ffd166"},
        30,
        617,
        px=3,
    )
    snake_fuji = render_sprite(
        FUJI_SPRITE,
        {"W": "#ffe5f1", "C": "#00f5d4", "V": "#261247"},
        300,
        700,
        px=10,
    )
    legend_colors = ["#0e1024", "#4a0e4e", "#9d4edd", "#ff7eb6", "#ffd166"]
    legend_elems = [f'<path d="{pixel_text_path("LESS", 564, 622, 2, 1)}" fill="#cbd5e1"/>']
    lx = 618
    for col in legend_colors:
        legend_elems.append(f'<rect x="{lx}" y="623" width="12" height="12" fill="{col}" stroke="#4a1c7a" stroke-width="1"/>')
        lx += 16
    legend_elems.append(f'<path d="{pixel_text_path("MORE", lx + 4, 622, 2, 1)}" fill="#cbd5e1"/>')
    badge_x = lx + 4 + text_width("MORE", 2, 1) + 16
    legend_elems.append(
        f'<rect x="{badge_x}" y="618" width="48" height="22" rx="3" fill="#170f2e" stroke="#ff2a85" stroke-width="1.5"/>'
        f'<path d="{jp_text_path("東京", badge_x + 8, 622, scale=2, gap=2)}" fill="#ffd166">'
        f'<animate attributeName="opacity" values="1;0.45;1" dur="1.6s" repeatCount="indefinite"/>'
        f'</path>'
    )
    foot_l = pixel_text_path("GRID: 52W X 7D", 32, 833, scale=2, gap=1)
    foot_c = pixel_text_path("SAKURA-SERPENT MK.II", 262, 833, scale=2, gap=1)
    foot_r_txt = "STATUS: HUNTING COMMITS"
    foot_r_x = W - 46 - text_width(foot_r_txt, 2, 1)
    foot_r = pixel_text_path(foot_r_txt, foot_r_x, 833, scale=2, gap=1)

    # --- SECTION 4: SUNSET LAKE ENDING (y = 892..1028) ---
    horizon_end = 972
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

    end_ripples = []
    for ry, rw, rcol, rop, rdur in [
        (976, 134, "#ffd166", "0.9", "2.6s"),
        (981, 106, "#ff8c42", "0.8", "3.1s"),
        (986, 78, "#ff2a85", "0.7", "2.8s"),
        (991, 50, "#9d4edd", "0.58", "3.4s"),
    ]:
        rx = (W - rw) // 2
        end_ripples.append(
            f'<rect x="{rx}" y="{ry}" width="{rw}" height="3" fill="{rcol}" opacity="{rop}" shape-rendering="crispEdges">'
            f'<animate attributeName="width" values="{rw};{rw+18};{rw-10};{rw}" dur="{rdur}" repeatCount="indefinite"/>'
            f'<animate attributeName="x" values="{rx};{rx-9};{rx+5};{rx}" dur="{rdur}" repeatCount="indefinite"/>'
            f'</rect>'
        )
    end_torii = render_sprite(TORII_SPRITE, JP_PALETTE, 56, 910, px=4)
    end_pagoda = render_sprite(PAGODA_SPRITE, JP_PALETTE, W - 56 - 64, 910, px=4)
    end_lantern_l = render_sprite(LANTERN_SPRITE, JP_PALETTE, 20, 892, px=3)
    end_lantern_r = render_sprite(LANTERN_SPRITE, JP_PALETTE, W - 44, 892, px=3)

    all_petals = sakura_petals_svg([
        (140, 56, "#ff7eb6", "4.8s", 22),
        (430, 52, "#ff7eb6", "6.0s", 20),
        (720, 66, "#ff2a85", "4.6s", 16),
        (585, 412, "#ff7eb6", "4.5s", 14),
        (760, 416, "#ff2a85", "5.2s", 12),
        (165, 658, "#ff7eb6", "5.0s", 16),
        (685, 662, "#ffd166", "4.7s", 14),
        (220, 896, "#ff7eb6", "4.9s", 14),
        (640, 898, "#ff2a85", "5.3s", 16),
    ])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Cahyo Wisanggeni Japanese Neon Sunset Profile">
  <defs>
    <!-- Continuous Full-Canvas Japanese Neon Sunset Sky & Horizon -->
    <linearGradient id="masterSunset" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0724"/>
      <stop offset="10%" stop-color="#380d54"/>
      <stop offset="17%" stop-color="#9e1f5c"/>
      <stop offset="20.8%" stop-color="#ff8c42"/>
      <stop offset="22%" stop-color="#2c0b47"/>
      <stop offset="35%" stop-color="#4e125c"/>
      <stop offset="48%" stop-color="#a8225c"/>
      <stop offset="56%" stop-color="#5a1359"/>
      <stop offset="72%" stop-color="#9e1f5c"/>
      <stop offset="86%" stop-color="#c92a63"/>
      <stop offset="93.2%" stop-color="#ff8c42"/>
      <stop offset="93.6%" stop-color="#22093a"/>
      <stop offset="100%" stop-color="#070614"/>
    </linearGradient>
    <linearGradient id="sunGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff07c"/>
      <stop offset="48%" stop-color="#ff8c42"/>
      <stop offset="100%" stop-color="#ff2a85"/>
    </linearGradient>
    <linearGradient id="dioramaSunset" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#11082b"/>
      <stop offset="35%" stop-color="#4c1059"/>
      <stop offset="70%" stop-color="#c92a63"/>
      <stop offset="90%" stop-color="#ff7b47"/>
      <stop offset="94%" stop-color="#1f0936"/>
      <stop offset="100%" stop-color="#120624"/>
    </linearGradient>
    <linearGradient id="screenSunset" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d0726"/>
      <stop offset="38%" stop-color="#420e54"/>
      <stop offset="72%" stop-color="#b82460"/>
      <stop offset="92%" stop-color="#ff7e47"/>
      <stop offset="100%" stop-color="#ffb347"/>
    </linearGradient>
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
    <filter id="snakeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="heroSkyClip">
      <rect x="4" y="4" width="{W-8}" height="{horizon_hero - 4}"/>
    </clipPath>
    <clipPath id="endSkyClip">
      <rect x="4" y="886" width="{W-8}" height="{horizon_end - 886}"/>
    </clipPath>
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000000" opacity="0.14"/>
    </pattern>
  </defs>

  <!-- Unified Continuous Japanese Sunset Canvas -->
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="14" fill="url(#masterSunset)"/>
  <g>{global_grid}</g>
  <g>{star_elems}</g>

  <!-- ==================== SECTION 1: HERO ==================== -->
  <g clip-path="url(#heroSkyClip)">
    <g shape-rendering="crispEdges">{hero_clouds}</g>
    <circle cx="440" cy="148" r="80" fill="url(#sunGrad)" opacity="0.76"/>
    <g fill="#6b1659" opacity="0.62">
      <rect x="355" y="142" width="170" height="4"/>
      <rect x="355" y="156" width="170" height="6"/>
      <rect x="355" y="172" width="170" height="8"/>
      <rect x="355" y="188" width="170" height="10"/>
    </g>
    <g opacity="0.92">{hero_fuji}</g>
  </g>
  <g>{"".join(hero_grid)}</g>
  <line x1="10" y1="{horizon_hero}" x2="{W-10}" y2="{horizon_hero}" stroke="#ff2a85" stroke-width="2" stroke-opacity="0.8" filter="url(#glowPink)"/>
  <g shape-rendering="crispEdges">{"".join(skyline)}</g>
  <rect x="57" y="134" width="22" height="38" rx="2" fill="#090a18" stroke="#ff2a85" stroke-width="1"/>
  <path d="{jp_text_path('東京', 61, 138, scale=2, gap=2, vertical=True)}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <rect x="772" y="128" width="22" height="56" rx="2" fill="#090a18" stroke="#00f5d4" stroke-width="1"/>
  <path d="{jp_text_path('ネオン', 776, 132, scale=2, gap=2, vertical=True)}" fill="#ff7eb6" shape-rendering="crispEdges"/>
  <g>{hero_lantern_l}</g>
  <g>{hero_lantern_r}</g>

  <rect x="16" y="16" width="{W-32}" height="30" rx="4" fill="#090a18" fill-opacity="0.86" stroke="#4a1c7a" stroke-width="1.5"/>
  <path d="{pixel_text_path(hud_l, 28, 24, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges"/>
  <path d="{pixel_text_path(hud_r, W - 28 - text_width(hud_r, 2, 1) - 18, 24, 2, 1)}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <rect x="{W-38}" y="25" width="10" height="10" fill="#00f5d4" shape-rendering="crispEdges">
    <animate attributeName="opacity" values="1;0.15;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>

  <path d="{pixel_text_path(title, tx, ty, 5, 1)}" fill="#09071a" stroke="#09071a" stroke-width="5" stroke-linejoin="miter" shape-rendering="crispEdges"/>
  <path d="{pixel_text_path(title, tx+4, ty+4, 5, 1)}" fill="#ff2a85" opacity="0.95" shape-rendering="crispEdges" filter="url(#glowPink)"/>
  <path d="{pixel_text_path(title, tx, ty, 5, 1)}" fill="#00f5d4" shape-rendering="crispEdges" filter="url(#glowCyan)"/>

  <rect x="{sx - 18}" y="{sy - 10}" width="{sw + 36}" height="34" rx="4" fill="#0a0c1d" fill-opacity="0.92" stroke="#ff2a85" stroke-width="2"/>
  <path d="{pixel_text_path(sub, sx, sy, 2, 1)}" fill="#f8f9fa" shape-rendering="crispEdges"/>

  <g filter="url(#glowPink)">{hero_torii}</g>
  <g filter="url(#glowCyan)">{hero_pagoda}</g>
  <path d="{pixel_text_path(press, px, 252, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges">
    <animate attributeName="opacity" values="1;1;0.25;1" dur="1.8s" repeatCount="indefinite"/>
  </path>

  <!-- ==================== DIVIDER 1 ==================== -->
  {divider_bar(326, W)}

  <!-- ==================== SECTION 2: PLAYER CARD ==================== -->
  <rect x="16" y="348" width="{W-32}" height="216" rx="10" fill="#09071a" fill-opacity="0.72" stroke="url(#neonBorder)" stroke-width="2"/>
  <rect x="26" y="358" width="{W-52}" height="32" rx="4" fill="#0d0f22" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
  <path d="{card_header}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <path d="{card_jp}" fill="#ff7eb6" shape-rendering="crispEdges"/>

  <rect x="26" y="398" width="488" height="156" rx="6" fill="#090b1a" fill-opacity="0.84" stroke="#4a1c7a" stroke-width="1.5"/>
  <g shape-rendering="crispEdges">{"".join(card_rows)}</g>
  <rect x="454" y="509" width="48" height="28" rx="3" fill="#170a24" stroke="#ff2a85" stroke-width="1.5"/>
  <path d="{hanko_jp}" fill="#ff2a85" shape-rendering="crispEdges"/>

  <rect x="526" y="398" width="328" height="156" rx="6" fill="url(#dioramaSunset)" stroke="#4a1c7a" stroke-width="1.5"/>
  <g shape-rendering="crispEdges" opacity="0.65">
    <rect x="548" y="422" width="46" height="4" fill="#ff9e6d"/>
    <rect x="556" y="418" width="28" height="4" fill="#ffd166"/>
    <rect x="768" y="426" width="52" height="4" fill="#ff9e6d"/>
    <rect x="776" y="422" width="32" height="4" fill="#ffd166"/>
  </g>
  <circle cx="656" cy="462" r="40" fill="url(#sunGrad)" opacity="0.88"/>
  <g>{scene_fuji}</g>
  <line x1="532" y1="542" x2="848" y2="542" stroke="#ff2a85" stroke-width="2" opacity="0.75"/>
  <g>{scene_torii}</g>
  <g>{scene_lantern_l}</g>
  <g>{scene_lantern_r}</g>

  <!-- ==================== DIVIDER 2 ==================== -->
  {divider_bar(580, W)}

  <!-- ==================== SECTION 3: CONTRIBUTION SNAKE ==================== -->
  <rect x="16" y="602" width="{W-32}" height="258" rx="10" fill="#09071a" fill-opacity="0.74" stroke="url(#neonBorder)" stroke-width="2"/>
  <rect x="26" y="612" width="{W-52}" height="34" rx="4" fill="#0d0f22" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
  {mini_snake}
  <path d="{snake_title}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <g shape-rendering="crispEdges">{"".join(legend_elems)}</g>

  <rect x="26" y="652" width="{W-52}" height="172" rx="6" fill="url(#screenSunset)" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
  <g shape-rendering="crispEdges" opacity="0.55">
    <rect x="76" y="674" width="84" height="6" fill="#ff9e6d"/>
    <rect x="92" y="668" width="48" height="6" fill="#ffd166"/>
    <rect x="690" y="678" width="90" height="6" fill="#ff9e6d"/>
    <rect x="706" y="672" width="54" height="6" fill="#ffd166"/>
  </g>
  <circle cx="440" cy="728" r="54" fill="url(#sunGrad)" opacity="0.55"/>
  <g opacity="0.65">{snake_fuji}</g>
  <rect x="41" y="809" width="798" height="15" rx="2" fill="#0d1024" fill-opacity="0.88" stroke="#4a1c7a" stroke-width="1"/>

  <svg x="28" y="646" width="824" height="180" viewBox="{view_box}">
    {snake_inner}
  </svg>

  <rect x="26" y="828" width="{W-52}" height="24" rx="4" fill="#0d0f22" fill-opacity="0.92" stroke="#4a1c7a" stroke-width="1.5"/>
  <g shape-rendering="crispEdges">
    <path d="{foot_l}" fill="#ff7eb6"/>
    <path d="{foot_c}" fill="#ffd166"/>
    <path d="{foot_r}" fill="#00f5d4"/>
    <rect x="{W - 38}" y="835" width="10" height="10" fill="#ff2a85">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- ==================== DIVIDER 3 ==================== -->
  {divider_bar(874, W)}

  <!-- ==================== SECTION 4: SUNSET LAKE ENDING ==================== -->
  <g clip-path="url(#endSkyClip)">
    <circle cx="440" cy="968" r="44" fill="url(#sunGrad)" opacity="0.92"/>
    <g fill="#731659" opacity="0.6">
      <rect x="388" y="944" width="104" height="3"/>
      <rect x="388" y="953" width="104" height="4"/>
      <rect x="388" y="963" width="104" height="5"/>
    </g>
    <g shape-rendering="crispEdges">
      <rect x="130" y="936" width="64" height="5" fill="#ff8e72" opacity="0.72"/>
      <rect x="142" y="931" width="38" height="5" fill="#ffd166" opacity="0.65"/>
      <rect x="680" y="934" width="72" height="5" fill="#ff8e72" opacity="0.72"/>
      <rect x="694" y="929" width="42" height="5" fill="#ffd166" opacity="0.65"/>
    </g>
  </g>
  <line x1="10" y1="{horizon_end}" x2="{W-10}" y2="{horizon_end}" stroke="#ff9e44" stroke-width="2" opacity="0.88"/>
  <g>{"".join(end_ripples)}</g>
  <g>{end_torii}</g>
  <g>{end_pagoda}</g>
  <g>{end_lantern_l}</g>
  <g>{end_lantern_r}</g>

  <rect x="{(W - etotal - 44)//2}" y="894" width="{etotal + 44}" height="32" rx="4" fill="#09071a" fill-opacity="0.86" stroke="#ff2a85" stroke-width="1.5"/>
  <path d="{pixel_text_path(end_txt, etx, 903, 2, 1)}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <path d="{jp_text_path(arigatou, eax, 903, scale=2, gap=2)}" fill="#ff7eb6" shape-rendering="crispEdges"/>

  <rect x="{esx - 18}" y="998" width="{esw + 36}" height="24" rx="4" fill="#070614" fill-opacity="0.85" stroke="#4a1c7a" stroke-width="1"/>
  <path d="{pixel_text_path(sub_end, esx, 1003, 2, 1)}" fill="#ffd166" shape-rendering="crispEdges">
    <animate attributeName="opacity" values="1;1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
  </path>

  <!-- ==================== GLOBAL PETALS, SCANLINES & BORDER ==================== -->
  {all_petals}
  <rect x="4" y="4" width="{W-8}" height="{H-8}" rx="12" fill="url(#scanlines)" pointer-events="none"/>
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
    print(f"Unified Japanese Sunset Profile SVG written to {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
