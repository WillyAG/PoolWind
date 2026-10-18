# PoolWind

**Swimmer-sensing jet control for swim-in-place pools.**

<img src="docs/images/PoolWind_Station_running.jpg" width="400" alt="The PoolWind station beside the pool: a portrait monitor in a waterproof case showing the pace, average pace and distance, with a waterproof keyboard and mouse">

> No GitHub account is needed to read or download anything here. If the
> GitHub app on your phone asks you to sign in, open the link in your web
> browser instead, or in a private (incognito) tab.

## PoolWind in brief

PoolWind monitors your swim with an overhead camera and adjusts the pool's jet flow so that you will not run into the front or the rear of the pool as you swim faster or slower. The pool is divided into "zones", each representing an increasing jet speed toward the front. As you move forward through these zones the jet flow will increase until you settle into a zone where your swim is balanced with the jet flow. Forward movement stops. Swim harder and you move into the next zone where the jet flow increases further. The program is set to your specifications and the last zone should be just beyond your most powerful stroke. When you decide to rest a bit, the jet will move you backwards to a zone where your swim is once again balanced as the jet flow relaxes. You can change stroke styles without running into walls.

That is the main crux of PoolWind but since it involves a camera and computer, it opens up other helpful possibilities.  It also estimates your actual swimming pace which is displayed on a monitor in letters large enough to see anywhere in the pool, along with the distance swum and the average pace at the current point in time. A big possibility that opened up is swim training, described below.

The PoolWind system is designed for swim training. Each swimmer can plug in their own USB stick and log in their swim session daily over multiple sessions. The camera records the swim and the USB stick stores the data and video. One menu of the program is "Swim Plot" that if selected not only shows the video but also shows a plot of Pace/time or MPH/distance with the cursor synchronized to the exact frame of the video at the moment. The video can be paused, sped up, and slowed down. Moving the cursor also moves the video forward or backward.  A calendar allows you to pick a range of dates to be displayed. Reviewing the logs can point out good and bad swimming habits and with average daily Pace being shown on each day of the calendar, progress can be seen at a glance.

The author's own experience: his kick used to be fairly random. By watching
his movements and seeing their effect on the pace plot, swim after swim, he
coordinated his legs with the rest of his body into a single, unified stroke
pattern and his speed improved noticeably as a result.


**PoolWind is a do-it-yourself project.** It comes with no warranty. Limited help may be found in [Discussions](../../discussions), where the author takes part at his discretion.

**Please read [SAFETY.md](SAFETY.md) before building or using PoolWind.**

## Getting started

1. **Read [SAFETY.md](SAFETY.md).**
2. **Check first:** [three checks to make before buying anything](docs/BUILD_GUIDE.md#before-you-buy-anything-three-checks): your remote, your pool's Pace Display port, and your skills.
   They take a few minutes and tell you whether PoolWind can work with your pool.
3. **Gather the parts:** the [parts list](hardware/PARTS_LIST.md), about $480 in all.
4. **Build it:** the [build guide](docs/BUILD_GUIDE.md).
5. **Install the software and fit it to your pool:** the [setup and calibration guide](docs/SETUP_GUIDE.md).
6. **Swim:** the [user manual](docs/USER_MANUAL.md).


## How it works

- PoolWind is an **add-on**. It does not modify the pool in any way:

- Control: wires are soldered to a spare copy of the pool's own handheld remote, and relays driven by a Raspberry Pi "press" its speed Up,  Down, and On/Off buttons.

- Feedback: the jet speed is read back as a voltage through the port that the manufacturer already provides for its optional Pace Display.

- Vision: a camera above the pool tracks where the swimmer is.

- The pool's own controls keep working as when manufactured. Without the PoolWind running, the pool operates normally using the other remote (usually supplied).

## Features

- Automatic jet speed from swimmer position, within pace limits you choose.

- "Swimmer Pace" estimate (your pace through the water, not just the jet setting)

- Distance, Swimmer Pace and Average Pace logged to a CSV file for every session

- "Swim Plot" for reviewing a day or a date range, synchronized with recorded video

- Hold mode: freeze the current speed, vary it with Up and Dn screen buttons

- Automatic detection if swimmer leaves the center swim zone, pausing data collection and lowering the jet flow to its lowest setting

- Per-swimmer USB sticks: personal settings (height, pace limits, video recording switch) and swim data. Months of data can be collected depending on the size of the USB stick
(Approx 70 hours on a 32 GB stick) 

- Safety voltage limits

- Jet flow winds down automatically at startup and shutdown to lowest level

- Waterproof: mouse, keyboard, case with clear door holding the Raspberry Pi and monitor at the poolside

## Compatibility

- Tested on:  Endless Pools, Standard Endless Pool (purchased February 2012). The controller board was later replaced after a lightning strike, and PoolWind works with the replacement.

- Other models: Untested. Other remotes may have similar buttons which can be used. But a feedback voltage is essential and a relationship between voltage and Pace must be measured in the form of data points.

- Lighting: PoolWind is developed and tested in an indoor installation with outdoor light coming through. Using artificial lights (tested at night) also works well.

- Outdoor use:  Untested, especially in direct sun. Surface glare, moving light patterns on the pool floor, and sharp shadows (including the swimmer's own) can confuse the camera's swimmer detection. Shade over the pool and a polarizing filter on the camera should help; full outdoor support may need further development.


*PoolWind is an independent project. It is not affiliated with or endorsed by Endless Pools. "Endless Pools" is used only to describe compatibility.*


## What's in this repository

- The PoolWind program (poolwind.py)
- Settings files (poolwind_defaults.txt, poolwind_calibration.txt) 
- Schematics, layout, and PCB Gerber files for the interface board in a [Fritzing](https://fritzing.org) file (a free circuit design program)
- Parts and source list
- Build guide, setup and calibration, user manual


## Hardware summary
- Raspberry Pi 5, monitor mounted in portrait, both in a waterproof case with a see-through door, and waterproof mouse and keyboard
- Overhead camera looking down on the swim area
- INA260 voltage/current sensor (I2C) reading the Pace Display port
- Relay board driven by GPIO 17 (Up), GPIO 18 (Down) and GPIO 27 (pump On/Off)
- A spare pool remote, with wires soldered to its buttons

Full details are in [`hardware/`](hardware/) and the build guide in [`docs/`](docs/).

## License

PoolWind is a shared hobby project, free for personal, hobby and other noncommercial use under the licenses described in [LICENSE.md](LICENSE.md). It isn't for sale, and commercial use isn't permitted.

Copyright © William A. Gorlitz. U.S. Copyright Registration TXu 2-304-621.


## Support

- No support is provided:  You're welcome to share builds, questions and answers with other users in [Discussions](../../discussions) in which the author may participate.


## Acknowledgments

- PoolWind relies on OpenCV, NumPy, SciPy, PyQt5 and matplotlib, and on the many people who share their knowledge online. Special thanks to Murtaza's Workshop for perspective adjustment and color filtering techniques. Program was conceived and prototype written by the author and further developed with the help of AI  (Grok, CoPilot, finishing with Anthropic's Claude Code).


