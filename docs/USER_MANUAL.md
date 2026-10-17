# PoolWind User Manual

This manual is for swimmers. Building PoolWind and setting it up for your
pool are covered in the build guide and the setup and calibration guide.

**Please read [SAFETY.md](../SAFETY.md) first.**

## Contents

1. [Before you swim](#1-before-you-swim)
2. [Starting PoolWind](#2-starting-poolwind)
3. [The pool screen](#3-the-pool-screen)
4. [Swimming with PoolWind](#4-swimming-with-poolwind)
5. [Finishing a swim](#5-finishing-a-swim)
6. [Your USB stick](#6-your-usb-stick)
7. [Reviewing your swims: Swim Plot](#7-reviewing-your-swims-swim-plot)
8. [Your settings](#8-your-settings)

---

## 1. Before you swim

- **Use your own USB stick.** It holds your personal Pace limits, so the jet
  never goes faster than you've chosen. Never use someone else's stick,
  especially a stronger swimmer's.
- **Insert your stick before starting PoolWind.** A stick inserted while
  PoolWind is running isn't used until the next start.
- **Know how to take manual control:** close PoolWind (see
  [Finishing a swim](#5-finishing-a-swim)). PoolWind fights against any change
  the pool's own remote makes.

## 2. Starting PoolWind

1. Insert your USB stick.
2. Start PoolWind with its **desktop icon**. 
3. **"Starting Up: Please wait for voltage wind down"**: PoolWind first brings
   the jet down to its lowest setting. Wait for this message to close.
4. The pool screen appears. Press **Begin** (or **Resume**, see below) when
   you're ready to swim. Until then, the jet stays at its lowest setting.

**Begin or Resume?** If you've already swum today, the big button says
**Resume** (in red) instead of Begin. Your swim continues where it left off:
today's distance and average Pace carry on from your earlier session.

**A blank or new USB stick?** PoolWind offers to set it up as a new
swimmer's stick (see [Setting up a new stick](#setting-up-a-new-stick)).

## 3. The pool screen

The screen shows the camera's view of the pool swimming area from above, with your
numbers on top in large letters you can read from anywhere in the pool.

**Your numbers:**

| On screen | Meaning |
|---|---|
| Large Pace at the top (e.g. `2:15`) | Your **Swimmer Pace**: your estimated Pace through the water, in minutes per 100 yards |
| `2:31 avg` | Your average Pace so far today |
| `0.512 mi` | Distance swum today, in miles |

**Buttons:**

Most buttons are labeled with what they'll do when you press them. Two of
them also change color to warn you that PoolWind isn't running normally:
**Hold** turns yellow and **Suspend** turns red.

| Button | What it does |
|---|---|
| **Begin** (large, center) | Starts the day's first swim. Then it says **Suspend** |
| **Suspend** | Pauses your swim. Then it turns red and says **Resume**. See [Pausing](#pausing-suspend-and-resume) |
| **Resume** (red) | Continues your swim |
| **Hold** | Keeps the jet constant, wherever you are in the pool. The button turns yellow and says **Vary**. See [Hold](#hold-a-steady-jet) |
| **Vary** (yellow) | Shown while Hold is on. Use **UP** and **DN** to vary the held speed, and press **Vary** to go back to automatic control |
| **View** | Switches between the camera view and three detection views (see below) |
| **UP / DN** | In Hold mode, raise or lower the held speed, one jet step per press |
| **OnOff** | Turns the pool's pump on or off |
| **≡** (top left) | Menu: **Set Swim Area...** and **Swim Plot...** |
| **X** (top right) | Closes PoolWind |

A button looks pressed in while you touch it.

**The View button** cycles through four views. The first is the normal
camera view. The other three show what the camera's swimmer detection
sees, in black and white. They help when checking that PoolWind is
detecting you properly. Press View until the camera view returns.

**Tap the picture** (anywhere off the buttons) to light up the zone that
matches the jet's speed; tap again to turn it off. See
[Seeing the jet's zone](#seeing-the-jets-zone-the-zone-highlight).

## 4. Swimming with PoolWind

### How the jet follows you
PoolWind divides the pool into **zones** from back to front. Each zone has
its own jet speed, slowest at the back and fastest at the front.

- **Speed up**, and you move forward into a faster zone. The jet speeds up
  until it balances your faster stroke.
- **Ease off**, and the jet pushes you back into a slower zone, where it
  relaxes again to balance your slower stroke.
- **Swim steadily**, and you settle in one zone with a steady jet flow.

The fastest zone is set by the top Pace on your USB stick, so the jet never
goes faster than that.

You can change strokes, speed up, and slow down to rest without running into
the front or the back of the pool. But a **sprint** will put you into the wall.
Delays in jet response and changing the momentum of the large volume of water 
take a few seconds. Give the system a little time to work.

### Seeing the jet's zone: the zone highlight

**Tap the picture** (anywhere off the buttons) to light up the zone that
matches the jet's speed right now, as a faint band across the screen. Tap
again to turn it off. It is turned off when PoolWind starts.

- The band is the **jet's** zone, not yours: It is not a physical zone but it represents the rate the water is moving.  You can think of the band as the readout of a jet speed meter, slowest at the bottom of the screen (the back of the pool), fastest at the top.
  For how the zones work, see
  [PoolWind in brief](../README.md#poolwind-in-brief) in README.
- It stays put while the jet holds a speed, so it's a **stationary
  reference**: you can see a stronger or easier stroke carry you forward or
  let you drift back against it.
- It moves a few seconds after you do, once the water has caught up. That
  same delay is why a sprint can run you into the wall: you can watch it
  happen.
- Don't blame the program for the slow movement of the band, it only reflects built in pool delays of setting the jet speed (moving the valve) and moving the mass of the water. Nothing can speed that up.

The same tap works on the video in [Swim Plot](#7-reviewing-your-swims-swim-plot).

### swimArea definition
**swimArea** is the swimming area of the pool that does not include the water return benches. Its four corners are marked using the menu item: (**≡**, top left)  **Set Swim Area...** (see [The swim area](SETUP_GUIDE.md#51-the-swim-area) in the setup guide). Everything else the camera might pick up is cut out of the swimArea and discarded. The swimArea is what you see on the monitor.

### swimZone definition
**swimZone** is a subset of the swimArea and is a lateral zone down the middle of the pool that has a width of 35% (as shipped) of the swimArea. It's a "zone" because PoolWind only responds to swims occurring in the swimZone.

### dataTracking definition
**dataTracking** refers to a set of operations that consists of:
- compute and display distance swum
- compute and display average Pace
- record video taken of the swimArea including the swimmer
- record swim data synchronized with the video including Pace, averagePace, and distance
This set can be turned on or off as a whole. When "on", the latest data is displayed and sent to the USB stick (or on the SD if there is no stick). When "off", computation and recording stop, leaving latest values frozen on the monitor (Pace, however, still updates). When "on" again, data is appended, not destroyed.

### Swim down the middle in the swimZone
PoolWind turns on dataTracking only if you are in the swimZone but allows you to deviate in and out with no problem.

- if you leave the swimZone and stand next to it, dataTracking is suspended and the jet winds down to its lowest setting after a few (3) seconds
- if you leave the pool and the camera can't see you, dataTracking stops within a fraction of a second, and the jet starts winding down at once, stepping down to its lowest setting over several seconds (there's no 3-second wait)
- dataTracking is re-enabled when you re-enter the swimZone

### Pausing: Suspend and Resume

Press **Suspend** to take a break. 
- dataTracking stops
- the jet winds down to its lowest setting. 
- the button turns red (easy to spot while swimming) and says **Resume**
- press **Resume** to continue your swim and return back into the swimZone

As mentioned directly above, leaving the swimZone also suspends dataTracking but pressing the "Suspend" button will not allow dataTracking to resume if you re-enter the swimZone.

### Hold: a steady jet

Press **Hold** to adjust the jet flow to a constant level.
- you had already left the swimZone to reach the monitor and mouse
- data tracking had stopped
- the jet probably had or will soon have wound down to its lowest setting
- the button turns yellow and says **Vary**, an easily seen reminder that the jet is no longer following you
- immediately the jet will start to increase its flow to where it was when you exited the swimZone
- press and hold **UP** or **DN** to vary the jet flow as indicated by the Pace display

When you return back to the swimZone:
- the jet flow will not vary
- dataTracking resumes

Press **Vary** to go back to automatic control. 
- you had already left the swimZone to reach the monitor and mouse
- data tracking had stopped
- the jet winds down to its lowest level 
- PoolWind runs normally

Note that if a coach is pressing the buttons for you and you remain in the swimZone, the jet flow will not wind down and dataTracking remains active. 

Hold is useful for drills or steady-Pace training. Remember that in Hold,
the jet doesn't slow down if you fall back, get out of the swim zone, or even leave the pool.

### OnOff: the pump

**OnOff** turns the pool's pump on or off, the same as the button on the
pool's remote. PoolWind briefly stops adjusting the speed while it does
this, giving OnOff top priority.

## 5. Finishing a swim

Press **X** at the top right of the screen to close PoolWind. It then:

1. winds the jet down to its lowest setting,
2. releases its control of the pool's remote,
3. finishes saving your swim to your USB stick, or the Raspberry Pi if there's no stick, and
4. **ejects your USB stick** and tells you so.

When the message says **"USB stick ejected"**, you can remove your stick.
The next swimmer can insert theirs before starting PoolWind.

If the message says **"USB stick not ejected"**, your swim is still saved,
but don't pull the stick yet. Something else is using it (for example a
file manager window showing it). Close that, then eject the stick yourself:
click the **eject icon (⏏)** in the top bar of the screen and choose your
stick. Remove it when its icon disappears from the desktop.

**Why eject?** The Raspberry Pi doesn't write to a USB stick at once: it
can hold the last part of your swim in memory for up to half a minute.
Pulling a stick that hasn't been ejected can lose the end of your swim,
or leave the stick needing repair.

Once PoolWind is closed, the pool works normally with its own remote.

## 6. Your USB stick

Each swimmer has their own USB stick. It holds:

- **your settings**: height, Pace limits, logRate (optional), whether to record training video, and the control method (see [Your settings](#8-your-settings));
- **your swims**: a log of every swim and its training video, in a folder
  called `CSV Vault`.

Swimmers without a stick all share one log on the Pi, so their swims can't be told apart.

### Insert USB stick before, remove after

> **Insert your USB stick before starting PoolWind, and remove it only after
> PoolWind has closed and ejected it** (see
> [Finishing a swim](#5-finishing-a-swim)). Pulling it out during a swim won't
> affect the jet, but the rest of that swim won't be recorded. A stick
> inserted while PoolWind is running isn't used until the next start.

### How much it holds depends on **logRate**

**logRate** is how many snapshots of your swim PoolWind records each second.
See [logRate: how often PoolWind records](#lograte-how-often-poolwind-records)
for what it is, and why and how to change it.

A 32 GB USB stick, at the shipped logRate of 5, holds roughly 70 hours of swim data and video. At logRate of 15, the stick holds about 25 hours. It's a tradeoff of video smoothness vs data size.

If your stick is nearly full when PoolWind starts, it asks what to do:

- **Log in Main Memory**: save today's swim on the Raspberry Pi instead.
- **Erase Oldest Video**: delete your oldest training videos to make room.
  PoolWind shows exactly what it will delete and asks you to confirm first.
  Your swim logs are kept.
- **Eject & Replace**: eject the stick and close PoolWind, so you can use a
  different stick.

### Setting up a new stick

When PoolWind starts with a blank or unrecognized USB stick inserted, it
offers to set it up as a new swimmer's stick. You enter:

- the swimmer's **name** (it becomes the stick's name),
- their **height**, and
- their **Pace limits**: the slowest and fastest Pace the jet may run at.

**Setting up a stick erases everything on it.** PoolWind asks you to tick a
box confirming this before it continues.

For children and weaker swimmers, choose a **slow top Pace**, for example
3:00 per 100 yards.

## 7. Reviewing your swims: Swim Plot

Open the menu (**≡**, top left) and choose **Swim Plot...**.

While you're away from the pool screen, PoolWind doesn't adjust the jet:

- **"Leaving the pool screen"**: the jet first winds down to its lowest
  setting, and PoolWind lets go of the pool's UP and DN controls.
- **OnOff** still works: the calendar and the plot screen each have a button
  for the pump.
- **"Back to the pool screen"**: when you return, the jet winds down
  again and starts from its lowest setting, as at startup.

The same happens with **Set Swim Area...**.

### Choosing the days

A window with two calendars appears: **From** and **To**. Both start on
today. Days with swims are marked in green, and each shows that day's
average Pace. Pick a single day or a range, then press **OK**. If none of the
chosen days has a swim, PoolWind says so and stays on the calendars: pick a
green date. **Close** returns to the pool screen. **Pump On/Off** turns the
pool's pump on or off.

### The plot and video

The swim's training video plays together with a plot of your swim:

- **Pace** over time (shown first), or **MPH** over distance: switch with
  the **MPH** button. PoolWind remembers your choice.
- Faster swimming plots higher on the Pace plot.
- A **cursor** on the plot follows the video, frame by frame. Move the
  cursor and the video jumps to that moment.

**Controls:**

| Control | What it does |
|---|---|
| **▶ Play / Pause** | Plays or pauses. The video starts playing by itself and stops at the end |
| Mouse wheel over the plot | Zooms time or distance in and out |
| Mouse wheel over **Play** or the speed label | Plays faster or slower |
| **Compress Gaps** | Shortens the breaks between swims, so the plot shows mostly swimming |
| Left click on the plot and drag | Moves the cursor and swim video through time or distance |
| Right click on the plot and drag | Moves the entire plot and cursor left or right |
| Click on the video | Turns the [zone highlight](#seeing-the-jets-zone-the-zone-highlight) on or off (swims recorded since it was added) |
| **On/Off** | Turns the pool's pump on or off |
| **Close** | Back to the calendars, to pick another day |

### What to look for

The heart of PoolWind's training value is that you can see how different stroke styles and methods affect your swimming. In a macro view, you can see on the calendar's daily average Pace how you've improved day by day. Of course that depends on what your stroke style is and which ones you used during the day's session.

In the micro view, you can look at the video and see how each stroke and kick builds a momentary acceleration against the pool's stationary backdrop. Turn on the zone highlight for a clearer backdrop: it shows the zone of the jet's speed at that moment, so you can see each stroke carry you forward or let you slip back against it.

In between macro and micro views, the plots can tell you if those movements combine to build up speed but can never resolve down to the level that shows the effects of each single stroke or kick. A trained eye can look at all three views and determine what might improve style.

## 8. Your settings

Settings live in two places, with the **same names** in both:

- **The main settings file** (`poolwind_defaults.txt`, next to the
  program): the starting settings for everyone.
- **Your USB stick** (`poolwind_ind_defaults.txt`): your personal
  settings. Anything on your stick replaces the main file's value while
  your stick is in.

| Setting | Example | Meaning |
|---|---|---|
| `'swimmersHeight'` | `66` | Your height in inches. Helps PoolWind judge your position |
| `'paceMin, Max'` | `('5:00', '3:00')` | Slowest and fastest Pace the jet may run at, in minutes per 100 yards |
| `'recordTrainingVideo'` | `True` | Record the training video for Swim Plot (`True` or `False`) |
| `'algorithm (basic or swimmerPace)'` | `'swimmerPace'` | The control method. `'swimmerPace'` is the full method (use this); `'basic'` is a simpler one |
| `'logRate'` | `5` | Determines the number of video frames and related data that are written per second, 1 to 15. `5` is enough to follow your Pace and stroke rhythm; `15` gives smoother stroke details but fills your stick about three times faster. See [logRate](#lograte-how-often-poolwind-records) |

Two more settings work **only in the main settings file** (not on a stick):

| Setting | Example | Meaning |
|---|---|---|
| `'zoneHighlight'` | `False` | Whether the [zone highlight](#seeing-the-jets-zone-the-zone-highlight) is on when PoolWind starts (`True` or `False`). A tap on the picture still turns it on or off |
| `'zoneHighlightLevel'` | `0.2` | How bright the zone highlight is: `0.05` is barely seen, `0.3` is strong |

You can edit either file with a text editor. Keep the quote marks, commas
and brackets exactly as they are. Changes take effect within about a
second, even while PoolWind is running (except `recordTrainingVideo` and
`logRate`, which take effect at the next start).

### Finding your stick's settings file

Your stick's settings file is called `poolwind_ind_defaults.txt` and sits
at the top of the stick, next to the `CSV Vault` folder. To open it:

1. Double-click your stick's icon on the desktop. It has the swimmer's name
   you gave it when the stick was set up (for example `BILL_G`). If
   PoolWind has closed and ejected the stick, pull it out and plug it back
   in first.
2. Double-click `poolwind_ind_defaults.txt`. It opens in a text editor.
3. Make your change, save, and close the editor.
4. If PoolWind isn't running, eject the stick with the eject icon (⏏) in
   the top bar before removing it.

### logRate: how often PoolWind records

While you swim, PoolWind takes **snapshots**: each one is a line in your swim
log (time, Pace, distance) and one frame of your training video, always
together, so the plot and the video stay in step in Swim Plot. **logRate**
is how many snapshots it takes per second, from 1 to 15.

| logRate | Good for | Video | A 32 GB stick holds |
|---|---|---|---|
| `5` (shipped) | Everyday swims: following your Pace and stroke rhythm | Steps visibly from frame to frame | About 70 hours |
| `15` | Studying a single stroke or kick, slowed down in Swim Plot | Smooth, even in slow motion | About 25 hours |

**Why change it.** Raise it to `15` for sessions where you want to study
your technique closely: each arm pull and kick shows in three times as many
frames. Go back to `5` for everyday swims, so your stick doesn't fill three
times as fast. Lower than 5 saves more space but makes the video jumpy.

**How to change it.** Add or change this line in your stick's
`poolwind_ind_defaults.txt` (see
[Finding your stick's settings file](#finding-your-sticks-settings-file)):

```
,'logRate': 15
```

On your stick, it applies only to you. In the main settings file, it
applies to everyone whose stick doesn't set its own. **It takes effect the
next time PoolWind starts.** Swim Plot plays days recorded at different
rates together correctly, so you can switch as often as you like.

Other settings (the pool's calibration, safety limits and advanced tuning)
are covered in the setup and calibration guide. They're for technicians
and builders, not for day-to-day swimming.
