# PoolWind Setup and Calibration Guide

**DRAFT.** Comments like `<!-- Bill: ... -->` are notes for the author.
They don't show on GitHub.

This guide is for the person who builds and installs PoolWind: installing
the software, fitting it to your pool, and the settings behind the scenes.
Swimmers only need the [user manual](USER_MANUAL.md).

**Please read [SAFETY.md](../SAFETY.md) first.** Several steps here move the
pool's jet. Do them with nobody in the pool.

## Contents

1. [What you need](#1-what-you-need)
2. [Preparing the SD card](#2-preparing-the-sd-card)
3. [Installing PoolWind](#3-installing-poolwind)
4. [First start](#4-first-start)
5. [Calibrating for your pool](#5-calibrating-for-your-pool)
6. [The settings files](#6-the-settings-files)
7. [Built-in settings](#7-built-in-settings)
8. [Testing at a desk](#8-testing-at-a-desk)
9. [Working from home](#9-working-from-home)
10. [Updating PoolWind](#10-updating-poolwind)
11. [Backups](#11-backups)

---

## 1. What you need

- The PoolWind hardware, built and wired as in the build guide: the
  Raspberry Pi 5, monitor, camera, INA260 voltage sensor, relay board and
  the modified pool remote.
- A microSD card, 32 GB or larger. A "high endurance" card lasts longest.
- A PC with **Raspberry Pi Imager** (free from raspberrypi.com) to write the
  card.
- An internet connection for the Pi during installation.
- A USB stick for each regular swimmer (optional): it holds their own
  settings, swims and videos. See the [user manual](USER_MANUAL.md).

## 2. Preparing the SD card

1. In Raspberry Pi Imager, choose:
   - **Device:** Raspberry Pi 5
   - **Operating system:** Raspberry Pi OS (64-bit), the version *with
     desktop*
   - **Storage:** your microSD card
2. Imager then offers to **customise** the system (in older versions:
   **OS customisation → Edit settings**). Fill in:
   - **Hostname:** for example `poolwind`
   - **Username and password:** your choice. Remember them.
   - **Wi-Fi:** your network name and password, if the Pi won't use a cable
   - **Time zone and keyboard layout**
   - **SSH** (remote access): turn it on if you want to reach the Pi from
     another computer
3. Write the card, put it in the Pi and switch on. The first start takes a
   few minutes.

## 3. Installing PoolWind

Open a terminal on the Pi: click the **Terminal** icon (a black screen
with `>_`) on the bar at the top of the desktop. Type these two lines,
pressing Enter after each:

```
git clone https://github.com/WillyAG/PoolWind.git ~/PoolWind-download
bash ~/PoolWind-download/install.sh
```

The first line downloads PoolWind into a `PoolWind-download` folder. The
second runs the install script.

**It asks for your password once:** the password you chose in Raspberry Pi
Imager (section 2). Nothing shows on the screen while you type it, not even
dots; type it and press Enter.

The install script:

- installs the libraries PoolWind needs: OpenCV, NumPy, SciPy, PyQt5,
  matplotlib, lgpio, the Adafruit INA260 library, ffmpeg, exfatprogs and
  i2c-tools;
- turns on **I2C**, which the voltage sensor uses;
- switches the desktop to **X11**, the setup PoolWind is tested on (new
  Raspberry Pi OS installs start with the newer Wayland desktop). X11 is
  also what makes [working from home](#9-working-from-home) possible;
- turns on **VNC**, so you can use the Pi's desktop from another computer;
- lets PoolWind set up new USB sticks for swimmers without asking for a
  password;
- copies PoolWind into a **`PoolWind` folder** in your home folder. This is
  where the program, its settings files and the `CSV Vault` live;
- adds two icons to the desktop: **PoolWind**, and **Monitor Toggle** for
  [working from home](#9-working-from-home);
- turns the monitor to **portrait** (taller than wide) every time the Pi
  starts, ready for swimming.

It writes everything it does to a log file, `install.log`, in the
`PoolWind` folder. If something goes wrong, that's the place to look.

It never overwrites settings or calibration files you already have, so it's
safe to run again. When it updates the program, it keeps the previous one
as `poolwind.py.previous`.

When it finishes, **restart the Pi.**

## 4. First start

Before the first start:

- **Nobody in the pool.**
- The pool switched on, with the pool's own remote at hand.
- **The monitor is in portrait** (taller than wide). The install script
  sets this up, so it happens by itself a few seconds after the desktop
  appears. If it doesn't, double-click **Monitor Toggle**, and if your
  monitor isn't the author's, see [working from home](#9-working-from-home)
  for its settings.
- **Calibration:** the `poolwind_calibration.txt` that comes with PoolWind
  holds the author's pool. Its pace table should be close for a pool of
  the same model (section 5.2), but **set the swim area for
  your own camera** (section 5.1) and check the safety limits (section 5.3)
  before the first swim.

Double-click the **PoolWind** icon. Then:

1. **"Starting Up: Please wait for voltage wind down"**: with a real valve,
   PoolWind first brings the jet to its lowest setting.
2. The pool screen appears, showing the camera's view from above.

Check that:

- the camera shows the whole pool, from above;
- the large pace, average and distance are readable from the water;
- **the jet answers.** With nobody in the pool, press **Hold**, then
  **UP** a few times and **DN** a few times (one jet step per press, see
  the [user manual](USER_MANUAL.md)), and watch the jet change. Then close
  PoolWind: it winds the jet back down.
  <!-- Bill: does Hold step the jet with nobody in the pool, or does the
  inactivity wind-down take over? This is the same question as the build
  guide's relay test (section 9, step 4); settle both at the pool session. -->

## 5. Calibrating for your pool

These settings fit PoolWind to **your** pool. They're stored in
`poolwind_calibration.txt`, next to the program.

> **The calibration file is safety-critical.** It decides which voltages
> PoolWind drives the jet to. Only someone who understands the system should
> change it.

### 5.1 The swim area

This tells PoolWind where the pool is in the camera's picture.

1. On the pool screen, open the menu (**≡**, top left) and choose
   **Set Swim Area...**.
2. Click the **four corners of the swim area**. Follow the inner benches,
   except at the rear, and click on the **water surface**, not the pool
   floor.
3. Drag any corner to adjust it. **Reset** starts over.
4. Press **Save**. The swim area is saved to the calibration file
   immediately.

Do this again if the camera is ever moved.

### 5.2 The pace table (`pace_voltage`)

PoolWind reads the jet speed as a voltage on the pool's Pace Display port.
The voltage changes steadily with the jet speed: the same jet speed always
gives the same voltage. To turn a voltage into a pace, PoolWind needs a
table of pairs: the pace, and the voltage at that pace.

**The table that comes with PoolWind was measured on the author's pool, a
Standard Endless Pool.** On a pool of the same model it should be close
enough to start with, but it hasn't been checked on any other pool.
Measuring your own table is optional, and can be done later.

**To measure your own table,** use the PoolWind calibration program
(planned). It will build the table automatically, reading each voltage
through PoolWind's own voltage sensor. You'll only need to do one of two
things at each jet speed: type in the pace shown on your Pace Display, if
you have one, or drop ping-pong balls in the water for it to time.
<!-- Bill: link to the calibration program's description once it exists. -->

```
'pace_voltage': [
    (7.0, 1.185),
    (6.85, 1.186),
    ...
    (1.46, 2.43),
    (1, 2.5)
]
```

Each pair is (pace in minutes per 100 yards as a decimal, volts). For example
`2.25` means 2:15. List them from slowest to fastest.

### 5.3 Safety voltage limits

```
'SafetyVoltageLimits': (1.46, 2.15)
```

- The **first** number is the jet's lowest voltage. PoolWind winds the jet
  down to this at startup and shutdown.
- The **second** number is the highest voltage PoolWind may ever drive the
  jet to, whatever any pace setting says. Set it at the fastest pace you're
  willing to let PoolWind reach in your pool.

With the author's pace table, `(1.46, 2.15)` keeps the jet between about
4:49 and 1:49 per 100 yards.

Changes to the calibration file take effect at the next start.

### 5.4 Pool length and the center lane

```
,'poolLength': 180

,'middleSwimZone %': 35
```

- **`poolLength`** is the swim area's length, front to back, in inches.
  PoolWind uses it to turn positions in the camera picture into distances.
- **`middleSwimZone %`** is the width of the center lane where PoolWind
  tracks the swimmer, as a percentage of the swim area's width. Wider
  catches a swimmer who drifts sideways; narrower ignores people standing
  beside the pool. 35 % works well in the author's pool.

### 5.5 Raw video (development only)

```
'recordRawVideo': False
```

`True` records the camera's full, uncorrected video, but only when
`'developerMode'` is on. The files are large. It's a tool for developing
the swimmer detection.

## 6. The settings files

PoolWind keeps its settings in plain text files next to the program, all
starting with the program's name:

| File | Holds | Who changes it |
|---|---|---|
| `poolwind_defaults.txt` | The swimmer settings for anyone without a USB stick | The owner |
| `poolwind_calibration.txt` | Pace table, safety limits, swim area, pool length, center lane, raw video | Technician only |
| `poolwind_ind_defaults.txt` (on each USB stick) | One swimmer's own settings | That swimmer |

The swimmer settings use **the same names** in the defaults file and on
the USB sticks. A stick's value wins while it's inserted. See the
[user manual](USER_MANUAL.md#8-your-settings) for the list.

**The defaults file as shipped** uses a moderate top pace, 3:00 per 100
yards, and an average height. If you raise the top pace for yourself,
remember it applies to anyone who swims without their own stick.

**Recording rate (`'logRate'`).** How many swim log records, and training
video frames, PoolWind saves per second: 1 to 15, read when PoolWind
starts. Set it in the defaults file for everyone (a coach's choice, for
example) or on a swimmer's stick for that swimmer.

| `'logRate'` | Video | Storage | A 32 GB stick holds |
|---|---|---|---|
| `5` (shipped) | Steps visibly between frames; enough to follow pace and stroke rhythm | About 7 MB a minute | About 70 hours |
| `15` | Smooth stroke detail, even slowed down | About 20 MB a minute | About 25 hours |

Higher rates also use more of the Pi's time (about 10 % at 15), so 15 is the
limit.

The files are written like this:

```
{
'swimmersHeight': 66

,'paceMin, Max': ('5:00', '3:00')
}
```

- Keep the curly brackets around everything.
- Every setting after the first starts with a comma.
- Text goes in quotes. `True` and `False` have capital letters.
- Lines starting with `#` are comments, ignored by PoolWind.

If the defaults or calibration file can't be read when PoolWind starts, it
says why in the terminal and doesn't start. If you make a mistake while it's
running, it says so and keeps the last good settings.

The program never rewrites the defaults file, so your comments stay.

## 7. Built-in settings

These were tuned during development and are built into the program. To
change one, add its line to `poolwind_defaults.txt`, with exactly the same
name. The file's value then replaces the built-in one. Delete the line to
go back.

Most take effect while PoolWind is running. Those marked **restart** need
PoolWind to be closed and started again.

| Setting | Built-in value | What it does |
|---|---|---|
| `'Sensitivity'` | `5000` | Minimum size, in pixels, of something the camera counts as a swimmer |
| `'CoM filter Alpha'` | `0.05` | Smoothing of the swimmer's position. Smaller is smoother but slower to react |
| `'inactivity wind down time (sec)'` | `3` | How long the swimmer may be out of the lane before the jet winds down (**restart**) |
| `'DRIFT_SCALE'`, `'WATER_TAU'`, `'DRIFT_TAU'`, `'DRIFT_MAX'` | `1.5`, `5.0`, `5.0`, `25.0` | The Swimmer Pace estimate. Leave these alone unless you're developing |
| `'developerMode'` | `False` | Developer tools: see [Testing at a desk](#8-testing-at-a-desk). Also shows the position bar and the `dIdx`, `V` (jet voltage) and `CoM` readouts on the pool screen, lets a click on the Swim Plot video show the position bar there, and allows raw video. Users leave it off: the position bar also moves with swim angle and depth, not just the stroke, which would confuse a swimmer |
| `'paceTrace'` | `False` | Developer: writes a detailed `pace_trace_*.csv` file of the pace estimate, about 15 MB an hour |
| `'Runtime: hotReloadParameters'` | `True` | Picks up settings changes while running |

The swimmer settings also have built-in fallbacks, used only if the
defaults file leaves them out: `'paceMin, Max': ('5:00', '1:30')`,
`'algorithm (basic or swimmerPace)': 'swimmerPace'` and `'logRate': 5`.

## 8. Testing at a desk

These developer settings let you run PoolWind without the pool. They only
work with `'developerMode': True` in `poolwind_defaults.txt`. With it off,
PoolWind always runs the real pool setup, whatever the file says. Add them
to `poolwind_defaults.txt`; they all need a **restart**.

| Setting | Normal | Meaning |
|---|---|---|
| `'Valve (real or simulate)'` | `'real'` | `'simulate'` runs without pressing the remote's buttons |
| `'capture_device (camera or video)'` | `'camera'` | `'video'` plays a recorded swim instead of the live camera |
| `'display_device (work or pool)'` | `'pool'` | `'work'` switches the monitor to landscape for programming, and `'pool'` back to portrait (monitor mode set in the program code) |
| `'workplace (home or pool or default)'` | `'pool'` | Sets all three above at once: `'home'` = video, work, simulate; `'pool'` = camera, pool, real; `'default'` = use the three lines as written |

The pump relay is only connected when the workplace is `'pool'`. So
`'default'` with `'Valve (real or simulate)': 'real'` tests the speed
relays at a desk with no chance of starting the pool's pump.

In `'video'` mode, the recorded video and its swim area are set in the
program code, next to the video's file name.

Before swimming, delete these lines or set `'developerMode': False`.

## 9. Working from home

You can work on the Pi from a computer elsewhere in the house while it
stays at the pool: change settings, look at swim logs, or work on the
program.

**Connecting:**

1. On your computer, install **RealVNC Viewer** (free from realvnc.com).
2. Connect to the Pi by its name, for example `poolwind.local` (the
   hostname you chose in section 2), or by its network address. Your
   computer and the Pi must be on the same home network.
3. Log in with the Pi's username and password.

**The Monitor Toggle icon.** In portrait, the pool monitor's picture is too
narrow to work in comfortably, and VNC shows you the same picture. Double-click
**Monitor Toggle** on the Pi's desktop to turn the monitor to **landscape**
(full width) while you work. Double-click it again to turn it back to
**portrait**. Restarting the Pi also turns it back to portrait.

> **Always turn the monitor back to portrait before anyone swims.**

The toggle is set up for the author's monitor (the Eyoyo 10-inch on the
parts list): portrait at 800×600, landscape at 1280×800, on the output
called `HDMI-1`. With a different monitor, open
`~/.local/bin/toggle_monitor.sh` in a text editor and change the three
settings at its top. To see your monitor's output name and sizes, type
`xrandr` in a terminal.

## 10. Updating PoolWind

Download the new version and run the install script again:

```
cd ~/PoolWind-download
git pull
bash install.sh
```

Your settings, calibration, swim logs and videos are kept.

## 11. Backups

The install script can rebuild the software at any time. What it **can't**
rebuild is yours, so back it up:

- `poolwind_calibration.txt`: your pool's measurements;
- `poolwind_defaults.txt`: your settings;
- the `CSV Vault` folder next to the program, for swimmers without a stick;
- each swimmer's USB stick, which holds their swims and videos.

Copy them to a PC or another USB stick now and then, and always before
changing the SD card.
