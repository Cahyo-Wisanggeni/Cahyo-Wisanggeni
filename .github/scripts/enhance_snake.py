"""Post-process Platane/snk SVG into a Neon Pixel Arcade Cabinet."""

import re
import sys
from pathlib import Path

FONT_5X7 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
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
    return len(text) * 5 * scale + max(0, len(text) - 1) * gap * scale


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


def render_mini_snake(x: int, y: int, px: int = 3) -> str:
    palette = {
        "C": "#00f5d4",
        "W": "#ffffff",
        "P": "#ff2a85",
        "V": "#9d4edd",
        "G": "#ffd166",
    }
    by_col: dict[str, list[str]] = {}
    for r, row in enumerate(MINI_SNAKE_ICON):
        for c, ch in enumerate(row):
            if ch in palette:
                by_col.setdefault(palette[ch], []).append(f"M{x + c * px},{y + r * px}h{px}v{px}h-{px}z")
    return "".join(
        f'<path d="{"".join(cmds)}" fill="{col}" shape-rendering="crispEdges"/>'
        for col, cmds in by_col.items()
    )


def enhance_snake_svg(raw_svg: str) -> str:
    # Extract viewBox and inner body from Platane/snk output
    vb_match = re.search(r'viewBox="([^"]+)"', raw_svg)
    view_box = vb_match.group(1) if vb_match else "-16 -32 880 192"

    inner_match = re.search(r"<svg[^>]*>(.*)</svg>", raw_svg, flags=re.DOTALL)
    if not inner_match:
        raise ValueError("Invalid SVG input: missing <svg> wrapper")
    inner = inner_match.group(1)

    # Remove <desc> and crisp up rounded corners on rects
    inner = re.sub(r"<desc>.*?</desc>", "", inner, flags=re.DOTALL)
    inner = re.sub(r'\s+r[xy]="[0-9.]+"', "", inner)

    # Inject crisp pixel & multi-color neon snake overrides right after </style>
    override_css = (
        "<style>"
        ":root{--ce:#101326;--cb:#251d47;--c0:#101326;--c1:#3b0764;--c2:#7e22ce;--c3:#00f5d4;--c4:#ffd166}"
        ".c{shape-rendering:crispEdges !important;stroke-width:1px;stroke:var(--cb)}"
        ".c.c1,.c.c2,.c.c3,.c.c4{stroke:#ffffff22}"
        ".u{shape-rendering:crispEdges !important}"
        ".s{shape-rendering:crispEdges !important}"
        ".s.s0{fill:#00f5d4 !important;filter:url(#snakeGlow)}"
        ".s.s1{fill:#ff2a85 !important;filter:url(#snakeGlow)}"
        ".s.s2{fill:#9d4edd !important}"
        ".s.s3{fill:#ffd166 !important}"
        "</style>"
    )
    inner = inner.replace("</style>", "</style>" + override_css, 1)

    W, H = 880, 272
    title_path = pixel_text_path("SNAKE.EXE // CONTRIBUTION ARCADE", 54, 21, scale=2, gap=1)
    mini_snake = render_mini_snake(20, 16, px=3)

    # Top-right legend + blinking 1UP
    legend_colors = ["#101326", "#3b0764", "#7e22ce", "#00f5d4", "#ffd166"]
    legend_elems = [f'<path d="{pixel_text_path("LESS", 590, 21, 2, 1)}" fill="#94a3b8"/>']
    lx = 644
    for col in legend_colors:
        legend_elems.append(f'<rect x="{lx}" y="22" width="12" height="12" fill="{col}" stroke="#2d2057" stroke-width="1"/>')
        lx += 16
    legend_elems.append(f'<path d="{pixel_text_path("MORE", lx + 4, 21, 2, 1)}" fill="#94a3b8"/>')
    one_up_x = lx + 4 + text_width("MORE", 2, 1) + 18
    legend_elems.append(
        f'<rect x="{one_up_x}" y="17" width="48" height="22" rx="3" fill="#170f2e" stroke="#ff2a85" stroke-width="1.5"/>'
        f'<path d="{pixel_text_path("1UP", one_up_x + 7, 21, 2, 1)}" fill="#ffd166">'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/>'
        f"</path>"
    )

    # Bottom status bar text
    foot_l = pixel_text_path("GRID: 52W X 7D", 22, 244, scale=2, gap=1)
    foot_c = pixel_text_path("CYBER-SERPENT MK.II", 336, 244, scale=2, gap=1)
    foot_r_txt = "STATUS: HUNTING COMMITS"
    foot_r_x = W - 38 - text_width(foot_r_txt, 2, 1)
    foot_r = pixel_text_path(foot_r_txt, foot_r_x, 244, scale=2, gap=1)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Neon Pixel Contribution Snake Arcade">
  <defs>
    <linearGradient id="cabBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070812"/>
      <stop offset="100%" stop-color="#110b24"/>
    </linearGradient>
    <linearGradient id="cabBorder" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f5d4"/>
      <stop offset="50%" stop-color="#9d4edd"/>
      <stop offset="100%" stop-color="#ff2a85"/>
    </linearGradient>
    <filter id="snakeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="crtLines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="2" fill="#000000" opacity="0.14"/>
    </pattern>
  </defs>

  <!-- Outer Cabinet -->
  <rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="10" fill="url(#cabBg)" stroke="url(#cabBorder)" stroke-width="2.5"/>

  <!-- Top Arcade Header -->
  <rect x="12" y="12" width="{W - 24}" height="34" rx="4" fill="#0d0f22" stroke="#2d2057" stroke-width="1.5"/>
  {mini_snake}
  <path d="{title_path}" fill="#00f5d4" shape-rendering="crispEdges"/>
  <g shape-rendering="crispEdges">{"".join(legend_elems)}</g>

  <!-- Inner Arcade Screen Frame -->
  <rect x="12" y="52" width="{W - 24}" height="182" rx="6" fill="#080a16" stroke="#251d47" stroke-width="1.5"/>

  <!-- Progress / Combo Meter Track aligned to Platane/snk .u bar (y=144 in nested viewBox) -->
  <rect x="29" y="213" width="822" height="16" rx="2" fill="#0d1024" stroke="#2d2057" stroke-width="1"/>

  <!-- Nested Live Contribution Snake -->
  <svg x="16" y="46" width="848" height="185" viewBox="{view_box}">
    {inner}
  </svg>

  <!-- Bottom Arcade Status Bar -->
  <rect x="12" y="238" width="{W - 24}" height="24" rx="4" fill="#0d0f22" stroke="#2d2057" stroke-width="1.5"/>
  <g shape-rendering="crispEdges">
    <path d="{foot_l}" fill="#9d4edd"/>
    <path d="{foot_c}" fill="#ffd166"/>
    <path d="{foot_r}" fill="#00f5d4"/>
    <rect x="{W - 30}" y="245" width="10" height="10" fill="#ff2a85">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- Subtle CRT Scanlines & Corner Rivets -->
  <rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="8" fill="url(#crtLines)" pointer-events="none"/>
  <g shape-rendering="crispEdges">
    <rect x="8" y="8" width="4" height="4" fill="#00f5d4"/>
    <rect x="{W - 12}" y="8" width="4" height="4" fill="#ff2a85"/>
    <rect x="8" y="{H - 12}" width="4" height="4" fill="#ff2a85"/>
    <rect x="{W - 12}" y="{H - 12}" width="4" height="4" fill="#00f5d4"/>
  </g>
</svg>'''


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: enhance_snake.py <input.svg> <output.svg>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.write_text(enhance_snake_svg(src.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Enhanced snake SVG written to {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
