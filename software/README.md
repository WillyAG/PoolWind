# Software

License: see [LICENSE.md](../LICENSE.md).

Required Notice: Copyright (c) William A. Gorlitz. U.S. Copyright Registration TXu 2-304-621.

## Files

| File | Purpose |
|---|---|
| `poolwind.py` | The program |
| `poolwind_defaults.txt` | The swimmer settings for anyone without a USB stick |
| `poolwind_calibration.txt` | Your pool's calibration: pace table, safety limits, swim area, pool length, center lane. **The one here is the author's pool, as an example** (setup guide, section 5) |
| `toggle_monitor.sh` | The Monitor Toggle: turns the pool monitor between portrait and landscape (setup guide, section 9) |

The settings files must sit next to the program and start with its name.
Each swimmer's own settings go on their USB stick, in
`poolwind_ind_defaults.txt`.

## Installing and setting up

Follow the [setup and calibration guide](../docs/SETUP_GUIDE.md). The install
script, [`install.sh`](../install.sh), sets up everything on a fresh
Raspberry Pi OS and copies these files to a `PoolWind` folder in your home
folder. The guide then covers fitting PoolWind to your pool (swim area,
pace table, safety limits) and explains every setting.

## Tested platform

- Raspberry Pi 5, Raspberry Pi OS based on Debian 13 (trixie), Python 3.13
- OpenCV 4.13, NumPy 2.2, SciPy 1.17, matplotlib 3.10, PyQt5,
  Adafruit INA260 1.3 (with Blinka `board`), lgpio

## Where your swims are saved

Swim logs (CSV) and training video are saved on the swimmer's USB stick if
one is inserted when PoolWind starts, or otherwise in a `CSV Vault` folder
next to the program.
