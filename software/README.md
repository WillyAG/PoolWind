# Software

License: see [LICENSE.md](../LICENSE.md).

Required Notice: Copyright (c) William A. Gorlitz. U.S. Copyright Registration TXu 2-304-621.

## Files

| File | Purpose |
|---|---|
| `poolwind.py` | The program, with the calibration built in (menu **Calibrate pool...**, or `python3 poolwind.py --calibrate`) |
| `poolwind_defaults.txt` | The swimmer settings for anyone without a USB stick |
| `poolwind_calibration.txt` | Your pool's calibration: the Master Pace table (the zones; its first and last rows are the jet's limits), swim area, swim length, swim zone width. **The one here is the author's pool**: the calibration's scan fits it to yours (setup guide, section 5) |
| `toggle_monitor.sh` | The Monitor Toggle: turns the pool monitor between portrait and landscape (setup guide, section 9) |
| `WHATS_NEW.txt` | What's new in this version; the install script shows it after an update (setup guide, section 10) |

The settings files must sit next to the program and start with its name.
Each swimmer's own settings go on their USB stick, in
`poolwind_ind_defaults.txt`, and their own Pace table in
`poolwind_ind_calibration.txt`.

## Installing and setting up

Follow the [setup and calibration guide](../docs/SETUP_GUIDE.md). The install
script, [`install.sh`](../install.sh), sets up everything on a fresh
Raspberry Pi OS and copies these files to a `PoolWind` folder in your home
folder. The guide then covers fitting PoolWind to your pool (swim area,
the calibration, the jet's limits) and explains every setting.

## Tested platform

- Raspberry Pi 5, Raspberry Pi OS based on Debian 13 (trixie), Python 3.13
- OpenCV 4.13, NumPy 2.2, SciPy 1.17, matplotlib 3.10, PySide6 6.8,
  Adafruit INA260 1.3 (with Blinka `board`), lgpio

## Where your swims are saved

Swim logs (CSV) and training video are saved on the swimmer's USB stick if
one is in (plugged in before or while PoolWind runs), or otherwise in a `CSV Vault` folder
next to the program.
