#!/usr/bin/env python3
"""Post-process a keymap-drawer SVG to add color-coded combo key highlighting and a legend.

Reads combo definitions from the parsed YAML, auto-assigns colors from a palette,
injects CSS to highlight trigger keys on the Default layer, and adds an inline legend
between the Default and Symbol layers.

Usage: python3 scripts/add-combo-legend.py <parsed.yaml> <input.svg> [output.svg]
  If output is omitted, the input SVG is modified in place.
"""

import re
import sys
from pathlib import Path

import yaml

# Color palette for combos (dark-theme friendly): (key_fill, stroke/accent, text_fill)
PALETTE = [
    ("#4a3a1a", "#c89b40", "#e8c860"),  # amber
    ("#1a3a3a", "#40a0a0", "#60d0c8"),  # teal
    ("#3a1a3a", "#a040a0", "#d060d0"),  # magenta
    ("#1a2a3a", "#4080c0", "#60b0e8"),  # blue
    ("#3a2a1a", "#c07040", "#e09060"),  # orange
    ("#1a3a2a", "#40a060", "#60d080"),  # green
]

LEGEND_Y = 370
LEGEND_HEIGHT = 70
LEGEND_ITEM_W = 200
LEGEND_ITEM_H = 26
LEGEND_ITEM_GAP = 20
LEGEND_X_START = 0
FONT = "SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace"


def load_combos(yaml_path: str) -> list[dict]:
    """Load combo definitions from parsed keymap YAML."""
    data = yaml.safe_load(Path(yaml_path).read_text())
    return data.get("combos", [])


def key_name_for_position(yaml_path: str, pos: int) -> str:
    """Look up the key name at a position on the Default layer."""
    data = yaml.safe_load(Path(yaml_path).read_text())
    default_keys = data.get("layers", {}).get("Default", [])
    if pos >= len(default_keys):
        return str(pos)
    key = default_keys[pos]
    if isinstance(key, dict):
        return key.get("t", str(pos))
    return str(key)


def generate_css(combos: list[dict], yaml_path: str) -> str:
    """Generate CSS for color-coded combo trigger keys on the Default layer."""
    lines = ["/* auto-generated combo key highlighting */"]
    for i, combo in enumerate(combos):
        fill, stroke, _ = PALETTE[i % len(PALETTE)]
        positions = combo["p"]
        key_names = [key_name_for_position(yaml_path, p) for p in positions]
        label = combo.get("k", " + ".join(key_names))
        selectors = ",\n    ".join(
            f".layer-Default .keypos-{p} rect.key" for p in positions
        )
        lines.append(f"    /* {label} ({' + '.join(key_names)}) */")
        lines.append(f"    {selectors} {{ fill: {fill}; stroke: {stroke}; }}")
    return "\n".join(lines)


def generate_legend_svg(combos: list[dict], yaml_path: str) -> str:
    """Generate SVG legend group for all combos."""
    items = []
    x = LEGEND_X_START
    for i, combo in enumerate(combos):
        fill, stroke, text_fill = PALETTE[i % len(PALETTE)]
        positions = combo["p"]
        key_names = [key_name_for_position(yaml_path, p) for p in positions]
        label = combo.get("k", " + ".join(key_names))
        trigger = " + ".join(key_names)
        text = f"{trigger} \u2192 {label}"

        # Size the box to fit the text (approximate: 7.5px per char at 12px font)
        text_w = len(text) * 7.5 + 20
        item_w = max(LEGEND_ITEM_W, text_w)

        items.append(
            f'  <rect rx="4" ry="4" x="{x}" y="8" width="{item_w:.0f}" height="{LEGEND_ITEM_H}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>\n'
            f'  <text x="{x + item_w / 2:.0f}" y="21" text-anchor="middle" '
            f'dominant-baseline="middle" fill="{text_fill}" font-size="12px" '
            f'font-family="{FONT}">{text}</text>'
        )
        x += item_w + LEGEND_ITEM_GAP

    inner = "\n".join(items)
    return f'<g class="combo-legend" transform="translate(30, {LEGEND_Y})">\n{inner}\n</g>'


def process_svg(svg: str, css: str, legend_svg: str) -> str:
    """Inject combo CSS and legend into the SVG, shifting non-Default layers down."""
    # Update height and viewBox
    height_match = re.search(r'height="(\d+)"', svg)
    old_height = int(height_match.group(1))
    new_height = old_height + LEGEND_HEIGHT
    svg = svg.replace(f'height="{old_height}"', f'height="{new_height}"', 1)
    svg = re.sub(
        r'viewBox="0 0 (\d+) ' + str(old_height) + '"',
        lambda m: f'viewBox="0 0 {m.group(1)} {new_height}"',
        svg,
        count=1,
    )

    # Inject CSS before closing </style>
    svg = svg.replace("</style>", f"\n{css}\n</style>", 1)

    # Shift non-Default layers down and inject legend before Symbol
    def shift_layer(match: re.Match) -> str:
        full = match.group(0)
        y = int(match.group(1))
        new_y = y + LEGEND_HEIGHT
        return full.replace(f"translate(30, {y})", f"translate(30, {new_y})")

    svg = re.sub(
        r'<g transform="translate\(30, (\d+)\)" class="layer-(?!Default)(\w+)"',
        shift_layer,
        svg,
    )

    # Inject legend before Symbol layer
    svg = re.sub(
        r'(<g transform="translate\(30, \d+\)" class="layer-Symbol")',
        legend_svg + "\n" + r"\1",
        svg,
        count=1,
    )

    return svg


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <parsed.yaml> <input.svg> [output.svg]")
        sys.exit(1)

    yaml_path = sys.argv[1]
    svg_path = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else svg_path

    combos = load_combos(yaml_path)
    if not combos:
        print("No combos found, skipping legend injection.")
        return

    css = generate_css(combos, yaml_path)
    legend_svg = generate_legend_svg(combos, yaml_path)
    svg = Path(svg_path).read_text()
    result = process_svg(svg, css, legend_svg)
    Path(out_path).write_text(result)

    print(f"Injected {len(combos)} combo(s) into {out_path}")


if __name__ == "__main__":
    main()
