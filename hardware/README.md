# Hardware

License: see [LICENSE.md](../LICENSE.md). Commercial use: see [COMMERCIAL.md](../COMMERCIAL.md).

How to build it: see the [build guide](../docs/BUILD_GUIDE.md).

## Contents

- [Parts list](PARTS_LIST.md), with approximate 2026 prices. [DRAFT]
- `schematics/` — the interface board design as a [Fritzing](https://fritzing.org)
  project (`.fzz`, made with Fritzing 0.9.10). Open it in Fritzing to see the
  breadboard, schematic and PCB views, or to change the design.
  `PoolWind_interface_board_bb.png` and `PoolWind_interface_board_pcb.png` are
  pictures of the wiring (breadboard view) and the board layout (PCB view).
- `gerbers/` — the interface board's manufacturing files.
  **`PoolWind_PCB_gerbers.zip`** is ready to upload to any PCB maker:
  two-layer board, 117 × 88 mm (4.59 × 3.46 in). The same files are also
  there unzipped, with a pick-and-place list (`_pnp.txt`).
- `PoolWind_PCB_preview.png` — a picture of the board drawn from the Gerber
  files (top copper yellow, bottom copper orange, silkscreen white). Checked
  2026-10-10: the Gerber files' copper connections match the Fritzing design
  exactly.

## Connections used by the software

| Function | Connection |
|---|---|
| Jet speed Up (remote button) | Relay on GPIO 17 (active low) |
| Jet speed Down (remote button) | Relay on GPIO 18 (active low) |
| Pump On/Off (remote button) | Relay on GPIO 27 (active low, 2-second pulse) |
| Jet speed feedback | INA260 sensor on I2C at address 0x40, reading the Pace Display port voltage on its VBUS pin (its V+ to VBUS jumper cut) |
| Camera | Spedal 920 Pro Conference Camera (120°, USB) above the swim area, opened as video device 0 |

The program never energizes Up and Down at the same time. Before pressing
On/Off, it releases Up and Down.

The Raspberry Pi pin numbers and the RJ45 jack pins are in the build guide,
section 3. I2C must be turned on (the install script does this; see the
setup guide).
