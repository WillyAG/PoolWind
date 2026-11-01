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
- downloads the **sample video**, a recorded swim for the demo;
- adds three icons to the desktop: **PoolWind**, **Monitor Toggle** for
  [working from home](#9-working-from-home), and **Claude**
  ([getting help](#12-getting-help));
- turns the monitor to **portrait** (taller than wide) every time the Pi
  starts, ready for swimming.

It writes everything it does to a log file, `install.log`, in the
`PoolWind` folder. If something goes wrong, that's the place to look.

It never overwrites settings or calibration files you already have, so it's
safe to run again. When it updates the program, it keeps the previous one
as `poolwind.py.previous`.

When it finishes, **restart the Pi.**

When the screen comes back, there will be a "PoolWind" icon. When you double-click it, PoolWind comes up in demo mode
([the demo tour](USER_MANUAL.md#9-the-demo-tour) explains what it shows).

## 4. First start

**Turn the demo off first.** PoolWind is installed as a demo: a recorded
swim and a simulated jet, so nothing at the pool moves. To control the
pool, open `poolwind_defaults.txt` in the `PoolWind` folder (double-click
it), change `'Demo': True` to `'Demo': False`, and save it.

Suggested before starting:

- Nobody in the pool
- The pool switched off at first; you'll turn it on for the jet check
- the pool's own remote at hand
- **The monitor is in portrait mode** (taller than wide). The install script
  sets this up, so it happens by itself a few seconds after the desktop
  appears. If it doesn't, double-click **Monitor Toggle**. 

Double-click the **PoolWind** icon. The pool screen appears, showing the
camera's view from above.

Check that:

- the display shows most of the pool from above (will set the correct view later)
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

1. **Set Swim Area** (5.2): where the pool is in the camera's picture.
2. **Calibrate pool** (5.3-5.5): your pool's voltages, the jet's limits and
   the pool's Pace table (the **Master** table).
3. Each swimmer's **Swimmer limits**: see the
   [user manual](USER_MANUAL.md#swimmer-limits-your-slowest-and-fastest-zone).

> **The calibration file is safety-critical.** It decides which voltages
> PoolWind drives the jet to. Only someone who understands the system should
> change it. 



### 5.1 **Pool, Master, and Swimmer datasets and the USB stick**
This is a good time to talk about what these terms mean.

1. 'Pool' and 'Master' data are exactly the same thing and the term 'Master'
   will be used from now on. This data is stored in the `poolwind_calibration.txt`
   file on the SD card.
   - Master datasets consist of the pool Pace-volt calibration, other pool parameters, pool swim data, and pool swim videos.
   - Only the builder can create or edit this data as it defines your pool parameters.
   - The builder will need the Raspberry Pi password entered during the
     initial installation.

2. Swimmer datasets consist of their own Pace-volt calibration, swim data,
   and swim videos.

3. USB stick: PoolWind knows whether or not a swimmer's USB stick is plugged in.
   - If not plugged in, the builder is allowed to create or edit the 'Master'
     dataset. See (1.) above.\
     **Pace correction** will edit the Master dataset, not the Swimmer dataset.
     The builder is also the 'swimmer' and their swim data will be stored in the Master dataset on the SD card. Any other swimmer without a USB stick, will simply add to the builder's swim data but they cannot edit the Master dataset without knowing the password.
     The builder should not plug in a USB stick unless they want to be just a
     normal swimmer and keep their own data.  
   - If plugged in, while the Master dataset still controls the pool, the 
     Pace-volt data and Swimmer dataset from the USB stick takes precedence over the corresponding subset of the Master data on the SD card.\
     **Pace correction** in this case, will edit the Swimmer dataset, not the Master dataset. This gives swimmers the
     ability to keep their individual Pace-volt settings, swim data, and swim videos. They access them by simply plugging in the USB stick.

### 5.2 Set swim area

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
length changed, change the usable swim length too (5.9). In the dark, when
there isn't enough to compare, the check says nothing.

### 5.3 Calibrate pool - Begin initial voltage scan - Master dataset
On the pool screen, open the menu (**≡**, top left) and choose **Calibrate pool...**.

This is an automatic scanning operation that must be run before any other calibration.
This scan runs the jet from its slowest to its fastest speed, creating and building the Pace-volt table by filling in the measured voltages found. 


**In this PoolWind version, code only supports a pool with a feedback voltage range in discrete steps
(like the author's). A continuous voltage range will need programming changes. The link to 'Claude', made as an icon on the screen, will send a note describing PoolWind and the method needed to make a 'continuous' voltage range if necessary. This routine checks for stepped vs continuous and will give a warning message if the voltage range is not stepped before quitting. It is up to the builder to implement this.**



At this point Pace is not yet filled in.
Basically, the program operates with only the voltages, jet speed is determined by voltage and the swimmer position determines the voltages. 

**It is most important that the builder presses "Stop", then "Use as top", when they feel the jet speed is high enough and going further puts unnecessary strain and wear on the pool. PoolWind respects this decision and will never run the jet higher.**

The Pace-volt table's first and last rows become the jet's limits. This procedure combined with **Swimmer limits** and programming establish the "feel" of the pool, how fast the swimmer swims in the highest zone, how slow in the lowest zone, and how it "feels" to transition through the zones. Pace settings have nothing to do with the "feel".

1. Press **Begin initial voltage scan**, then **Start**. The calibration
   reads the voltage for a few seconds, takes the jet down to its slowest
   speed, then steps it up, counting the steps.
2. **Watch and listen to the pool.** When it sounds too fast or strained,
   or the Pace Display stops changing, press **Stop**, then **Use as
   top**.
3. The jet is taken back down, and the results show your pool's range,
   its number of steps and the Pace table: **one row for each jet
   step**. These rows are PoolWind's **zones**.
4. Press **Save scan** (it asks "Write scan to Master calibration file?"). Here is where Pace values are written into the table. The shape of the author's Pace-volt table, built into PoolWind, is stretched to the low and high range and its values are entered into the newly created Pace-volt table. This gives reasonable Pace values that can be used in a swim.
The table is written into the calibration defaults file: `poolwind_calibration.txt`
If re-initializing, the old Pace-volt table is kept in `temp/poolwind_calibration_before_<date>.txt`.  The scan data is also kept as `temp/calibration_scan_<date>.csv`.

**The scan's Paces are a first estimate.** The scan measures only your
pool's voltages, not its speeds, so the associated Paces it writes are estimated:
**7:00** at your pool's slowest step, **1:00** at its top (where you
pressed Stop, or the jet's fastest speed), and in between an inverse-speed curve. That's realistic enough for PoolWind to run and to start swimming with. **Pace Entry** and **PingPong** replace the estimates with
Paces measured on your pool, and **Pace correction** in PoolWind's menu
adjusts them to what feels right from your own swimming experience.

To scan again later if necessary, press **Begin initial
voltage scan** again. It says the scan has already been run and asks
**Replace** or **Cancel**. The scan starts over: any changes made to the Pace table are replaced by the first estimate above.

### 5.4 Calibrate pool - Pace entry - Master dataset
This routine is used if the pool has a Pace display. It's recommended to use this over PingPong. It's the best the manufacturer can give you for your pool. Afterwards, you can always edit the Pace values with **Pace correction**. Do not insert a USB stick since you are still setting up and building the Master dataset.

On the pool screen, open the menu (**≡**, top left) and choose **Calibrate pool...**.

**Pace here is only an estimate.** It can never be exact due to the
varying speed of layers as you go from top to bottom. It is different for
stroke styles and body types depending on how deep you go (your legs
mostly). But after calibration, it is close and consistent enough for
training. You can only measure an accurate Pace in a regular pool.

**Before you start**

- **Nobody in the pool.** The jet goes up to fast speeds.
- The pool's **pump on**, and the swim area set (5.2).

**Edit screen** This routine opens the edit screen first where it displays the current Pace-volt table. **If you have not done a 'Pace entry Auto scan' before, skip edits and press the 'Auto scan' button (see below).**
You can select a row on the table and the jet speed will step to the row selected. It will pause a moment to let the pool settle and then allow you to re-enter the Pace showing on the Pace display. Enter the correct three digits - entering the third digit completes the edit.
Rows showing **-----** are jet steps the initial scan found above the table's top (the table was ended lower with **Entry complete**, below). They are not part of the table, but you can select one and enter its Pace: it then joins the table and raises the jet's top to it.
- **Error checking**:
  - If the entry made is not correct, it is likely that some rows will turn red. You can click back to that row and re-enter or hit the **↺** button next to the entry box to get the original setting back.
  - If the entry is correct but rows around it are displayed red, that means the proper sequence of Pace values has been broken. Click to the closest red value and re-enter the Pace reading now showing. 
  - If all entries are correct but there are still errors showing, go to each red entry and type a value close to the original but one that will also fit the sequence. Repeat until there are no red warnings. Remember Pace is not accurate no matter how well the entries went.

**Auto scan** clears the table's Paces, takes the jet down to
  its slowest speed, then steps it up one step at a time to the top the
  initial scan found (the **-----** rows too) while you type the Pace at each. There will be a pause at the start and between entries for the jet to settle. A Pace that can't be right or mis-entered turns red and the scan goes on: there's no time for corrections. 
  
  Once the top speed has been reached, the jet steps back down, stopping at each red step to
  ask again for the Pace display entry. **Back** stops the scan: displaying two buttons: **Back** (again) goes back and carries on and **Continue** keeps what you typed, takes the jet down and the Edit screen comes back. This occurs in about 30 steps, 10-20 minutes. If you did not finish the scan, the table will be interpolated for the final end points.
  If there are warnings, edit the entries as explained above.

  **Entry complete** (after two steps are typed): when you have entered enough steps, or the pool shouldn't go any faster. The last step you typed becomes the top of the table, the jet's fastest speed. The steps above it show **-----** and are left out of the table, but kept: the next Pace Entry or PingPong shows them again. The jet goes down and the Finish screen comes up; nothing is saved until **Save Table**.

- **Finish** (from the Edit screen): shows the new table beside the current one,
  and how far apart they are in %. Steps without a Pace get a calculated
  Pace, marked `~`: interpolated between the steps typed, and extended on
  to 1:00 at the fastest step and 7:00 at the slowest. A step that isn't faster than the step below is marked red.
  While the jet is still going down, **Save Table** and **Quit** are greyed out ("Taking the jet down...").

  **Save Table** replaces the Master table (it asks first, and warns if a step is still red) and  goes back to PoolWind. **Edit table** goes back to the Edit screen.

  **Quit** leaves without saving, after "Are you sure?".


### 5.5 Calibrate pool - PingPong - Master dataset

You would mainly use this if you are unhappy with the rough initial Pace values and do not have the Pace display. Afterwards you can always edit the Pace values with **Pace correction**. Do not insert a USB stick since you are still setting up and building the Master dataset.

On the pool screen, open the menu (**≡**, top left) and choose **Calibrate pool...**.
This section and the previous one (5.4) deal with entering Pace. 

**Pace here is only an estimate.** It can never be exact due to the
varying speed of layers as you go from top to bottom. It is different for
stroke styles and body types depending on how deep you go (your legs
mostly). But after calibration, it is close and consistent enough for
training. You can only measure an accurate Pace in a regular pool.

**Before you start**

- **Nobody in the pool.** The jet goes up to fast speeds.
- The pool's **pump on**, and the swim area set (5.2).

You need five **orange** ping-pong balls (bright or fluorescent; white ones don't work). 

There is a starting line and a finish line drawn on the pool live video. 
When prompted, set one ball gently on the water right at the jet, in the middle. The measurement will begin when the ball crosses the starting line and end when the ball reaches the finish line. The distance is known from the pool calibration default of 'usableSwimLength'. When 3 drops agree, it moves on to the next set while you are collecting the balls.

If you think enough balls had been dropped (in one set), you can press 'Use dropped'. 
If you think the measurement was bad, you can press 'Clear dropped'.

The ball rides on the surface which is the fastest level that the jet pushes. Lower levels move slower and the bottom is practically still. A swimmer typically occupies the top 10 inches, not counting hands and legs, and so would move slower than the pingpong balls.
So the ball's pace is turned into a swimming Pace with two numbers: **bodyDrag**, the factor at the jet's fastest speed (1.50), and **deltaBodyDrag**, how much more it is at the
slowest (0.18). Between the two Pace changes evenly, step by step. These are defaults that work in the author's pool, an educated guess. The results screen shows both: change them and the table follows. They're kept in the calibration file with the ball measurements, so they can be changed again later in Pace correction.

During measurements:
- **Stop** If the builder thinks the pool is going too fast or that there have been enough entries made. Values already measured will keep and the remainder of the curve will be interpolated.

When stopped either manually or at the jet's top (the top the initial scan found; PingPong also goes on into the **-----** steps above the table's top, see 5.4):
- **Resume** goes back to scan
- **Quit** without saving keeps the current table.
- **Finish** takes the jet down to its slowest speed and shows the results.

PingPong ends with a results table, new against current. Steps above your last ball set that are in the table show `...` and are filled in when saved; the **-----** steps above the table's top are left out unless you measured them. A step that isn't faster than the step below is marked red.
- **Save table** writes it (with a backup); 
- **Quit** without saving keeps the current table.


### 5.6 Compare Calibrate pool options - Master dataset

Briefly:
1. The initial voltage scan (5.3) produces an accurate voltage scan but rough Pace values in the table. The swimmer can swim with the 'feel' of PoolWind but all calculations depending on Pace like distance and average Pace will probably be off. You can keep these values or, if not satisfied, use (2.) or (3.) below.

2. Pace entry (5.4) will use the manufacturer's best guess of Pace as displayed on the Pace display. The Pace entries of the initial voltage scan will be replaced by hand entered values of what is displayed. This will be the better choice over PingPong if you own the Pace display.

3. Use PingPong if you have no Pace Display. PingPong (5.5) will accurately measure the surface speed of each of your pool's 'zones' using the pingpong balls. But the actual Pace needs a drag factor and change of drag factor to multiply the pingpong measurements. Those factors are just guessed at. The routine gives a dynamic plot of how these factors affect Pace as well as being able to edit points. So with a little experience you may arrive at a pretty good table. 


### 5.7 **Pace correction** - Master dataset(no USB stick) or Swimmer dataset(with USB stick) 

'Pace correction' offers a dynamic way to edit the Pace values that you feel are off and replace them with values based on your swimming experience. Even a single entry, say based on your fastest measured time in a real pool, will help and the surrounding Pace values will be interpolated. More entries, say based on other styles, will improve the Pace values even better yet.

1. If the builder thinks they can improve the calibration Pace values for the Master dataset, they would not plug in a USB stick while using Pace correction. Changes go to the Master dataset.

2. If a swimmer thinks they can improve the values of the Master dataset for themselves personally, they would have their USB stick plugged in. Changes go to the Swimmer dataset on the USB stick. While swimming, Swimmer dataset values override the Master dataset values.

**Earlier swims change too.** 
A change in the Pace-volt table will change the Pace values when the swim is viewed in the **Swim Plot...** routine.\
See [Your earlier swims change too](USER_MANUAL.md#pace-correction-when-the-paces-dont-feel-right) in the user manual's Pace correction section

See the [user manual](USER_MANUAL.md#pace-correction-when-the-paces-dont-feel-right) for more details on this routine.


### 5.8 The jet's limits

There is no separate limits setting: the **Pace table's first and last
rows** are the jet's limits.

- The **first** row's voltage is the jet's lowest. PoolWind winds the jet
  down to it when **OnOff** is pressed, before it switches the pump.
- The **last** row's voltage is the highest PoolWind ever drives the jet
  to, whatever any swimmer's setting says.

The scan ends the table where you stopped it (**Use as top**), or at the
jet's top speed. Pace Entry and PingPong never step the jet above it. The
limits always come from the pool's table, never from a swimmer's.

Before PoolWind v15.6 the limits were a `'SafetyVoltageLimits'` line in the
calibration file. An old line is ignored now, and the next scan takes it
out.

Changes to the calibration file take effect at the next start.

### 5.9 Usable swim length and swim zone width

Set both on the first screen of **Calibrate pool** (menu **≡**, top left),
under **Pool settings**, then press **Save**. There's no need to open the
calibration file.

- **Usable swim length** (inches): from the surface of the jet to the rear
  of the pool, **not** the pool's length. It should match the swim area you
  set in [5.2](#52-set-swim-area). On the author's Standard Endless Pool,
  the pool is 180" long and the jet's surface is 18" from the front, so
  it's 162. PoolWind uses it to turn the camera picture into distances.
- **Swim zone width** (%): the width of the swim zone, as a percentage of
  the swim area's width. 35 % leaves enough room for the swimmer to swim in
  and still get out of it to step to the bench.

PoolWind uses the new values as soon as the calibration window closes.

## 6. The settings files

PoolWind keeps its settings in plain text files next to the program, all
starting with the program's name:

| File | Holds | Who changes it |
|---|---|---|
| `poolwind_defaults.txt` | The swimmer settings for anyone without a USB stick | The owner |
| `poolwind_calibration.txt` | The Master Pace table (the zones; its first and last rows are the jet's limits), swim area, swim length, center lane, the scan's results (`InitialCalFinished`, `jetVoltageRange`, `jetStepVolts`: every jet step the scan found, so Pace Entry and PingPong can show steps above the table's top again, `PacesFromFormula`: the Paces are still the scan's estimate), PingPong's numbers (`bodyDrag`, `deltaBodyDrag`, `PingPongBalls`), Pace correction's pending changes for swimmers without a stick (`PacesPending`), and the update's `logsTable` / `rulerAdded` (section 10) | The calibration, Pace correction and the technician |
| `poolwind_calibration_camera.png` | The camera picture the swim area was set on (the camera check, 5.2) | PoolWind, when the swim area is saved |
| `poolwind_ind_defaults.txt` (on each USB stick) | One swimmer's own settings | That swimmer |
| `poolwind_ind_calibration.txt` (on each USB stick) | One swimmer's own Pace table, their Pace correction's pending changes and drag numbers. Made from the pool's table the first time the stick is used | Pace correction |
| `temp` folder (next to the program, and on each USB stick) | Files PoolWind never needs to run: the backups made before a table is replaced (`..._before_<date>.txt`), the calibration's records (`calibration_scan_`, `calibration_session_`, `calibration_drops_`, `calibration_correction_<date>.csv`) and developer traces. Delete it any time; PoolWind makes it again when needed | PoolWind |

The swimmer settings use **the same names** in the defaults file and on
the USB sticks. A stick's value wins while it's inserted. See the
[user manual](USER_MANUAL.md#8-your-settings) for the list.

**The defaults file as shipped** uses a moderate range of zones, `(6, 12)`
(about 4:34 to 3:07 per 100 yards on the shipped Pace table), and an
average height. If you raise the fastest zone for yourself, remember it
applies to anyone who swims without their own stick.

**Zones on the sticks.** A swimmer's stick holds their slowest and fastest
**zone** (`'zoneMin, Max'`), set with Swimmer limits. The defaults file uses
zones too. An older pace range (`'paceMin, Max'`) still works: PoolWind
turns it into zones through the Pace table. Zone numbers belong to
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

**Ejecting the stick at close.** When PoolWind closes, it always writes
everything to the swimmer's USB stick and unmounts it, so it's safe to
remove. There's no message, except when something else was using the
stick and it couldn't be ejected. The stick isn't powered off, so if it
stays in, the next start mounts it again. To see its files in the File
Manager after PoolWind closes, unplug it and plug it back in. (The
`'ejectStickOnClose'` setting is gone since v15.7; a line left in a file
is ignored.)

The files are written like this:

```
{
'swimmersHeight': 66

,'zoneMin, Max': (6, 12)
}
```

- Keep the curly brackets around everything.
- Every setting after the first starts with a comma.
- Text goes in quotes. `True` and `False` have capital letters.
- Lines starting with `#` are comments, ignored by PoolWind.

If the defaults or calibration file can't be read when PoolWind starts, it
says why in the terminal and doesn't start. If you make a mistake while it's
running, it says so and keeps the last good settings.

PoolWind only ever changes single lines in the defaults file (Swimmer
limits without a stick, Set Swim Area in video mode), so your comments
stay.

## 7. Built-in settings

These were tuned during development and are built into the program. To
change one, add its line to `poolwind_defaults.txt`, with exactly the same
name. The file's value then replaces the built-in one. Delete the line to
go back.

Most take effect while PoolWind is running. Those marked **restart** need
PoolWind to be closed and started again.

| Setting | Built-in value | What it does |
|---|---|---|
| `'Demo'` | `True` | Runs the program in demo mode. Does not need further hardware including pool. Most routines are functional.|
| `'Sensitivity'` | `5000` | Minimum size, in pixels, of something the camera counts as a swimmer |
| `'CoM filter Alpha'` | `0.05` | Smoothing of the swimmer's position. Smaller is smoother but slower to react |
| `'inactivity wind down time (sec)'` | `3` | How long the swimmer may be out of the lane before the jet winds down (**restart**) |
| `'stillSeconds'` | `15` | Seconds without movement before a swimmer in the lane counts as gone (someone standing or floating) |
| `'stillMotion'` | `0.25` | How much of the swimmer's shape must change to count as movement for `'stillSeconds'` |
| `'autoSuspendMinutes'` | `3` | Minutes after that before PoolWind suspends the swim by itself. `0` never does |
| `'DRIFT_SCALE'`, `'DRIFT_TAU'`, `'DRIFT_MAX'` | `1.67`, `5.0`, `25.0` | The Swimmer Pace estimate. Leave these alone unless you're developing |
| `'WATER_TAU'` | `5.0` | Seconds the water takes to catch up after the jet changes speed, for the Swimmer Pace estimate. (The [zone highlight](USER_MANUAL.md#seeing-the-jets-zone-the-zone-highlight) follows the jet directly.) |
| `'zoneHighlight'` | `False` | Whether the zone highlight is on when PoolWind starts. A tap on the picture turns it on or off either way |
| `'zoneHighlightLevel'` | `0.2` | How bright the zone highlight is: `0.05` is barely seen, `0.3` is strong |
| `'developerMode'` | `False` | Developer tools: see [Testing at a desk](#8-testing-at-a-desk). Also shows the position bar and the `dIdx`, `V` (jet voltage) and `CoM` readouts on the pool screen, shows the position bar on the Swim Plot video while the zone highlight is on, allows raw video, and opens **Calibrate pool...** with a USB stick in, without the builder's password and whatever the workplace, valve or camera setting (Pace correction too; with the simulated valve the calibration uses the pool's relays, sensor and camera itself). Users leave it off: the position bar also moves with swim angle and depth, not just the stroke, which would confuse a swimmer |
| `'readouts'` | `True` | Developer: with `developerMode` on, `False` hides the `dIdx`, `V` and `CoM` numbers on the pool screen (for example for a screenshot) |
| `'comBar'` | `True` | Developer: with `developerMode` on, `False` hides the position bar (pool screen and Swim Plot) but keeps the readouts. The zone highlight is the steadier reference |
| `'algorithm (basic or swimmerPace)'` | `'swimmerPace'` | Developer: the control method. `'swimmerPace'` is the method the manuals describe; leave it. `'basic'` is a simple baseline for building new control methods on. Main defaults file only: a USB stick's line is ignored |
| `'paceTrace'` | `False` | Developer: writes a detailed `temp/pace_trace_*.csv` file of the pace estimate, about 15 MB an hour |
| `'recordRawVideo'` | `False` | Developer: with `developerMode` on, records the camera's full, uncorrected video, a tool for developing the swimmer detection. The files are large (**restart**) |
| `'Runtime: hotReloadParameters'` | `True` | Picks up settings changes while running |

The swimmer settings also have built-in fallbacks, used only if the
defaults file leaves them out: every zone of the Pace table
(`'zoneMin, Max': None`) and `'logRate': 5`.

**The swim log** (`CSV Vault/<date>.csv`, one line per record, no header):
time, pace, distance, video segment, frame, position (`CoM_h`), swimmer
tick (`CoM_w`, `-1` = none), and since the zone highlight, the jet's zone
(`-1` = none) and the number of zones. Older files without those columns
replay without the highlight. Since v15.7 two more: the jet's voltage and
the Pace the table in use gave there, so Swim Plot can show any swim in
today's table (user manual, Swim Plot). Logs from before
v15.7 show as they were swum.

## 8. Testing at a desk

These developer settings let you run PoolWind without the pool. They only
work with `'developerMode': True` and `'Demo': False` in
`poolwind_defaults.txt`: a demo always plays the sample video with a
simulated jet, and with `developerMode` off PoolWind always runs the real
pool setup, whatever the file says. Add them to `poolwind_defaults.txt`;
they all need a **restart**.

| Setting | Normal | Meaning |
|---|---|---|
| `'Valve (real or simulate)'` | `'real'` | `'simulate'` runs without pressing the remote's buttons |
| `'capture_device (camera or video)'` | `'camera'` | `'video'` plays a recorded swim instead of the live camera |
| `'display_device (work or pool)'` | `'pool'` | `'work'` switches the monitor to landscape for programming, and `'pool'` back to portrait (monitor mode set in the program code) |
| `'workplace (home or pool or default)'` | `'pool'` | Sets all three above at once: `'home'` = video, work, simulate; `'pool'` = camera, pool, real; `'default'` = use the three lines as written |
| `'video file, start (sec), corners'` | `'PoolWind_demo.mp4'`, `0`, the sample's corners | The recorded swim `'video'` (and the demo) plays: its file, the number of seconds in to start, and the swim area's four corners in that video |

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
,'video file, start (sec), corners': ('PoolWind_demo.mp4', 0, [(153, 148), (479, 151), (384, 601), (184, 583)])
```

The pump relay is only connected when the workplace is `'pool'`. So
`'default'` with `'Valve (real or simulate)': 'real'` tests the speed
relays at a desk with no chance of starting the pool's pump.

The last line is the built-in value, for the sample video. To use your own
recording, add the line to `poolwind_defaults.txt` with its file name
(next to the program, or a full path), the seconds in to start, and corners. For its corners, run it and use **Set Swim Area**: in video mode,
the corners are saved in this line of `poolwind_defaults.txt`, and the
pool's own swim area in the calibration file is left as it is. If the file
isn't found, PoolWind says so and uses the camera.

Before swimming, delete these lines or set `'developerMode': False`.

With `'work'`, PoolWind's window keeps its title bar. While Swim Plot is
open it says **Using Swimmer dataset** or **Using Master dataset**, and its
**×** closes Swim Plot, not PoolWind.

**The calibration** has no simulation: it always drives the real jet. With
the simulated valve, **Calibrate pool...** uses the pool's relays, voltage
sensor and camera itself (with `'developerMode': True`, which these settings
need, it and **Pace correction...** stay in the menu). The pump doesn't need to run: with it off, the
jet's valve still moves to each voltage, so the calibration screens can be
tried at the Pi without swimming.

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

(In a new terminal, which starts in your home folder.) If you no longer
have the `PoolWind-download` folder, follow section 3 again: it's the same
script.

The same script installs and updates. On an update it replaces the program
(keeping the old one as `poolwind.py.previous`) and leaves everything else
as it is: your settings, your pool's calibration, swim logs, videos and USB
sticks. When it finishes it says which version it updated from and to, and
what's new.

The new version reads the older files as they are. Updating from v15.5 to
v15.7, for example:

- the calibration's old `'SafetyVoltageLimits'` line is ignored (the jet's
  limits are the Pace table's ends, 5.8);
- the first start keeps the pool's Pace table as `'logsTable'` in the
  calibration file: the table the old swims were swum with;
- each swim log folder (`CSV Vault`, the Pi's and each USB stick's, when
  the stick is first used) has its old logs given the jet's voltage and
  Pace once, so Swim Plot can show them in today's Paces; it's marked
  `'rulerAdded'`, and takes a few seconds;
- each swimmer's own Pace table is made on their stick the first time it's
  used.

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

- **[Discussions](https://github.com/WillyAG/PoolWind/discussions)** on the
  PoolWind GitHub page, where builders share their builds, questions and
  answers. Anyone can read them; to post, sign up for a free GitHub account.
- **An AI assistant** such as [Claude Code](https://claude.com/claude-code),
  run in the `PoolWind-download` folder (section 3). 
  
### Using Claude Code

Claude Code is Anthropic's AI assistant for working with programs. It runs
in a terminal on the Pi, where it can see PoolWind's files. It needs a paid
Claude account.

The download includes `CLAUDE.md`, a detailed description of PoolWind
written for Claude: how the program works, the hardware, the safety rules
and known problems. Claude Code reads it by itself whenever it starts in
the `PoolWind-download` folder, so there's nothing to copy or paste. It can
read PoolWind's messages with you, explain settings, and help change the
program for a pool or camera that differs from the author's, such as a
pool whose speed voltage drops to zero while the pump is off. Test any
change with nobody in the pool first.


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

Either way, once you're signed in:

**Describe the problem in your own words.** Claude Code has already
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

1. **Click [Download the PoolWind demo](https://github.com/WillyAG/PoolWind/releases/latest/download/install_windows.bat).**
   This downloads the install script, `install_windows.bat`.
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
     user folder. The video is a hidden file. When you close PoolWind,
     the whole `PoolWind` folder is deleted.

   Everything it does is written to `install.log` in that folder.
6. **When it says Done,** [the demo tour](USER_MANUAL.md#9-the-demo-tour)
   opens in your browser and PoolWind starts, with **DEMO** on the pool
   screen. The tour opens in a new tab: the page you came from is still
   in the tab next to it. Give PoolWind the left third of the screen and
   the tour the rest: click PoolWind, press the Windows key and the left
   arrow, click the browser on the right, then drag the line between them
   to the left. The demo starts swimming by itself, with the zones
   showing; follow the tour.

### Watching it again

Click [Download the PoolWind demo](https://github.com/WillyAG/PoolWind/releases/latest/download/install_windows.bat) again and run it. The script
deletes itself from **Downloads** when it finishes, so copies don't pile
up there. Python and the libraries are already there, so it only
downloads the sample video again, then the tour opens and the demo
starts. It also
brings you the latest PoolWind.

**Why the warnings?** Windows and the browsers warn about any program or
script from the internet that isn't signed by a known publisher, and
PoolWind is a hobby project without one. The script is plain text: to see
what it does before running it, right-click it and choose **Edit** (or
**Open with → Notepad**).

### Removing it

Closing PoolWind already deletes its `PoolWind` folder (if PoolWind was
stopped some other way, delete that folder in your user folder yourself).
If the script installed Python and you don't need it, remove
**Python 3.13** in **Settings → Apps**.
