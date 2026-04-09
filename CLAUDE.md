# ZMK Config - Hillside View

## Project structure

- `config/hillside_view.keymap` - ZMK keymap source (layers, combos, behaviors)
- `config/hsv_layout.json` - physical key layout for keymap-drawer
- `keymap_drawer.config.yaml` - keymap-drawer config (key name mappings, draw styling, CSS)
- `keymap-drawer/hillside_view.yaml` - parsed keymap YAML (auto-generated)
- `keymap-drawer/hillside_view.svg` - rendered SVG (auto-generated)
- `scripts/add-combo-legend.sh` - post-processes SVG to inject combo legend
- `.github/workflows/draw-keymaps.yml` - renders keymap diagram (runs after firmware build)

## Rendering the keymap locally

```bash
pip install keymap-drawer  # or use a venv

keymap -c keymap_drawer.config.yaml parse \
  -z config/hillside_view.keymap \
  -l Default Symbol Number Navigation Function \
  > keymap-drawer/hillside_view.yaml

keymap -c keymap_drawer.config.yaml draw \
  --keys-only \
  keymap-drawer/hillside_view.yaml \
  -j config/hsv_layout.json \
  > keymap-drawer/hillside_view.svg

./scripts/add-combo-legend.sh keymap-drawer/hillside_view.svg
```

## What requires manual updates when changing combos

The combo display uses color-coded keys and an inline legend instead of keymap-drawer's default combo boxes. This means three files must be kept in sync manually whenever combos change:

| File | What to update |
|---|---|
| `config/hillside_view.keymap` | Combo `key-positions`, `bindings`, `layers` |
| `keymap_drawer.config.yaml` | CSS selectors under `svg_extra_style` targeting `.layer-Default .keypos-N rect.key` with the correct key position numbers and colors |
| `scripts/add-combo-legend.sh` | Legend text (e.g. "A + ; → ⌃B Tmux Leader"), rect fill/stroke colors, and text fill colors to match the CSS |

If you only change the keymap without updating the other two, the key highlighting and legend will be stale or wrong.

### Current combos

| Combo | Keys | Positions | Color |
|---|---|---|---|
| Caps Word | F + J | 16, 19 | Amber (`#4a3a1a` fill, `#c89b40` stroke) |
| Tmux Leader (⌃B) | A + ; | 13, 22 | Teal (`#1a3a3a` fill, `#40a0a0` stroke) |

### What does NOT need manual updates

- Adding/removing/reordering keys within layers - the parse + draw pipeline handles this automatically
- Layer styling (held keys, layer button colors) - driven by CSS classes that keymap-drawer assigns automatically
- Key name display (e.g. `LGUI` → `Cmd`) - controlled by `zmk_keycode_map` and `raw_binding_map` in the config

## Conventions

- Layers ordered: Default, Symbol, Number, Navigation, Function
- Layer buttons on Default are color-coded: blue=Nav, purple=Sym, amber=Num, green=Func
- Combos always use `layers = <0>;` to restrict to Default layer only
- macOS modifier names: Cmd, Opt, Ctrl, Shift
- Draw uses `--keys-only` flag; combo visualization is handled entirely by CSS + legend script
