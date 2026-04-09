# ZMK Config - Hillside View

## Project structure

- `config/hillside_view.keymap` - ZMK keymap source (layers, combos, behaviors)
- `config/hsv_layout.json` - physical key layout for keymap-drawer
- `keymap_drawer.config.yaml` - keymap-drawer config (key name mappings, draw styling, CSS)
- `keymap-drawer/hillside_view.yaml` - parsed keymap YAML (auto-generated)
- `keymap-drawer/hillside_view.svg` - rendered SVG (auto-generated)
- `scripts/add-combo-legend.py` - post-processes SVG to inject combo key highlighting and legend
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

python3 scripts/add-combo-legend.py keymap-drawer/hillside_view.yaml keymap-drawer/hillside_view.svg
```

## Combo display pipeline

Combos are displayed as color-coded trigger keys on the Default layer with an inline legend between the Default and Symbol layers. This is fully automatic — no manual CSS or legend updates needed when combos change.

`scripts/add-combo-legend.py` reads the parsed YAML, discovers all combos, auto-assigns colors from a palette, and injects:
- CSS to highlight trigger keys on the Default layer
- An SVG legend showing key names and combo actions

### When changing combos

Only `config/hillside_view.keymap` needs editing. The drawing pipeline handles everything else:
- Add display names for new bindings via `raw_binding_map` in `keymap_drawer.config.yaml` (otherwise the raw ZMK binding name is shown)
- Combos are active on all layers in firmware; the diagram shows them on the Default layer only via `--keys-only` draw + the legend script

## Conventions

- Layers ordered: Default, Symbol, Number, Navigation, Function
- Layer buttons on Default are color-coded: blue=Nav, purple=Sym, amber=Num, green=Func
- Combos are active on all layers; displayed on Default layer only in the diagram
- macOS modifier names: Cmd, Opt, Ctrl, Shift
- Draw uses `--keys-only` flag; combo visualization is handled by `add-combo-legend.py`
