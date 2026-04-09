#!/usr/bin/env bash
# Injects a combo legend between the Default and Symbol layers in the keymap SVG.
# Usage: ./scripts/add-combo-legend.sh <input.svg> [output.svg]
#   If output is omitted, the input file is modified in place.

set -euo pipefail

INPUT="$1"
OUTPUT="${2:-$1}"

LEGEND_HEIGHT=70

# Read current SVG height from the first line
HEIGHT=$(sed -n '1s/.*height="\([0-9]*\)".*/\1/p' "$INPUT")
NEW_HEIGHT=$((HEIGHT + LEGEND_HEIGHT))

# Write legend SVG fragment to temp file
LEGEND_FILE=$(mktemp)
cat > "$LEGEND_FILE" <<'EOF'
<g class="combo-legend" transform="translate(30, 370)">
  <rect rx="4" ry="4" x="0" y="8" width="180" height="26" fill="#4a3a1a" stroke="#c89b40" stroke-width="1"/>
  <text x="90" y="21" text-anchor="middle" dominant-baseline="middle" fill="#e8c860" font-size="12px" font-family="SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace">F + J → Caps Word</text>
  <rect rx="4" ry="4" x="200" y="8" width="200" height="26" fill="#1a3a3a" stroke="#40a0a0" stroke-width="1"/>
  <text x="300" y="21" text-anchor="middle" dominant-baseline="middle" fill="#60d0c8" font-size="12px" font-family="SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace">A + ; → ⌃B Tmux Leader</text>
</g>
EOF

# Step 1: Update SVG height and viewBox
sed \
  -e "s/height=\"${HEIGHT}\"/height=\"${NEW_HEIGHT}\"/" \
  -e "s/viewBox=\"0 0 1018 ${HEIGHT}\"/viewBox=\"0 0 1018 ${NEW_HEIGHT}\"/" \
  "$INPUT" > "${OUTPUT}.tmp"

# Step 2: Shift non-Default layers down and inject legend before Symbol layer
while IFS= read -r line; do
  # Inject legend before the Symbol layer
  case "$line" in
    *'class="layer-Symbol"'*)
      cat "$LEGEND_FILE"
      ;;
  esac
  # Shift non-Default layers down by LEGEND_HEIGHT
  case "$line" in
    *'class="layer-'*)
      case "$line" in
        *'layer-Default'*) ;;
        *)
          old_y=$(echo "$line" | sed 's/.*translate(30, \([0-9]*\)).*/\1/')
          new_y=$((old_y + LEGEND_HEIGHT))
          line=$(echo "$line" | sed "s/translate(30, ${old_y})/translate(30, ${new_y})/")
          ;;
      esac
      ;;
  esac
  printf '%s\n' "$line"
done < "${OUTPUT}.tmp" > "${OUTPUT}.tmp2"

mv "${OUTPUT}.tmp2" "$OUTPUT"
rm -f "${OUTPUT}.tmp" "$LEGEND_FILE"
