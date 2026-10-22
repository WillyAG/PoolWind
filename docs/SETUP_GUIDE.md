# PoolWind Setup and Calibration Guide

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
12. [Getting help](#12-getting-help)
13. [Trying PoolWind on a PC](#13-trying-poolwind-on-a-pc)

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
with `>_`) on the bar at the top of the desktop. Type these three lines,
pressing Enter after each:

```
git clone https://github.com/WillyAG/PoolWind.git PoolWind-download
cd PoolWind-download
bash install.sh
```

The first line downloads PoolWind into a `PoolWind-download` folder in your
home folder (where a new terminal starts). The second goes into that
folder, and the third runs the install script. Capitals and the `-` matter.

If the third line says "No such file or directory", open the
`PoolWind-download` folder in the File Manager instead, press **F4**
(Open Current Folder in Terminal) and type `bash install.sh` there.

**It asks for your password once:** the password you chose in Raspberry Pi
Imager (section 2). Nothing shows on the screen while you type it, not even
dots; type it and press Enter.

The install script:

- installs the libraries PoolWind needs: OpenCV, NumPy, SciPy, PySide6,
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

When the screen comes back, there will be a "PoolWind" icon. WHen you press it, it will come up in demo mode.

## 4. First start

Suggested before starting:

- Nobody in the pool
- The pool is switched off
- the pool's own remote at hand
- **The monitor is in portrait mode** (taller than wide). The install script
  sets this up, so it happens by itself a few seconds after the desktop
  appears. If it doesn't, double-click **Monitor Toggle**. 

Double-click the **PoolWind** icon. You will see:

The pool screen appears, showing the camera's view from above.

Check that:

- the camera shows some of the pool from above (will set the correct view later)
- 
- **the jet answers.** With nobody in the pool, press **Hold**, then
  **UP** a few times and **DN** a few times (one jet step per press, see
  the [user manual](USER_MANUAL.md)), and watch the jet change.
- **OnOff winds the jet down.** Press **OnOff**: the jet winds down to its
  lowest setting first, then the pump turns off. Press it again to turn the
  pump back on. While it winds down, **On/Off now** in the message switches
  the pump at once, for emergencies: try it once.

## 5. Calibrating for your pool

These settings fit PoolWind to **your** pool. They're stored in
`poolwind_calibration.txt`, next to the program. Do them in this order,
which is also the order of PoolWind's menu:

1. **Set Swim Area** (5.1): where the pool is in the camera's picture.
2. **Calibrate pool** (5.2): your pool's voltages, safety limits and Pace
   table.
3. Each swimmer's **Swimmer limits**: see the
   [user manual](USER_MANUAL.md#swimmer-limits-your-slowest-and-fastest-zone).

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

**The camera check.** Saving the swim area also saves the camera's
picture, as `poolwind_calibration_camera.png` next to the calibration file.
A few seconds after each start, PoolWind compares the camera's picture with
it, looking only outside the water (deck, benches, jet unit). If the camera
has moved, it asks **Camera moved?** and offers:

- **Adjust**: move the swim area with the picture (and save it);
- **Keep**: leave it as it is (it asks again at the next start);
- **Set Swim Area**: set the corners again yourself.

**Adjust** moves the swim area's four corners with the picture (sideways,
up and down, a slight turn, nearer or farther) and saves them, so the next
start uses them and doesn't ask again.

If the camera has moved **too far to follow** (part of the pool out of the
picture, or turned or tilted more than a little), or PoolWind **can't
recognize the pool** although the light is about the same, it says
**Check the camera** instead: move the camera back so it sees the whole
pool as before, then start PoolWind again, or press **Set Swim Area**.

Changing the swim area on purpose, for example for a jet box extension,
saves a new picture, so the check never asks then. If the swim area's
length changed, change `usableSwimLength` too (5.4). In the dark, when
there isn't enough to compare, the check says nothing.

### 5.2 The calibration program

PoolWind needs a **Pace table** for your pool: which jet voltage goes with
which pace. The calibration measures it through PoolWind's own voltage
sensor and relays.

**Pace here is only an estimate.** It can never be exact due to the
varying speed of layers as you go from top to bottom. It is different for
stroke styles and body types depending on how deep you go (your legs
mostly). But after calibration, it is close and consistent enough for
training. You can only measure an accurate Pace in a regular pool.

**Before you start**

- **Nobody in the pool.** The jet goes up to fast speeds.
- The pool's **pump on**, and the swim area set (5.1).

On the pool screen, open the menu (**≡**, top left) and choose
**Calibrate pool...**. PoolWind winds the jet down and hands it to the
calibration; when you close the calibration, PoolWind uses the new table
at once. (On a first install, or if PoolWind won't start, the calibration
also runs on its own: `python3 poolwind.py --calibrate` in a terminal, in
the PoolWind folder. Close PoolWind first then: both use the same relays.)

The first screen explains each choice. Only **Begin initial voltage scan**
can be pressed until the scan is done.

**Step 1: Initial voltage scan (once for each setup)**

Every pool sends different voltages. The scan runs the jet from its
slowest to its fastest speed, finds your pool's voltage range, and fits
PoolWind's safety limits, its settings and the shipped Pace table to it.
Pace Entry and PingPong need this to step your jet; they then replace the
table's paces with your own.

1. Press **Begin initial voltage scan**, then **Start**. The calibration
   reads the voltage for a few seconds, takes the jet down to its slowest
   speed, then steps it up, counting the steps.
2. **Watch and listen to the pool.** When it sounds too fast or strained,
   or the Pace Display stops changing, press **Stop**, then **Use as
   top**: that speed becomes your pool's top speed for PoolWind, and
   PoolWind never drives the jet faster. Otherwise the scan goes on until
   the jet stops getting faster.
3. The jet is taken back down, and the results show your pool's range,
   its number of steps and the new Pace table: **one row for each jet
   step**. These rows are PoolWind's **zones**. If your pool is the same
   as the one the table was made on (same slowest step and step size), the
   paces stay as they were. On another pool, the table's shape is moved to
   yours: a starting point, until you measure your own (step 2).
4. Press **Save scan**. The calibration file is written (the old one is
   kept as `poolwind_calibration_before_<date>.txt`), and the other choices
   open. The scan is also kept as `calibration_scan_<date>.csv`.

To scan again later (a new pool, a new controller), change
`'InitialCalFinished': True` to `False` in the calibration file.

**Step 2: the paces. Choose one:**

- **Pace Entry**, if your pool has a **Pace Display**. The calibration
  steps the jet up one step at a time; at each step, wait until the
  display is steady, type the pace it shows on the number pad (`2:15`, or
  just `215`) and press **Record**. Check the **highest voltage** first:
  it never steps above it. Press **Finish** when the jet is as fast as you
  want to go, or when the display stops changing (it offers to finish when
  the display shows the same pace twice). **Fix row** changes a row: tap
  it, type the right pace, press Fix row. About 30 steps, 15-20 minutes.
- **PingPong**, without a Pace Display. You need five **orange** ping-pong
  balls (bright or fluorescent; white ones don't work). At every 3rd step
  (you can choose every step), the calibration waits for the water to
  catch up, then asks for balls: set one gently on the water right at the
  jet, in the middle, and take your hand out of the picture; drop the next
  when it reaches the back wall. When 3 drops agree, it steps on by itself.
  The steps in between are filled in. Collecting the balls is the tedious
  part. About 25-35 minutes. The ball floats on the fastest water, so its
  pace is turned into a swimming pace with a factor measured on the
  author's pool: the new table is only estimated, and you may want to
  correct it afterwards.

Each ends with a results table, new against current. **Save table** writes
it (with a backup); **Quit** without saving keeps the current table. Every
reading is kept in `calibration_session_<date>.csv`. **Stop** lets go of
the buttons at once, any time; **Finish** takes the jet down to its
slowest speed and shows the results.

**The Paces don't feel right?** Use **Pace correction...** in PoolWind's
menu: you swim at a Pace you know and type what it should be (see the
[user manual](USER_MANUAL.md#pace-correction-when-the-paces-dont-feel-right)).

**The table in the file** looks like this:

```
'pace_voltage': [
    (5.2067, 1.22),
    (4.9933, 1.294),
    ...
    (1.4839, 2.397),
    (1.4297, 2.435)
]
```

Each pair is (pace in minutes per 100 yards as a decimal, volts). For example
`2.25` means 2:15. After a scan there is one pair per jet step, slowest
first. The table that comes with PoolWind was measured on the author's
pool, a Standard Endless Pool, with PingPong.

### 5.3 Safety voltage limits

```
'SafetyVoltageLimits': (1.46, 2.15)
```

- The **first** number is the jet's lowest voltage. PoolWind winds the jet
  down to this when **OnOff** is pressed, before it switches the pump.
- The **second** number is the highest voltage PoolWind may ever drive the
  jet to, whatever any swimmer's setting says. Set it at the fastest speed
  you're willing to let PoolWind reach in your pool.

The calibration's scan fits both to your pool's voltages, and where you
stopped the scan (**Use as top**) is a ceiling: the second number is never
above it. Zones outside these limits are never used. With the author's
pace table, `(1.46, 2.15)` keeps the jet between about 4:17 and 1:46 per
100 yards.

Changes to the calibration file take effect at the next start.

### 5.4 Usable swim length and the center lane

```
,'usableSwimLength': 162

,'middleSwimZone %': 35
```

- **`usableSwimLength`** is the swim area's length in inches: from the back wall
  to the edge of the jet unit, **not** the whole pool. It's the same length
  as the swim area you set in [5.1](#51-the-swim-area). On the author's
  Standard Endless Pool, the pool is 180" long and the jet unit's edge is
  18" from the front, so `usableSwimLength` is 162. PoolWind uses it to turn
  positions in the camera picture into distances: how far your fingertips
  and toes reach toward each end, and how fast you drift forward or back. (Before v15.5 it was called `usablePoolLength`, before v15.3 `poolLength`; older files still work.)
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

### 5.6 Number of zones

```
,'# zones or auto': 'auto'
```

`'auto'` (shipped): one zone for every jet step between the swimmer's
limits. A number, for example `10`: that many zones, spread evenly between
the limits, each on the nearest jet step. Fewer zones mean fewer jet
changes, which is easier on the equipment; try what feels right. A number
larger than the steps available, or not a number, means `'auto'`.

## 6. The settings files

PoolWind keeps its settings in plain text files next to the program, all
starting with the program's name:

| File | Holds | Who changes it |
|---|---|---|
| `poolwind_defaults.txt` | The swimmer settings for anyone without a USB stick | The owner |
| `poolwind_calibration.txt` | Pace table (the zones), safety limits, swim area, swim length, center lane, number of zones, raw video, and the scan's results (`InitialCalFinished`, `jetVoltageRange`, `jetSteps`) | The calibration and the technician |
| `poolwind_calibration_camera.png` | The camera picture the swim area was set on (the camera check, 5.1) | PoolWind, when the swim area is saved |
| `poolwind_ind_defaults.txt` (on each USB stick) | One swimmer's own settings | That swimmer |

The swimmer settings use **the same names** in the defaults file and on
the USB sticks. A stick's value wins while it's inserted. See the
[user manual](USER_MANUAL.md#8-your-settings) for the list.

**The defaults file as shipped** uses a moderate top pace, 3:00 per 100
yards, and an average height. If you raise the top pace for yourself,
remember it applies to anyone who swims without their own stick.

**Zones on the sticks.** A swimmer's stick holds their slowest and fastest
**zone** (`'zoneMin, Max'`), set with Swimmer limits. The defaults file may
use zones too, or, as shipped, a pace range (`'paceMin, Max'`), which
PoolWind turns into zones through the Pace table. Zone numbers belong to
the Pace table they were set on: after a new scan, set the swimmers'
limits again.

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

**Ejecting the stick at close (`'ejectStickOnClose'`).** `True` (shipped):
when PoolWind closes, it writes everything to the swimmer's USB stick and
unmounts it, so it's safe to remove. There's no message, except when
something else was using the stick and it couldn't be ejected. The stick
isn't powered off, so if it stays in, the next start mounts it again: no
need to unplug it to come straight back in. `False`: PoolWind writes
everything to the stick but leaves it mounted, so its files still show in
the File Manager. `False` suits a single swimmer who leaves the stick in
the Pi (and a developer); `True` suits a coach, or several swimmers each
taking their stick away. A coach who needs to edit a `True` stick plugs it
in, or unplugs it and plugs it back in, while PoolWind is closed. A `False` stick must still be
ejected with the eject icon (⏏) in the top bar before it's removed. Set it in the defaults file for everyone, or on a
swimmer's stick for that swimmer. New sticks get the defaults file's
value.

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
| `'Demo'` | `True` | Runs the program in demo mode. Does not further hardware including pool. Most routines are functional.|
| `'Sensitivity'` | `5000` | Minimum size, in pixels, of something the camera counts as a swimmer |
| `'CoM filter Alpha'` | `0.05` | Smoothing of the swimmer's position. Smaller is smoother but slower to react |
| `'inactivity wind down time (sec)'` | `3` | How long the swimmer may be out of the lane before the jet winds down (**restart**) |
| `'DRIFT_SCALE'`, `'DRIFT_TAU'`, `'DRIFT_MAX'` | `1.5`, `5.0`, `25.0` | The Swimmer Pace estimate. Leave these alone unless you're developing |
| `'WATER_TAU'` | `5.0` | Seconds the water takes to catch up after the jet changes speed, for the Swimmer Pace estimate. (The [zone highlight](USER_MANUAL.md#seeing-the-jets-zone-the-zone-highlight) follows the jet directly.) |
| `'zoneHighlight'` | `False` | Whether the zone highlight is on when PoolWind starts. A tap on the picture turns it on or off either way |
| `'zoneHighlightLevel'` | `0.2` | How bright the zone highlight is: `0.05` is barely seen, `0.3` is strong |
| `'developerMode'` | `False` | Developer tools: see [Testing at a desk](#8-testing-at-a-desk). Also shows the position bar and the `dIdx`, `V` (jet voltage) and `CoM` readouts on the pool screen, shows the position bar on the Swim Plot video while the zone highlight is on, and allows raw video. Users leave it off: the position bar also moves with swim angle and depth, not just the stroke, which would confuse a swimmer |
| `'readouts'` | `True` | Developer: with `developerMode` on, `False` hides the `dIdx`, `V` and `CoM` numbers on the pool screen (for example for a screenshot) |
| `'comBar'` | `True` | Developer: with `developerMode` on, `False` hides the position bar (pool screen and Swim Plot) but keeps the readouts. The zone highlight is the steadier reference |
| `'algorithm (basic or swimmerPace)'` | `'swimmerPace'` | Developer: the control method. `'swimmerPace'` is the method the manuals describe; leave it. `'basic'` is a simple baseline for building new control methods on. Main defaults file only: a USB stick's line is ignored |
| `'paceTrace'` | `False` | Developer: writes a detailed `pace_trace_*.csv` file of the pace estimate, about 15 MB an hour |
| `'Runtime: hotReloadParameters'` | `True` | Picks up settings changes while running |

The swimmer settings also have built-in fallbacks, used only if the
defaults file leaves them out: every zone inside the safety limits
(`'zoneMin, Max': None`) and `'logRate': 5`.

**The swim log** (`CSV Vault/<date>.csv`, one line per record, no header):
time, pace, distance, video segment, frame, position (`CoM_h`), swimmer
tick (`CoM_w`, `-1` = none), and since the zone highlight, the jet's zone
(`-1` = none) and the number of zones. Older files without the last two
columns replay without the highlight.

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
|`'video file'` | video filename | PoolWind plays the recorded swim named in this setting, starting the given number of seconds in, with the swim area's four corners of that video.|



To add them, copy these lines into `poolwind_defaults.txt`, just before
the closing `}`. They're set for pool use, so nothing changes until you
change a value: for a desk test, change `'pool'` on the workplace line to
`'home'`.

```
,'developerMode': True
,'workplace (home or pool or default)': 'pool'
,'capture_device (camera or video)': 'camera'
,'display_device (work or pool)': 'pool'
,'Valve (real or simulate)': 'real'
,'video file, start (sec), corners': ('poolwind_sample.mp4', 0, [(141, 151), (475, 146), (377, 608), (190, 585)])

```

The pump relay is only connected when the workplace is `'pool'`. So
`'default'` with `'Valve (real or simulate)': 'real'` tests the speed
relays at a desk with no chance of starting the pool's pump.

The sample video:
That is the built-in value. To use your own
recording, add the line to `poolwind_defaults.txt` with its file name
(next to the program, or a full path), the seconds in to start, and corners. For its corners, run it and use **Set Swim Area**: in video mode,
the corners are saved in this line of `poolwind_defaults.txt`, and the
pool's own swim area in the calibration file is left as it is. If the file
isn't found, PoolWind says so and uses the camera.

Before swimming, delete these lines or set `'developerMode': False`.

**The calibration at a desk.** With the simulated valve, **Calibrate
pool...** and **Pace correction...** are greyed out in the menu. To try the
calibration screens without the pool:

```
python3 poolwind.py --calibrate --simulate --window
```

It uses a simulated jet, Pace Display and ping-pong balls, and saves only
to `poolwind_calibration_simulated.txt`, never to the real calibration
file.

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

**Another monitor.** The toggle is set up for the author's monitor (the
Eyoyo 10-inch on the parts list): portrait at 800×600, landscape at
1280×800, on the output called `HDMI-1`. Another monitor usually works
without changes: if `HDMI-1` has no monitor, the toggle uses whichever
monitor is connected, and if the monitor doesn't offer one of those sizes,
it uses the monitor's own preferred size. PoolWind adapts its screen to
whatever size it finds.

To choose the sizes yourself, open `~/.local/bin/toggle_monitor.sh` in a
text editor and change the three settings at its top. To see your
monitor's output name and the sizes it offers, type `xrandr` in a
terminal. Updating PoolWind keeps these settings.

## 10. Updating PoolWind

Download the new version and run the install script again:

```
cd PoolWind-download
git pull
bash install.sh
```

(In a new terminal, which starts in your home folder.)

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

## 12. Getting help

PoolWind has no support, but you're not on your own:

- **Discussions** on the PoolWind GitHub page, where builders share their
  builds, questions and answers.
- **An AI assistant** such as [Claude Code](https://claude.com/claude-code),
  run in the `PoolWind-download` folder (section 3). 
  
### Using Claude Code

Claude Code is Anthropic's AI assistant for working with programs. It runs
in a terminal on the Pi, where it can see PoolWind's files. It needs a paid
Claude account.
The author (mostly AI) has provided a detatiled description that will be sent to Claude automatically after subscribing.`CLAUDE.md` gives it PoolWind's background: how the program works, the  hardware, the safety rules and known problems. Claude Code reads it by
  itself, so there's nothing to copy or paste. It can read PoolWind's
  messages with you, explain settings, and help change the program for a
  pool or camera that differs from the author's, such as a pool whose
  speed voltage drops to zero while the pump is off. Test any change with
  nobody in the pool first.


**The easy way: the Claude icon** on the Pi's desktop, which the install
script adds. Double-click it:

- the first time, it explains Claude Code and offers to install it, then
  Claude Code asks you to sign in (or to create an account) through a
  link to open in a web browser;
- after that, it opens Claude Code in the `PoolWind-download` folder,
  carrying on your last conversation.

**By hand** (for example over SSH from a PC, below):

1. **Install it** (once). In a terminal on the Pi, type:
   ```
   curl -fsSL https://claude.ai/install.sh | bash
   ```
2. **Start it in the downloaded folder:**
   ```
   cd PoolWind-download
   claude
   ```
   The first time, it asks you to sign in: it shows a link to open in a
   web browser.
3. **Describe the problem in your own words.** Claude Code has already
   read `CLAUDE.md` as it started, so it knows PoolWind's background. For
   example: "the jet doesn't move when I press UP" or "my pool reads zero
   volts when it's off". It asks before reading files outside the folder (such as the
   installed `PoolWind` folder) or running anything.

**To check that it has the background**, type `/memory`: it lists the
`CLAUDE.md` files it has loaded, and `PoolWind-download/CLAUDE.md` should
be among them. If it isn't, Claude Code was started in another folder:
type `/exit`, then start it again with step 2.

To go back to your last conversation later, start it with `claude -c`
instead of `claude`. To finish, type `/exit`.

### The author's setup: Claude on a PC, the Pi at the pool

The author talks to Claude from a PC in the house, in its own window, while
the Pi stays at the pool. The PC needs nothing more than the Pi already
has: Claude runs on the Pi, and the PC only shows its terminal.

1. **SSH must be on** in the Pi (section 2). If you didn't turn it on
   there: Pi menu → **Preferences → Control Centre** (older versions:
   **Raspberry Pi Configuration**) → **Interfaces → SSH** on.
2. **On the PC, open a terminal window.** Windows: **Terminal** or
   **PowerShell** from the Start menu (SSH is built into Windows 10 and
   11). Mac: **Terminal**.
3. **Connect to the Pi**, with the username and hostname you chose in
   section 2:
   ```
   ssh yourname@poolwind.local
   ```
   The first time, answer **yes** to the question about the Pi's key, then
   type the Pi's password. The window is now a terminal on the Pi.
4. **Start Claude** in it, as above:
   ```
   cd PoolWind-download
   claude
   ```
5. **To see the Pi's screen** at the same time, use RealVNC Viewer
   (section 9) in another window, or on a second monitor.

**At the pool**, open a terminal on the Pi and type the same commands
(`cd PoolWind-download`, then `claude -c` to carry on the same
conversation). Finish with `/exit` on the PC first: two windows working on
the same conversation get in each other's way.

## 13. Trying PoolWind on a PC

You can try PoolWind on a Windows PC before building anything. It runs as
a **demo**: a recorded swim plays on the pool screen, and the jet is
simulated, so you can see how PoolWind follows a swimmer, how the zones
and the Pace work, and try Swim Plot. A PC can't control a pool: that
needs the Raspberry Pi build.

**You need:** Windows 10 or 11, an internet connection, and about 1 GB of
free space (most of it for Python and its libraries).

### Installing the demo

1. **Download the install script.** On PoolWind's GitHub page, click
   `install_windows.bat`, then the **Download raw file** button (a
   downward arrow at the top right of the file). Clicking the file name
   alone only shows its text.
2. **Your browser may warn** that the file "isn't commonly downloaded" or
   "could harm your device". In Edge: click **…** next to the download,
   then **Keep**, then **Show more → Keep anyway**. Chrome: **Keep**.
3. **Double-click** the downloaded `install_windows.bat` (in your
   **Downloads** folder).
4. **Windows will probably say "Windows protected your PC"** (a blue
   window). Click **More info**, then **Run anyway**.
5. The script installs, in a black window:
   - **Python**, if it isn't on the PC already, with Windows' own
     installer. Windows may ask you to allow it;
   - the libraries PoolWind uses (OpenCV, PySide6, NumPy, SciPy,
     matplotlib). This takes a few minutes the first time;
   - PoolWind itself and the sample video, in a `PoolWind` folder in your
     user folder;
   - a **PoolWind** icon on the desktop.

   Everything it does is written to `install.log` in that folder. When it
   says **Done**, press a key to close it.
6. **Double-click PoolWind** on the desktop. **DEMO** shows on the pool
   screen.

**Why the warnings?** Windows and the browsers warn about any program or
script from the internet that isn't signed by a known publisher, and
PoolWind is a hobby project without one. The script is plain text: to see
what it does before running it, right-click it and choose **Edit** (or
**Open with → Notepad**). Run it again at any time to update PoolWind:
your settings are kept.

### Removing it

Delete the `PoolWind` folder in your user folder and the PoolWind icon on
the desktop. If the script installed Python and you don't need it, remove
**Python 3.13** in **Settings → Apps**.
