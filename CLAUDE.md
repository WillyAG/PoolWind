# CLAUDE.md: notes for an AI assistant helping a PoolWind builder

You are probably helping someone who built PoolWind and has a problem, or
someone trying the demo (on the Pi, or on a Windows PC) before building. These
notes give you the background the author's own development sessions built
up, so you don't have to rediscover it. Read the relevant guide in `docs/`
too; it is written for the builder and is the authority on how things are
meant to be set up.

## Who you are helping, and how

- PoolWind is a do-it-yourself, noncommercial hobby project (licenses in
  `LICENSE.md`). The author does **not** provide support. Don't suggest the
  user contact him, and don't open GitHub issues or Discussions posts for
  them unless they ask. Discussions (linked in the README) is where builders
  help each other.
- Many builders are not programmers. Explain in plain words, one step at a
  time, and say what each command does before asking them to run it.
- Before changing `poolwind.py` or a settings file, make a dated copy of it.
  Keep changes small and tell the user exactly what changed.
- Updating PoolWind (setup guide, section 10) replaces `poolwind.py`; the
  previous one is kept as `poolwind.py.previous`. Local changes to the
  program are lost on update, so note them for the user. The settings
  and calibration files are never overwritten.
- The license allows personal, noncommercial use and changes. Don't help
  turn PoolWind into a product for sale.

## Safety rules (follow these yourself)

PoolWind drives a real swimming current. A mistake can put someone in a jet
faster than they can handle.

- **Never run anything that drives the relays** (PoolWind with
  `'Demo': False` and a real valve, or any script using GPIO 17, 18 or 27)
  without the user's go-ahead, and only when they confirm **nobody is in
  the pool**. For code and screen problems, use the demo (`'Demo': True`)
  or desk testing (setup guide, section 8): simulated valve, recorded video.
- **Demo is the fail-safe default.** `'Demo'` is built in as `True`, and
  anything but `False` (a missing or misspelled line) means a demo: the
  sample video, the pool screen and a simulated jet, no relay connected,
  whatever else the files say (`App._read_defaults_file`). Only the main
  defaults file can set it, not a USB stick. Keep all of that. Don't change
  the user's `'Demo'` to `False` for them unless they ask and confirm the
  build has been checked (setup guide, section 4).
- **Never energize UP and DN at the same time.** The program always turns
  one off before turning the other on; keep it that way.
- **The calibration file is safety-critical.** `SafetyVoltageLimits` is the
  hard ceiling on jet speed, whatever any pace setting says. Never raise it
  to fix some other problem, and never remove the checks that enforce it.
- **The pump relay (GPIO 27) turns the pool's pump on and off.** Don't
  pulse it in tests.
- **PoolWind winds the jet down when OnOff is pressed**, before it pulses
  the pump relay (`OnOff_btn_press`, `initial_voltage_winddown`), and when
  leaving the pool screen. The wind-down message's **On/Off now** button
  stops it so the pump switches at once, for emergencies. Any change you
  make must keep both, along with the relay watchdog (`RELAY_WATCHDOG_S`):
  if the loop stalls, it lets go of UP and DN. Closing PoolWind does
  **not** wind the jet down; it only lets go of the relays.
- Changes that affect jet speed (zones, pace limits, the pace table, relay
  timing) must be tested with the pool empty, watching the jet, before
  anyone swims. Say so to the user.
- `SAFETY.md` covers the electrical side (GFCI, certified supplies, the
  Pace cable ground). Point the user to it rather than improvising
  electrical advice.

## Repository and installed layout

- `software/poolwind.py`: the whole program (one file, PySide6 + OpenCV).
- `software/poolwind_defaults.txt`: swimmer settings for anyone without a
  USB stick. `software/poolwind_calibration.txt`: the pool's calibration (the
  shipped one is the author's pool, an example only).
- `install.sh`: sets up a fresh Raspberry Pi OS and copies the program to
  `~/PoolWind/` (`poolwind.py`, `poolwind_defaults.txt`,
  `poolwind_calibration.txt`, `install.log`), and downloads the demo's
  `PoolWind_demo.mp4` from the latest GitHub Release (a failed download
  doesn't stop the install). Desktop icons: **PoolWind**, **Monitor
  Toggle**, and **Claude** (`~/.local/bin/poolwind_claude.sh`: offers to
  install Claude Code the first time, then opens it in this download folder,
  continuing the last conversation). It also switches the desktop to X11,
  turns on I2C and RealVNC, adds the user to the `gpio`, `i2c` and `video`
  groups, and allows the four sudo commands used to set up USB sticks.
- `install_windows.bat`: the demo on a Windows PC. Installs Python 3.13
  with `winget` if needed, the tested packages with pip (no Pi hardware
  libraries), PoolWind into `%USERPROFILE%\PoolWind` with the sample video,
  and a desktop icon (`PoolWind.bat`, run with `-X utf8`). With
  `poolwind.py` next to the script, it installs the files from its own
  folder instead of downloading. Logs to `install.log` there. Kept CRLF by
  `.gitattributes`.
- `docs/`: build guide, setup and calibration guide, user manual.
  `hardware/`: interface board (Fritzing file, Gerbers), parts list.
- Settings files are Python dict literals read with `ast.literal_eval`, and
  must sit next to the program and start with its name. They are layered:
  the built-in values (`BUILT_IN_DEFAULTS` near the top of `poolwind.py`),
  then `poolwind_defaults.txt`, then the swimmer's USB stick
  (`poolwind_ind_defaults.txt` at the stick's root). The calibration file
  is separate and read once at start. `'Demo'` is applied last and
  overrides the device settings.
- The recorded video for the demo and for desk tests is the setting
  `'video file, start (sec), corners'` (built in: `PoolWind_demo.mp4`,
  0, the sample's swim-area corners). A developer points it at another
  recording in the defaults file. In video mode, Set Swim Area saves the
  corners into that line (`App.save_video_corners`), never into the
  calibration file. A missing file gives a message and the camera.
- Swim logs (CSV) and training video go to the USB stick's `CSV Vault`
  folder, or to `~/PoolWind/CSV Vault` without a stick.

## Hardware facts (measured on the author's pool)

- Raspberry Pi 5, Raspberry Pi OS (Debian 13 trixie), Python 3.13, X11.
  The same `poolwind.py` runs on Windows as a demo: the Pi libraries
  (`lgpio`, `board`, `adafruit_ina260`) are optional, and without them a
  real valve falls back to the simulated jet with a message.
- Relays on GPIO 17 (UP), 18 (DN), 27 (pump On/Off), **active low**: writing
  0 turns a relay on. They "press" the buttons of a spare pool remote.
- The jet speed is read as a voltage from the pool's Pace Display port by an
  INA260 on I2C (`i2cdetect -y 1` should show it, normally at 0x40).
- One UP/DN step moves the voltage about 0.04 V, all at once (under 0.05 s).
  Reading noise is about 0.0013 V. On the author's pool the jet runs from
  about 1.2 V (slowest) up.
- The radio remote loses 30-50% of single short presses, so PoolWind
  **holds** UP or DN and lets go once the voltage has moved. A held button
  gives its first step 0.2-1.7 s after the press, then one about every
  0.95 s.
- The pool accepts only one remote at a time. While PoolWind runs, it
  overrides the pool's own remote.

## How the program works (poolwind.py)

- `App`: settings, relays (`UP_relay`, `DN_relay`, `relay_off`), the jet
  drive (`_hold_drive`), logging (`accrue_log_disp`), buttons (Hold, Suspend,
  OnOff), USB stick handling, settings hot-reload.
- `QtMainWindow.qt_update_loop`: the main loop. It reads a frame, finds the
  swimmer, updates the position, runs the controller and drives the relays.
- `MyVideoCapture`: the camera. MJPG 1280x720 at 30 fps, read by a grabber
  thread (`_grabber`). `getImages` shrinks the frame to 640x480, turns it
  upright, then straightens the swim area to 480x640 with the calibration
  file's `swimAreaPoints`. The jet is at the top of that picture.
- Swimmer detection (`F_mask`): distance in HSV from the picture's average
  color, a threshold, then the best-scoring blob of at least `Sensitivity`
  pixels (5000). Small objects such as a ping-pong ball are deliberately
  ignored. `get_auto_CoM` and `BodyCoMCorrection` turn the blob into a
  position from 0 (back) to 1000 (front), allowing for the swimmer's reach
  (`swimmersHeight`, `usableSwimLength`; the old name `usablePoolLength`
  is still read).
- `SwimController`: `_zone_steps` divides the pool into equal zones, **one per
  jet step**: the pace table's rows (rows within 0.01 V count once) that lie
  inside the swimmer's zone limits (`'zoneMin, Max'`, 1-based step numbers)
  and the safety limits. The calibration's `'# zones or auto'` can ask for
  fewer zones, spread evenly by voltage. `_index_for_CoM` maps the position
  to a zone, and so to a target jet step. The pool is controlled by jet
  steps; Pace is for display and the swim log only. In a demo, and while
  Swimmer limits runs, the zones open to the whole safety range
  (`App.zone_limits`).
- Swim pace estimate: water speed from the voltage (through the pace table),
  plus the swimmer's drift, weighted by `DRIFT_SCALE` (1.5).
- `SimulatedValve`: the jet for desk tests and the demo. `SwimPlotWindow`:
  swim review with synchronized video. `USBDriveSetupDialog`: new swimmer
  sticks. `SwimmerLimitsPanel` and `PaceCorrectionPanel`: the small boxes
  over the pool screen (menu). `QtMainWindow.check_camera_moved`: the
  camera check a few seconds after start, against
  `poolwind_calibration_camera.png`.
- The calibration (`CalibrateWindow`, the voltage scan, Pace Entry,
  PingPong) is a section of the same file: menu **Calibrate pool...**
  (real valve only), or `python3 poolwind.py --calibrate`
  (`calibration_main`; `--simulate --window` at a desk, and always
  simulated while Demo is on).

## Finding out what's wrong

- **Run PoolWind from a terminal** to see its messages; the desktop icon
  hides them: `cd ~/PoolWind && python3 poolwind.py`. On Windows, in
  PowerShell: `cd $HOME\PoolWind` then `py -X utf8 poolwind.py`.
- **The install log:** `~/PoolWind/install.log` records every install step
  and its output.
- **Desk testing** (setup guide, section 8): `'developerMode': True` plus a
  simulated valve and/or a recorded video, so nothing at the pool moves.
- **Developer traces:**
  - `'paceTrace': True` in the defaults file writes `pace_trace_*.csv` next to
    the program, one row per loop: voltage, paces, position, swimmer found,
    target step, relay. It's switched live and grows about 15 MB an hour.
  - `recordRawVideo` (calibration file, works only with `'developerMode':
    True`) records the camera's uncorrected video for replaying a problem.
- **The camera:** `v4l2-ctl -d /dev/video0 --list-formats-ext` lists the
  sizes and frame rates it offers; `v4l2-ctl -d /dev/video0 --list-ctrls`
  lists exposure and other controls.
- **Hardware access:** check `groups` includes `gpio`, `i2c` and `video`
  (they apply after a restart).

## Known problems and their fixes

- **Camera without MJPG 1280x720 at 30 fps.** PoolWind asks for that mode;
  OpenCV quietly gives a camera's nearest mode. Check what the camera
  offers (above). The working picture is always resized to 640x480, so
  another size with the same 4:3 or 16:9 shape is usually fine; change the
  three `vidSrc.set(...)` lines in `MyVideoCapture.__init__` and
  re-set the swim area. YUYV at large sizes is too slow (often 5-10 fps).
- **Camera at 15 fps instead of 30.** On the author's camera,
  `CAP_PROP_BUFFERSIZE` 1 (set in `MyVideoCapture.__init__`) halves the
  rate. Removing that line gives 30 fps; the grabber thread keeps frames
  fresh anyway. The extra cost is about 6% of one core. Check with a
  short timing loop around `vidSrc.read()`.
- **Swimmer not found / jet not following.** Usually the swim area (setup
  guide 5.1: corners on the water surface, redo it if the camera moved),
  lighting (outdoor sun, glare and sharp shadows are untested), or the
  center lane (`middleSwimZone %`). The zone highlight and the
  developer readouts show what PoolWind sees.
- **DEMO on the screen, the jet doesn't respond.** `'Demo'` isn't
  `False` in `poolwind_defaults.txt` (setup guide, section 4).
- **"Video file not found".** The sample video didn't download (it's a
  GitHub Release file, `PoolWind_demo.mp4`), or a
  `'video file, start (sec), corners'` line names a missing file.
  PoolWind then uses the camera. Running the install script again retries
  the download.
- **Windows: "Windows protected your PC" or a browser warning** for
  `install_windows.bat`: expected for an unsigned script (setup guide,
  section 13): **More info → Run anyway**.
- **Jet doesn't move.** Check that the demo is off, that the voltage is read at all (a reading near 0 V
  means the Pace cable is unplugged, or, on some pools, the pump is off), that the remote
  works by hand, and the relay wiring (build guide, section 9, first
  power-up checks).
- **Install command typed wrongly.** `~` is easily read as `-`; the setup
  guide's commands avoid `~` for this reason. If `bash install.sh` says
  "No such file or directory", the user isn't in the downloaded folder:
  open it in the File Manager and press F4 for a terminal there.
- **Wayland instead of X11.** The installer switches to X11 (needed by the
  Monitor Toggle and RealVNC); it takes effect after a restart.
- **The pace table doesn't fit the user's pool.** The shipped table is
  the author's pool. The calibration built into PoolWind (menu
  **Calibrate pool...**, or `python3 poolwind.py --calibrate`; setup guide
  5.2) scans the user's jet steps and rewrites the table.
- **A pool whose speed voltage drops to zero while its pump is off.** On the
  author's pool the voltage is always there, and PoolWind assumes so. On
  such a pool, with the pump off and a swimmer in the swim area, PoolWind
  sees the jet below the slowest zone and holds UP; if that pool's valve
  can move while it is off, the jet could start fast when it's turned on.
  A fix: treat a reading far below the safety minimum as "no feedback" and
  press neither UP nor DN until a good reading returns, then wind down
  once.
