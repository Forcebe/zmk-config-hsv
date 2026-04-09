# Forcebe's Hillside View Config

ZMK firmware configuration for the [Hillside View](https://github.com/wannabecoffeenerd/HillSideView/) split keyboard (3x6 layout), running on nice!nano v2 with nice!view displays.

Keymap is based on [Miryoku](https://github.com/manna-harbour/miryoku) with home row mods and chords.

## Keymap

![Keymap](keymap-drawer/hillside_view.svg)

## Layers

| Layer | Description |
|-------|-------------|
| Default | QWERTY with home row mods and combos |
| Symbol | Symbols and brackets |
| Number | Numpad and arithmetic |
| Navigation | Arrow keys, Home/End, Page Up/Down |
| Function | Function keys, Bluetooth controls |

## Home row mods

Modifiers are available on the home row as hold-tap keys using a balanced flavor:

| Key | Left hand | Right hand |
|-----|-----------|------------|
| Ctrl | A | ; |
| Opt | S | L |
| Cmd | D | K |
| Shift | F | J |

`hold-trigger-key-positions` triggers the hold on cross-hand keypresses, while `hold-trigger-on-release` allows stacking modifiers on the same hand (e.g. Ctrl+Shift). Misfires are reduced with `require-prior-idle-ms` (150ms) and `quick-tap-ms` (175ms) for fast repeated taps.

## Combos

Combos are active on all layers.

| Keys | Action | Description |
|------|--------|-------------|
| F + J | Caps Word | Capitalizes the next word then deactivates |
| A + ; | ⌃B | Tmux leader key |

Combo trigger keys are color-coded in the keymap diagram above with a legend beneath the Default layer.

## Building

Firmware is built automatically via GitHub Actions on push. Download the artifacts from the [Actions tab](../../actions).

The keymap visualization is also auto-generated — including combo highlighting and legend — when the keymap changes.
