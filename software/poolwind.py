
if True:  # keep this here as an  easy way to skip over all this
    # poolwindAI_v15.3   -- PYSIDE6 instead of PyQt5 (GPL), so the
    #                         noncommercial license stands on its own:
    #                         imports, exec(), QAction in QtGui, matplotlib
    #                         backend_qtagg, mouse position(), the new-stick
    #                         checkbox (toggled). Install: apt
    #                         python3-pyside6.qtwidgets.
    #                       - poolLength 162 (the swim area: back wall to the
    #                         jet unit's edge), not 180 (the whole pool):
    #                         the body-reach correction was ~10% short.
    #                         DRIFT_SCALE stays 1.5 (1.67 was tried; 1.5
    #                         felt right in the pool).
    #                         The setting is renamed 'usablePoolLength'
    #                         ('poolLength' in older files is still read,
    #                         and the calibration file is saved renamed).
    #                       - STILLNESS CHECK REMOVED (2026-10-18): on
    #                         Raw_2026-09-29 (cover on) the cover's blob
    #                         moves with the lighting, so it isn't reliable.
    #                         The user manual says to close PoolWind before
    #                         putting a cover on.
    #
    # poolwindAI_v15.2   -- SWIM ZONE HIGHLIGHT, USB EJECT, STILLNESS CHECK:
    #                       - ZONE HIGHLIGHT: a tap on the picture (pool
    #                         screen and Swim Plot replay) lights the jet's
    #                         zone faintly, slowest at the bottom; it lags the
    #                         jet like the water (WATER_TAU), directly in
    #                         Hold. 'zoneHighlight' (off at start) and
    #                         'zoneHighlightLevel'. Swim log columns zone,
    #                         zones.
    #                       - Developer: 'comBar' and 'readouts' hide the CoM
    #                         bar and the dIdx / V / CoM numbers.
    #                       - USB STICK made safe to remove at close: written
    #                         and unmounted (not powered off), and mounted
    #                         again at the next start (no replug). Message
    #                         only if something is using it.
    #                         'ejectStickOnClose' is a user setting (also on a
    #                         stick). Eject & Replace ejects it too.
    #                       - The algorithm is a developer choice in the main
    #                         defaults file only (users get swimmerPace).
    #                       - PUMP buttons light red; On/Off off the main
    #                         screen asks "Are you sure?".
    #                       - SWIM PLOT: closely spaced pauses compress as
    #                         one gap; dates shown MM-DD-YYYY.
    #                       - developerMode turns the monitor with the
    #                         Monitor Toggle script; the landscape warning
    #                         points to it.
    #                       - STILLNESS CHECK: a "swimmer" that barely changes
    #                         for 'stillSeconds' (the pool cover's tape) is
    #                         not a swimmer; after 'autoSuspendMinutes' with
    #                         no swimmer PoolWind presses Suspend. Tested on
    #                         the 10-15-2026 video; not yet pool-tested.
    #                       - License notice: commercial use is not permitted.
    #                       Runs on PyQt5 (GPL). Archived 2026-10-18; the
    #                       next version, v15.3, will run on PySide6 (LGPL),
    #                       so the noncommercial license stands on its own.
    #
    # poolwindAI_v15.1   -- SAFETY, LOGGING AND SWIM PLOT fixes:
    #                       - UP/DN CAN'T STAY PRESSED off the main screen
    #                         (Bill, 2026-10-15: a relay left on while a plot
    #                         was open ran the jet to high). Swim Plot and Set
    #                         Swim Area wind down, then release UP/DN and
    #                         disconnect their pins (On/Off stays connected,
    #                         Hold off); coming back reconnects, winds down
    #                         again and starts from slow. A relay watchdog
    #                         releases UP/DN if the main loop stops for 1 s;
    #                         a wind-down gives up after 60 s; outputs are
    #                         claimed already off.
    #                       - ON/OFF on the calendar and plot screens. The
    #                         calendar won't open a day without swims ("Pick
    #                         a green date"); a plot without data has a "Back
    #                         to the calendar" button (no Esc needed).
    #                       - SWIM LOG on a steady schedule: 'logRate' rows and
    #                         video frames per second (built in 5, 1-15), set
    #                         in the defaults file or on a swimmer's stick;
    #                         the video keeps real time.
    #                       - SWIM PLOT: playback follows the recorded clock;
    #                         a gap needs a pause of at least 1 s; smoothing
    #                         is ~6 s at any rate.
    #                       - 'paceTrace' (built in off): the pace_trace debug
    #                         file only when switched on.
    #                       - A new USB stick mounts under the user's own
    #                         /media folder and IDs.
    #                       Pool-tested 2026-10-16: "the fixes worked."
    #                       Archived 2026-10-16; the next version is v15.2.
    #
        
    # just in case VCL gets real sluggish, close and try this in terminal:
    # code --disable-gpu

    # For flowcharting, ask AI this way:
    # “Make a Mermaid flowchart in the simple‑compatible style 
    # (no slashes, no HTML, no double brackets).”

    # Pace display manual: 
    # https://manualzz.com/doc/80503213/endless-pools-digital-pace-display-guide?utm_source=copilot.com&p=2

    """
    This program was conceived and written by William A. Gorlitz.
    Copyright (c) William A. Gorlitz. Copyright Reg # TXu 2-304-621.
    Licensed under the PolyForm Noncommercial License 1.0.0
    (https://polyformproject.org/licenses/noncommercial/1.0.0): free for
    personal, hobby and other noncommercial use. Commercial use is not
    permitted.

    This program would not have been possible had I not borrowed heavily
    from routines and methods found on the Internet. The imported packages
    of CV2 and numpy were especially essential (and free).

    Special thanks to Murtaza's Workshop for perspective adjustments and
    color filtering. And the most useful function is: "cent_Of_Mass" 
    from "scipy.ndimage" which threw out an unbelievable amount of barely 
    working code with a single word.


    """
    # --- Standard Library ---
    import sys
    import ast
    import time
    import math
    import random
    import glob
    import re
    import shutil
    from datetime import date, datetime, timedelta
    # --- Third‑Party Libraries (pip/apt installed) ---
    import cv2
    import numpy as np
    # --- Adafruit Hardware Libraries ---
    import board
    import adafruit_ina260
    # --- GPIO ---
    import lgpio
    import os
    # Qt for Python: PySide6 (LGPL), since v15.3. matplotlib's Qt canvas
    # uses the same binding.
    os.environ.setdefault("QT_API", "pyside6")

    import matplotlib
    matplotlib.use("Agg")     

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qtagg import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )


    import subprocess
    from PySide6 import QtWidgets, QtCore
    # Optional: pull specific classes for convenience
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QPushButton,
        QVBoxLayout, QHBoxLayout, QDialog, QMenu,
        QSizePolicy, QCheckBox, QMessageBox, QFrame,
        QCalendarWidget, QTableView
    )
    from PySide6.QtGui import (
        QAction, QPixmap, QImage, QPainter, QPen, QBrush, QColor, QFont, QCursor, QPalette,
        QTextCharFormat
    )
    from PySide6.QtCore import Qt, QTimer, QEvent, QPoint, QObject, QDate

    import stat, textwrap
    import collections

    #print = lambda *a, **k: None


# =====================================================================
# BUILT-IN SETTINGS (since v7.44)
# Values that were tuned during development and are now part of the
# program. They no longer appear in the defaults file. To change one
# without editing the program, copy its line (with the same name) into
# the defaults file: the file's value then replaces the one below, and
# it takes effect while running unless marked (at startup) -- those, and
# the workplace / device settings, need a program restart. Delete the
# line from the file to go back to the built-in value. Saving the
# defaults never adds these to the file.
# =====================================================================
BUILT_IN_DEFAULTS = {
    # --- developer tools ---
    # False for users: always camera / pool display / real valve, no
    # monitor switching, no development readouts, no raw video. True (in
    # the developer's defaults file) enables all of those, and the four
    # lines below. (Readouts are live; the rest need a restart.)
    'developerMode': False,

    # --- where the program runs (only used when developerMode is True) ---
    # A workplace line in the defaults file switches all three at once:
    # 'pool' = camera / pool / real, 'home' = video / work / simulate (desk
    # testing), and 'default' = use the three device lines as given. The
    # pump relay is connected only at 'pool', so 'default' with Valve 'real'
    # bench-tests the UP/DN relays with no chance of starting the pool motor.
    'workplace (home or pool or default)': 'pool',
    'capture_device (camera or video)': 'camera',    # live camera, or a recorded video
    'display_device (work or pool)': 'pool',         # pool = poolside monitor, rotated
    'Valve (real or simulate)': 'real',              # real = drive the jet relays

    # --- swimmer (fallbacks if the defaults file leaves them out) ---
    'paceMin, Max': ('5:00', '1:30'),    # pace limits (slowest, fastest), min/100 yd

    # --- control algorithm: developer choice (Bill, 2026-10-17) ---
    # 'swimmerPace' (the manuals are written around it), or 'basic' (the
    # simple baseline new algorithms are built on). Set in the main
    # defaults file only, on its own: not on a USB stick, and not tied to
    # developerMode.
    'algorithm (basic or swimmerPace)': 'swimmerPace',

    # --- swimmer detection ---
    'Sensitivity': 5000,                 # minimum swimmer size (pixels) to count as a swimmer
    'CoM filter Alpha': 0.05,            # smoothing of the swimmer's position (smaller = smoother, slower)
    'inactivity wind down time (sec)': 3,  # how long the swimmer may be missing before the jet winds down (at startup)

    # --- Swimmer Pace estimator (Algorithm 'swimmerPace') ---
    'DRIFT_SCALE': 1.5,                  # weight of the swimmer's forward/back drift
    'WATER_TAU': 5.0,                    # seconds the water speed lags the jet setting
    'DRIFT_TAU': 5.0,                    # seconds of smoothing on the drift speed
    'DRIFT_MAX': 25.0,                   # cap on the drift speed (yards/min)

    # --- logging and runtime ---
    # Swim log rows and training video frames per second (at startup).
    # 'logRate' in the defaults file overrides it for everyone (e.g. a
    # coach's choice), and on a USB stick for that swimmer.
    # 5 is smooth enough for pace; 15 gives smooth stroke video at three
    # times the storage. Limited to LOG_RATE_RANGE.
    'logRate': 5,
    # Eject the USB stick when PoolWind closes (a user setting, also on a
    # stick: a swimmer who keeps their stick in all the time sets False).
    'ejectStickOnClose': True,
    'paceTrace': False,                  # developer: pace_trace_*.csv debug file, ~15 MB/hour (live)
    'comBar': True,                      # developer: the CoM bar, pool screen and replay (live)
    'readouts': True,                    # developer: the dIdx / V / CoM numbers on the pool screen (live)
    'Runtime: hotReloadParameters': True,  # pick up defaults-file and USB-stick edits while running

    # --- swim zone highlight ---
    # The zone of the pool that matches the jet's current speed is lit up
    # faintly, on the pool screen and on Swim Plot replay. A tap on the
    # picture switches it on or off (both screens).
    'zoneHighlight': False,              # True = shown when the program starts
    'zoneHighlightLevel': 0.20,          # how bright: 0.05 barely seen, 0.3 strong
}


class App:
    def __init__(self):

        # ---------------------------------------------------------
        # Latest additions (to be integrated into proper sections)
        # ---------------------------------------------------------
        self.firstTime = True
        self.ema_voltage = None
        self.filteredCoM = None
        self.priorValveIndex = 0
        self.allow_UP = True
        self.allow_DN = True

        self._ema_pool_pace = None

        self.pool_pace = 0.0   # control pace
        self.swim_pace = 0.0   # display/logging pace

        # Pace EMA state
        self._ema_pace = None
        self.PACE_ALPHA = 0.25   # tune 0.1–0.3 depending on how smooth you want it
        self.systemShutdown = False
        self.pause_update_loop = False

        # standard work size
        self.work_size_w = 480
        self.work_size_h = 640
        aspect_ratio = self.work_size_w / self.work_size_h
        self.CoM_size_h = 1000.0
        self.CoM_size_w = 1000.0 * aspect_ratio

        self.last_log_time = 0

        # ---------------------------------------------------------
        # Load defaults + store startup state
        # ---------------------------------------------------------
        # 1. Build path to defaults file: <program name>_defaults.txt in the
        #    program's own folder (e.g. PoolWind.py -> PoolWind_defaults.txt)
        #    and its calibration file, <program name>_calibration.txt
        _prog = os.path.abspath(__file__)
        _base = os.path.join(os.path.dirname(_prog), os.path.splitext(os.path.basename(_prog))[0])
        self.defaults_path    = _base + "_defaults.txt"
        self.calibration_path = _base + "_calibration.txt"

        # 2. Calibration (pace table, safety limits, swim area), then the
        #    defaults file over the BUILT_IN_DEFAULTS, with calibration on top
        self.calibration = self._load_calibration()
        try:
            self.REPdefaults = self._read_defaults_file()
            self.original_defaults = self.REPdefaults.copy()
            self.REPdefaults = self._derive_internal_defaults(self.REPdefaults)

        except Exception as e:
            print("Error loading defaults file:", e)
            sys.exit()

        # ---------------------------------------------------------
        # Per-swimmer USB overlay: if a drive with poolwind_ind_defaults.txt
        # is mounted, overwrite the swimmer-specific values in REPdefaults.
        # The drive is identified by this file's presence, not its OS-
        # assigned label/mount path (labels can collide or get silently
        # renamed, e.g. MUSIC -> MUSIC1, if replugged before a clean
        # unmount). The main defaults file on disk is never touched by
        # this (the program doesn't write that file at all).
        # ---------------------------------------------------------
        self._ind_defaults = None
        self._ind_path = None        # the stick's poolwind_ind_defaults.txt (hot-reloaded)
        self._ind_mtime = None
        self._ind_check_t = 0.0
        self.usb_data_dir = None
        ind_defaults, usb_root = self._find_individual_defaults()
        self._stick_root = None      # the swimmer's stick, ejected at close
        if ind_defaults is not None:
            self._apply_individual_defaults(ind_defaults)
            self.usb_data_dir = usb_root
            self._stick_root = usb_root
            self._check_usb_free_space()
        else:
            # No configured swimmer stick found -- if a blank/unrecognized
            # removable drive is plugged in instead, offer to format and
            # set it up as one. Checked only here at startup (not during
            # the live video/tracking loop) so it never adds filesystem
            # polling cost to the real-time path.
            self._offer_usb_drive_setup()

        # ---------------------------------------------------------
        # Set up monitor orientation (hardware change)
        # ---------------------------------------------------------
        self.display_device = self.REPdefaults["display_device (work or pool)"]

        # Monitor switching between the developer's landscape coding layout
        # and the poolside portrait layout -- developer only. Users get
        # portrait at every start (the install runs toggle_monitor.sh
        # portrait) and turn it with the desktop's Monitor Toggle.
        if self.REPdefaults["developerMode"]:
            last = self.detect_current_mode()

            # If mode changed, rotate + restart
            if self.display_device != last:
                # The Monitor Toggle script knows this monitor (its output
                # name and sizes are set at the top of the script); the
                # xrandr lines are the fallback without it.
                toggle = os.path.expanduser("~/.local/bin/toggle_monitor.sh")
                want = "portrait" if self.display_device == "pool" else "landscape"
                if os.access(toggle, os.X_OK):
                    subprocess.run([toggle, want])
                elif want == "portrait":
                    subprocess.run([
                        "xrandr", "--output", "HDMI-1",
                        "--mode", "800x600",
                        "--rotate", "left"
                    ])
                else:
                    subprocess.run([
                        "xrandr", "--output", "HDMI-1",
                        "--mode", "1280x800",
                        "--rotate", "normal"
                    ])


                # **************** RESTART PROGRAM ******************

                qt_app.quit()
                qt_app.exit()
                python = sys.executable
                os.execl(python, python, *sys.argv)

        # ---------------------------------------------------------
        # Read actual monitor resolution + usable area
        # ---------------------------------------------------------
        screen = QApplication.primaryScreen()

        full   = screen.geometry()            # full monitor resolution (e.g., 1280x800)
        avail  = screen.availableGeometry()   # minus Pi menu bar

        monitor_w = full.width()
        monitor_h = full.height()
        usable_h  = avail.height() - 70   # your WORK-mode adjustment

        # ---------------------------------------------------------
        # Standard aspect ratio (hardware)
        # ---------------------------------------------------------
        # always have standard_aspect based on portrait mode w/h (<= 1)
        standard_aspect = min(monitor_w, monitor_h) / max(monitor_w, monitor_h)

        # ---------------------------------------------------------
        # Window sizing (WORK vs POOL) Global for all classes
        # ---------------------------------------------------------
        if self.display_device == "pool":
            # Full-screen portrait window (monitor is physically rotated)
            self.window_h = monitor_h      # e.g., 1280
            self.window_w = monitor_w      # e.g., 800
            if monitor_w > monitor_h:
                # Monitor still in landscape (left there by the Monitor
                # Toggle; only developerMode switches it): keep the
                # portrait shape instead of stretching the picture sideways.
                self.window_w = int(monitor_h * standard_aspect)
                print("The monitor is in landscape. PoolWind is meant for a portrait "
                      "monitor: double-click Monitor Toggle on the desktop, then "
                      "start PoolWind again.")
        elif self.display_device == "work":
            # Landscape window (fits usable height, leaves room for coding)
            self.window_h = usable_h       # e.g., 694
            self.window_w = int(usable_h * standard_aspect)  # portrait aspect → narrow window
        else:
            raise ValueError("Invalid display_device in defaults file")

        # Track modification time for hot-reload
        self.defaults_mtime = os.path.getmtime(self.defaults_path)

        self.GAP_SEC = 3      # ignore segments with >3 seconds between samples
        self.YARDS_PER_MILE = 1760.0


        # ---------------------------------------------------------
        # All CSV/AVI/raw-video data lives here (reading and writing).
        # Goes to the swimmer's own USB stick (found above) if one is
        # present, otherwise the local Vault as before.
        # ---------------------------------------------------------
        if self.usb_data_dir is not None:
            self.data_dir = os.path.join(self.usb_data_dir, "CSV Vault")
            os.makedirs(self.data_dir, exist_ok=True)
        else:
            self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CSV Vault")
            os.makedirs(self.data_dir, exist_ok=True)   # a fresh install has none yet

        # Load CSV file
        # --- Determine suspend/resume state based on today's log file ---
        self.todayCsvFile = os.path.join(self.data_dir, f"{date.today()}.csv")
        self.suspendButtonText = "Resume" if os.path.isfile(self.todayCsvFile) else "Begin"

        # Load today's CSV
        time_raw, pace_raw, dist_raw, segment_raw, frame_raw = self.load_today_csv()

        # Default if no CSV yet
        self.last_segment_id = 0

        # Recover last segment ID from CSV
        if len(segment_raw) > 0:
            self.last_segment_id = segment_raw[-1]

        # Recover last distance
        self.total_distance = dist_raw[-1] if len(dist_raw) > 0 else 0.0

        # Rebuild pacePoints and swimtime
        self.pacePoints = []
        self.total_swimtime = 0.0
        prev_t = None

        for t, p, d in zip(time_raw, pace_raw, dist_raw):
            self.pacePoints.append((t, p))

            if prev_t is not None:
                dt_sec = t - prev_t
                if dt_sec <= self.GAP_SEC:
                    self.total_swimtime += dt_sec / 60.0

            prev_t = t

        # UI fields
        self.PaceDisplay = "0:00"
        self.distanceSwam = f"{self.total_distance:.3f} mi"

        if self.total_swimtime > 0 and self.total_distance > 0:
            avgSwimRate = self.total_distance / self.total_swimtime  # miles/min
            avgPace = (100.0 / self.YARDS_PER_MILE) / avgSwimRate    # min per 100y
            self.avgPaceDisplay = Utils.DecimalToTime(avgPace)
        else:
            self.avgPaceDisplay = "0:00"

        # ---------------------------------------------------------
        # Extract Non Hot changeable parameters from self.REPdefaults
        # ---------------------------------------------------------
        lo, hi = self.LOG_RATE_RANGE
        rate = self.REPdefaults[self.KEY_LOGRATE]
        try:
            rate = int(round(float(rate)))
        except (TypeError, ValueError):
            rate = BUILT_IN_DEFAULTS[self.KEY_LOGRATE]
        if not lo <= rate <= hi:
            print(f"logRate {rate} is outside {lo}-{hi}; using {min(hi, max(lo, rate))}")
            rate = min(hi, max(lo, rate))
        self.data_recs_per_sec  = rate
        self.data_interval_sec  = 1.0 / self.data_recs_per_sec

        self.capture_device = self.REPdefaults["capture_device (camera or video)"]
        self.valveOption = self.REPdefaults["Valve (real or simulate)"]
        self.zoneWidth = self.REPdefaults["middleSwimZone %"] / 100

        # ---------------------------------------------------------
        # Swim Area configuration from saved PlacePoints
        # ---------------------------------------------------------
        # Camera: the calibration file. Video: each test video sets its own
        # points in the code below (this is only the fallback).
        self.swimAreaPoints = self.REPdefaults["swimAreaPoints"]

        # ---------------------------------------------------------
        # Video source selection
        # handy conversion code:
        #    ffmpeg -i /home/poolwind/poolwind/BillSwim2.mp4 -vf "scale=640:480,fps=30" -c:v libx264 -preset veryfast -crf 18 -c:a copy /home/poolwind/poolwind/BillSwim2a.mp4
        # ---------------------------------------------------------

        if self.capture_device == "video":

            self.video_source = "Raw_2026-10-17_13-05-11.mp4"
            #self.video_source = "Raw_2026-09-29_15-29-18.mp4" #Raw_2026-10-17_13-05-11.mp4"
            self.startLater_inSeconds = 310
            self.video_speed = 1.0   # 0.5x, 1x, 2x, etc.
            self.swimAreaPoints = [(141, 151), (475, 146), (377, 608), (190, 585)]

            # self.video_source = "Raw_2026-09-29_15-29-18.mp4"
            # self.startLater_inSeconds = 310
            # self.video_speed = 1.0   # 0.5x, 1x, 2x, etc.
            # self.swimAreaPoints = [(141, 151), (475, 146), (377, 608), (190, 585)]

            # self.video_source = "BillSwim2.mp4"  
            # self.startLater_inSeconds = 400 # 90 #400
            # self.video_speed = 1.0   # 0.5x, 1x, 2x, etc.
            # self.swimAreaPoints = [(83, 152), (421, 151), (341, 571), (175, 578)]

            # self.video_source = "Raw_2026-06-24_14-40-00.mp4"     #"output1.mp4"
            # self.startLater_inSeconds = 0
            # self.video_speed = 1.0   # 0.5x, 1x, 2x, etc.
            # self.swimAreaPoints = [(119, 148), (461, 142), (369, 600), (170, 588)]


            # Automatically detect FPS from the MP4 file
            cap = cv2.VideoCapture(self.video_source)
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()

            # Fallback if OpenCV returns 0 or nonsense
            if fps <= 0:
                fps = 30.0

            self.video_fps = fps
            self.frame_period = 1.0 / self.video_fps

        elif self.capture_device == "camera":
            self.video_source = 0
        else:
            raise ValueError("Invalid capture_device in defaults file")

        # ---------------------------------------------------------
        # Pace / plateau configuration
        # ---------------------------------------------------------
        self.speedArray = self.REPdefaults["pace_voltage"]
        self.SafetyVoltageLimits = self.REPdefaults["SafetyVoltageLimits"]
        self.plateau_voltages = [v for (pace, v) in self.speedArray]
        self.noiseAllowedPercent_valve = 0.15
        self.noiseAllowedPercent_desired = 0.40
        self.overLap = 0.75

        # ---------------------------------------------------------
        # INA260 sensor (only for real valve mode)
        # had problems with OS:
        # 
        # sudo nano /boot/firmware/config.txt
        # fix by uncommenting
        # dtparam=i2c_arm=on
        # ctrl-o, Enter, ctrl-x, reboot
        # ---------------------------------------------------------
        if self.valveOption == "real":
            i2c = board.I2C()
            self.ina260 = adafruit_ina260.INA260(i2c)
        else:
            self.ina260 = None

        # ---------------------------------------------------------
        # Valve abstraction (simulate or real)
        # ---------------------------------------------------------
        if self.valveOption == "simulate":
            self.valve = SimulatedValve(self)
        else:
            self.valve = self

        # ---------------------------------------------------------
        # GPIO setup
        # ---------------------------------------------------------
        self.GPIO = GPIOWrapper()
        self.GPIO.setwarnings(False)
        self.GPIO.setmode(None)

        if self.valveOption == "real":
            self.PIN_UP = 17
            self.PIN_DN = 18
            # Pump stays disconnected (None -> GPIOWrapper.setup/output
            # both no-op, same mechanism that already keeps it safe in
            # "simulate" mode) unless actually running at the pool. Lets
            # the real UP/DN valve relays be bench-tested from home
            # (workplace 'default' with Valve set to 'real') with zero
            # chance of the pool motor turning on. workplace 'home'
            # already forces Valve to 'simulate' on its own above, so in
            # practice this only ever matters for 'default'.
            self.PIN_PUMP = 27 if self.REPdefaults["workplace (home or pool or default)"] == "pool" else None
        else:
            self.PIN_UP = None
            self.PIN_DN = None
            self.PIN_PUMP = None

        self.GPIO.setup(self.PIN_UP, self.GPIO.OUT)
        self.GPIO.setup(self.PIN_DN, self.GPIO.OUT)
        self.GPIO.setup(self.PIN_PUMP, self.GPIO.OUT)

        self.GPIO.output(self.PIN_UP, True)
        self.GPIO.output(self.PIN_DN, True)
        self.GPIO.output(self.PIN_PUMP, True)

        # ---------------------------------------------------------
        # App state variables (UI / display)
        # ---------------------------------------------------------
        self.currentVoltage = 0.0
        self.desiredVoltage = 0.0

        self.desiredDirection = "LEVEL" # only set in PushButton
        self.currentDirection = "LEVEL" # only set in relay

        self.manual_direction = None

        self.valveIndex = 6 if self.valveOption == "simulate" else 0
        self.desiredIndex = self.valveIndex

        self.initial_voltage_winddown()

        # ---------------------------------------------------------
        # Create controller
        # ---------------------------------------------------------
        self.PaceLimitsDec = self.REPdefaults["PaceLimitsDec"]
        self.controller = SwimController(self)

        # ---------------------------------------------------------
        # Now create the REAL video capture object with correct filter
        # ---------------------------------------------------------
        self.myVideoCapture = MyVideoCapture(self)

        # Raw/Training video recording is config-driven, not manually
        # selected -- recordRawVideo is a technician setting (calibration
        # file), recordTrainingVideo can be overridden per-swimmer via
        # the USB stick overlay above.
        self.myVideoCapture.makeRawVideo = ("Start" if self.REPdefaults["developerMode"]
                                            and self.REPdefaults["recordRawVideo"] else "Close")
        self.myVideoCapture.makePerspectVideo = "Start" if self.REPdefaults["recordTrainingVideo"] else "Close"

        # ---------------------------------------------------------
        # Misc runtime state
        # ---------------------------------------------------------
        self.view_mode = 1
        self.hold_mode = False
        self.frozen_CoM_h = 1

        self.raw_voltage = 0.0      # unsmoothed 5-read average (pace trace)

    def UpdateLoop(self):
        self._last_update_loop_t = time.time()      # relay watchdog heartbeat
        # ------------------------------------------------------------
        #  Measure valve voltage (real or simulated)
        # ------------------------------------------------------------
        valveVoltage = self.takeReading()
        self.currentVoltage = valveVoltage
        # ------------------------------------------------------------
        # Retrieve swim info
        # ------------------------------------------------------------
        logDistance = self.window.logDistance
        CoM = self.window.CoM_h

        # Update pool_pace from voltage (infrastructure, same for every algorithm)
        now = time.time()
        raw_pace = self.updateVoltageAndPace(valveVoltage, now)

        # Find current plateau index
        self.valveIndex = self.findClosestPlateauIndex(
            valveVoltage,
            self.noiseAllowedPercent_valve,
            self.plateau_voltages
        )

        # The jet's zone, for the swim zone highlight (display and log only)
        self.jetZone, self.jetZones = self.controller.jet_zone(valveVoltage)

        # ------------------------------------------------------------
        # Selected algorithm (defaults file) -> desired index + swim_pace
        # ------------------------------------------------------------
        self.desiredIndex, self.swim_pace = self.controller.runAlgorithm(CoM, now, self.pool_pace)
        self._update_pace_display(now)
        self._write_pace_trace(now, valveVoltage, raw_pace)

        # Drive the relays: hold UP/DN until the jet reaches the desired step.
        # (A short-press drive was tried in v7.42 and removed: the radio
        # remote loses ~30-50% of single presses and occasionally sends the
        # previous command -- pace notes section 15.)
        if getattr(self, "_winding_down", False):
            pass    # a wind-down is holding DN (initial_voltage_winddown): hands off
        elif getattr(self, "_pump_pulsing", False):
            # OnOff sequence in progress: hands off UP/DN (see OnOff_btn_press)
            if self.currentDirection != "LEVEL":
                self.relay_off()
        else:
            self._hold_drive(valveVoltage)

        # --------------------------------------------------------
        #  Suspend button will accumulate distance
        # --------------------------------------------------------
        if self.suspendButtonText == "Suspend" and logDistance:
            self.accrue_log_disp()

        self.priorValveIndex = self.valveIndex

    def _hold_drive(self, valveVoltage):
        """Hold UP/DN until the (EMA) voltage reaches the desired step."""
        # Decide direction
        if self.desiredIndex > self.valveIndex:
            self.desiredDirection = "UP"
        elif self.desiredIndex < self.valveIndex:
            self.desiredDirection = "DN"
        else:
            self.desiredDirection = "LEVEL"

        # --------------------------------------------------------
        # Safety gating based on absolute voltage limits
        # --------------------------------------------------------
        minV, maxV = self.SafetyVoltageLimits
        self.allow_DN = valveVoltage > minV   # allow DN if above min
        self.allow_UP = valveVoltage < maxV   # allow UP if below max

        # --------------------------------------------------------
        # Act on decision
        # --------------------------------------------------------
        if self.desiredDirection == "LEVEL":
            self.relay_off()

        else:
            # --- DN request ---
            if self.desiredDirection == "DN":
                if self.allow_DN:
                    if self.currentDirection != "DN":
                        self.DN_relay()
                else:
                    # Block DN only
                    if self.valveOption == "simulate":
                        self.valve.sim_relay_off()
                    else:
                        self.GPIO.output(self.PIN_DN, True)  # de-energize DN only

            # --- UP request ---
            if self.desiredDirection == "UP":
                if self.allow_UP:
                    if self.currentDirection != "UP":
                        self.UP_relay()
                else:
                    # Block UP only
                    if self.valveOption == "simulate":
                        self.valve.sim_relay_off()
                    else:
                        self.GPIO.output(self.PIN_UP, True)  # de-energize UP only

    def accrue_log_disp(self):
        if self.pool_pace == 0:
            return

        # ------------------------------------------------------------
        # 1. Log pace point (RAM + CSV) on a steady schedule of
        #    logRate rows a second
        # ------------------------------------------------------------
        # Rows are due at fixed times (one interval apart), not "one
        # interval after the last row": the loop only gets here every
        # ~25 ms, and waiting a full interval after each late row lost a
        # bit every time (15 rows/s came out ~11/s, so the training video,
        # whose file says 15 fps, played too fast in other players). If
        # the loop falls a whole slot behind, the video frame is repeated
        # so the video keeps real time. After a pause (out of the lane,
        # Suspend) the schedule starts fresh.
        now = time.time()                     # full epoch timestamp
        timestamp = round(now, 2)

        interval = self.data_interval_sec
        due = getattr(self, "_next_log_due", 0.0)
        if now < due:
            return
        if now - due > 0.5:
            frame_slots = 1                   # first row, or back after a pause
            due = now
        else:
            frame_slots = 1 + int((now - due) / interval)
        self._next_log_due = due + frame_slots * interval
        self.last_log_time = now

        pace = round(self.swim_pace, 2)

        # Append to RAM
        self.pacePoints.append((timestamp, pace))

        # Pace sanity-check accumulators (this run only -- reset each
        # launch, not reloaded from CSV history). See
        # poolwindAI_v7.39_pace_notes.txt section 5: avg(swim_pace) should
        # converge to avg(pool_pace) over a full session; logged at
        # shutdown as an ongoing check on the estimator.
        self._pace_check_sum_pool = getattr(self, "_pace_check_sum_pool", 0.0) + self.pool_pace
        self._pace_check_sum_swim = getattr(self, "_pace_check_sum_swim", 0.0) + self.swim_pace
        self._pace_check_n = getattr(self, "_pace_check_n", 0) + 1

        # ------------------------------------------------------------
        # 2. Update swim stats incrementally
        # ------------------------------------------------------------
        if len(self.pacePoints) < 2:
            return

        prev_t, prev_p = self.pacePoints[-2]
        dt_sec = timestamp - prev_t

        # Ignore large gaps
        if dt_sec > self.GAP_SEC:
            return

        dt = dt_sec / 60.0  # minutes

        mpm_prev = 1.0 / (prev_p * 17.6)
        mpm_now  = 1.0 / (pace   * 17.6)

        dA = dt * (mpm_prev + mpm_now) / 2.0

        self.total_distance += dA
        self.total_swimtime += dt

        # ------------------------------------------------------------
        # 3A. Append to PWV (perspect video) and get frame number
        # ------------------------------------------------------------
        if not hasattr(self, "last_perspect_img") or self.last_perspect_img is None:
            segment_id = self.last_segment_id
            frameNum   = 0
        else:
            for _ in range(frame_slots):      # >1 only if the loop fell a slot behind
                segment_id, frameNum = self.myVideoCapture._perspect_video_writer(self.last_perspect_img)


        # ------------------------------------------------------------
        # 3B. Append to CSV: epoch time, pace, cumulative distance,
        #     segment number, frame number within segment
        # ------------------------------------------------------------
        try:
            with open(self.todayCsvFile, "a") as f:
                # columns 6-7 (since v7.43): CoM_h and the swimmer tick's
                # CoM_w (-1 = no tick), for the CoM bar on swim plot replay
                com_h = int(self.window.CoM_h or 0)
                com_w = self.window.com_w_tick()
                com_w = -1 if com_w is None else int(com_w)
                # columns 8-9 (since v15.2): the jet's zone (-1 = none) and
                # the number of zones, for the swim zone highlight on replay
                zone = getattr(self, "jetZone", None)
                zone = -1 if zone is None else int(zone)
                zones = int(getattr(self, "jetZones", 0) or 0)
                f.write(f"{timestamp:.2f},{pace:.2f},{self.total_distance:.3f},{segment_id},{frameNum},"
                        f"{com_h},{com_w},{zone},{zones}\n")
        except OSError as e:
            # Last-resort net: the mid-session free-space reserve in
            # _perspect_video_writer should make this unreachable, but
            # skip this row rather than crash the live tracking loop.
            print("CSV write failed, skipping row:", e)

        # ------------------------------------------------------------
        # 4. Update UI display fields
        # ------------------------------------------------------------
        self.distanceSwam = f"{self.total_distance:.3f} mi"

        if self.total_swimtime > 0 and self.total_distance > 0:
            avgSwimRate = self.total_distance / self.total_swimtime
            avgPace = (100.0 / self.YARDS_PER_MILE) / avgSwimRate
            self.avgPaceDisplay = Utils.DecimalToTime(avgPace)
        else:
            self.avgPaceDisplay = "--:--"

    # Minimum free space needed on a swimmer's USB stick for one full
    # swim session, with a 1.5x safety margin over the measured baseline
    # (354 MB/hr with training video, 424 KB/hr CSV-only) since actual
    # video size varies with motion/lighting.
    # Minimum free space needed on a swimmer's USB stick for one full
    # swim session, with a 1.5x safety margin over the measured baseline
    # (354 MB/hr with training video, 424 KB/hr CSV-only) since actual
    # video size varies with motion/lighting.
    USB_NEEDED_BYTES_WITH_VIDEO = int(354 * 1024 * 1024 * 1.5)
    USB_NEEDED_BYTES_CSV_ONLY   = int(424 * 1024 * 1.5)

    def _check_usb_free_space(self):
        """
        Called once at startup, right after a swimmer's USB stick is
        recognized (self.usb_data_dir is already set). If there isn't
        enough room left for a full session, prompts for how to proceed.
        As a result self.usb_data_dir may get cleared (falls back to
        local SD storage for this session) or the drive may get some of
        its oldest video erased -- either way, the per-swimmer settings
        already overlaid into self.REPdefaults above are untouched.
        """
        needed = (self.USB_NEEDED_BYTES_WITH_VIDEO
                  if self.REPdefaults["recordTrainingVideo"]
                  else self.USB_NEEDED_BYTES_CSV_ONLY)

        try:
            free = shutil.disk_usage(self.usb_data_dir).free
        except Exception:
            return  # can't check -- don't block startup over it

        if free >= needed:
            return

        while True:
            box = QMessageBox(
                QMessageBox.Warning, "USB Drive Nearly Full",
                "There may not be enough space left on your USB drive for "
                "a full swim session.\n\nHow would you like to proceed?"
            )
            log_btn   = box.addButton("Log in Main Memory", QMessageBox.AcceptRole)
            erase_btn = box.addButton("Erase Oldest Video", QMessageBox.DestructiveRole)
            eject_btn = box.addButton("Eject && Replace", QMessageBox.RejectRole)
            box.setDefaultButton(log_btn)
            box.exec()
            clicked = box.clickedButton()

            if clicked is log_btn:
                # Storage destination only -- swimmer's personal settings
                # (already applied above) still come from the stick.
                self.usb_data_dir = None
                return

            if clicked is eject_btn:
                if self._eject_stick(self.usb_data_dir):
                    text = ("The USB stick has been ejected. Remove it, insert "
                            "a different one, and start PoolWind again.")
                else:
                    text = ("The USB stick couldn't be ejected: something else "
                            "is using it. Close anything showing the stick, "
                            "eject it with the eject icon (\u23cf) in the top "
                            "bar, insert a different one, and start PoolWind again.")
                QMessageBox.information(None, "Replace USB Drive", text)
                sys.exit()

            # Erase Oldest Video -- plan which files this would delete
            # first and get explicit confirmation before touching
            # anything (added 2026-08-27 after an earlier live test, run
            # with an artificially-unreachable threshold, ended up
            # deleting nearly the entire real video history with no way
            # to see or stop it beforehand).
            plan = self._plan_oldest_usb_video_deletion(needed - free)
            if not plan:
                QMessageBox.warning(
                    None, "Nothing To Delete",
                    "There are no older video files that can be erased."
                )
                continue

            if not self._confirm_video_deletion(plan):
                continue   # user cancelled -- back to the 3-option prompt

            freed = self._delete_planned_usb_video(plan)
            try:
                free = shutil.disk_usage(self.usb_data_dir).free
            except Exception:
                free = 0

            if free >= needed:
                QMessageBox.information(
                    None, "Space Freed",
                    f"Freed {freed // (1024 * 1024)} MB of old video. "
                    "Continuing with the USB drive."
                )
                return

            # Not enough could be freed -- loop back so the swimmer can
            # pick a different option instead of getting stuck here.
            QMessageBox.warning(
                None, "Still Not Enough Space",
                "Could not free enough space from old video files. "
                "Please choose another option."
            )

    def _plan_oldest_usb_video_deletion(self, min_bytes_to_free):
        """
        Figures out which whole oldest swim sessions (each a
        <date>_<segment>.avi Training-video file -- one file per
        session, see MyVideoCapture._perspect_video_writer) from the USB
        CSV Vault would need to be deleted, oldest date and oldest
        segment first, to free at least min_bytes_to_free -- without
        deleting anything yet. CSV log files are never included, only
        video. Returns a list of (path, size_bytes) tuples.
        """
        vault_dir = os.path.join(self.usb_data_dir, "CSV Vault")
        csv_files = sorted(glob.glob(os.path.join(vault_dir, "????-??-??.csv")))

        plan = []
        planned_bytes = 0
        for csv_path in csv_files:
            date_str = os.path.basename(csv_path)[:-4]
            avi_files = sorted(glob.glob(os.path.join(vault_dir, f"{date_str}_*.avi")))
            for avi_path in avi_files:
                try:
                    size = os.path.getsize(avi_path)
                except OSError:
                    continue
                plan.append((avi_path, size))
                planned_bytes += size
                if planned_bytes >= min_bytes_to_free:
                    return plan
        return plan

    def _confirm_video_deletion(self, plan):
        """
        Shows the exact list of video files a deletion plan would erase
        and asks for explicit confirmation. Returns True only if the
        swimmer clicked Delete; Cancel is the default (Enter-safe).
        """
        total_mb = sum(size for _, size in plan) / (1024 * 1024)

        dlg = QDialog(None)
        dlg.setWindowTitle("Confirm Video Deletion")
        layout = QVBoxLayout(dlg)

        label = QLabel(
            f"The following {len(plan)} video file(s) will be "
            f"permanently deleted (~{total_mb:.0f} MB total). "
            "CSV logs are never deleted."
        )
        label.setWordWrap(True)
        layout.addWidget(label)

        file_list = QtWidgets.QListWidget()
        for path, size in plan:
            file_list.addItem(f"{os.path.basename(path)}  ({size / (1024 * 1024):.1f} MB)")
        layout.addWidget(file_list)

        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("color: red; font-weight: bold;")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setDefault(True)
        cancel_btn.setAutoDefault(True)
        delete_btn.clicked.connect(dlg.accept)
        cancel_btn.clicked.connect(dlg.reject)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        return dlg.exec() == QDialog.Accepted

    def _delete_planned_usb_video(self, plan):
        """Deletes exactly the files a prior _plan_oldest_usb_video_deletion
        call listed and the swimmer confirmed. Returns bytes actually freed."""
        freed = 0
        for path, size in plan:
            try:
                os.remove(path)
                freed += size
            except OSError:
                continue
        return freed

    def _mount_usb_sticks(self):
        """
        Mounts any USB stick that is plugged in but not mounted, such as
        the stick PoolWind unmounted when it last closed. Bill, 2026-10-17:
        the same swimmer "just quit the program for some reason and then
        wanted back in right away. He shouldn't have to replug the stick."
        Uses udisksctl, which the desktop user may run without a password.
        Removable disks only (/sys/block/<disk>/removable), never the SD card.
        """
        for removable_path in glob.glob("/sys/block/sd*/removable"):
            try:
                with open(removable_path) as f:
                    if f.read().strip() != "1":
                        continue
                disk = "/dev/" + removable_path.split("/")[3]
                out = subprocess.run(["lsblk", "-rpno", "PATH,FSTYPE,MOUNTPOINT", disk],
                                     capture_output=True, text=True, timeout=5).stdout
            except Exception:
                continue
            for line in out.splitlines():
                parts = line.split(" ")
                if len(parts) < 2 or not parts[1] or (len(parts) > 2 and parts[2]):
                    continue           # no filesystem, or already mounted
                try:
                    r = subprocess.run(["udisksctl", "mount", "-b", parts[0],
                                        "--no-user-interaction"],
                                       capture_output=True, text=True, timeout=15)
                    print("USB stick mount:", (r.stdout or r.stderr).strip())
                except Exception as e:
                    print("USB stick mount failed:", e)

    def _find_individual_defaults(self):
        """
        Scans mounted USB drives for a poolwind_ind_defaults.txt at their
        root (after mounting any stick left unmounted at the last close).
        Returns (dict, usb_root_dir), or (None, None) if no
        recognized swimmer's stick is present.
        """
        self._mount_usb_sticks()
        matches = sorted(glob.glob("/media/*/*/poolwind_ind_defaults.txt"))
        if not matches:
            return None, None
        if len(matches) > 1:
            print(f"Multiple individual defaults files found {matches}; using {matches[0]}")
        ind_path = matches[0]
        try:
            with open(ind_path, "r") as f:
                ind_defaults = ast.literal_eval(f.read())
        except Exception as e:
            print("Error loading individual defaults file:", e)
            return None, None
        self._ind_path = ind_path
        self._ind_mtime = os.path.getmtime(ind_path)
        return ind_defaults, os.path.dirname(ind_path)

    def _find_unconfigured_usb_drive(self):
        """
        Looks for a mounted, removable USB drive that has no
        poolwind_ind_defaults.txt at its root (i.e. not already a
        recognized swimmer's stick). Returns (mount_path, size_bytes) for
        the first one found, or None. Removability is confirmed via
        /sys/block/<disk>/removable so this can never match the Pi's own
        SD card even if the /media scan logic has a bug.
        """
        for mount_path in sorted(glob.glob("/media/*/*")):
            if not os.path.isdir(mount_path):
                continue
            if os.path.isfile(os.path.join(mount_path, "poolwind_ind_defaults.txt")):
                continue
            try:
                src = subprocess.run(
                    ["findmnt", "-no", "SOURCE", mount_path],
                    capture_output=True, text=True, timeout=5
                ).stdout.strip()
                if not src:
                    continue
                disk = re.sub(r'\d+$', '', os.path.basename(src))
                with open(f"/sys/block/{disk}/removable") as f:
                    removable = f.read().strip()
                if removable != "1":
                    continue
            except Exception:
                continue

            try:
                size_bytes = shutil.disk_usage(mount_path).total
            except Exception:
                size_bytes = 0
            return mount_path, size_bytes
        return None

    def _offer_usb_drive_setup(self):
        """
        If an unconfigured removable drive is present, prompt to format
        and set it up as a new swimmer's personal stick.
        """
        candidate = self._find_unconfigured_usb_drive()
        if candidate is None:
            return
        mount_path, size_bytes = candidate

        slow_pace, fast_pace = self.REPdefaults["PaceLimitsDec"]
        dlg = USBDriveSetupDialog(mount_path, size_bytes, default_min_pace=fast_pace, default_max_pace=slow_pace)
        if dlg.exec() != QDialog.Accepted:
            return

        name, height, min_pace, max_pace = dlg.get_values()
        self._format_and_setup_usb_drive(mount_path, name, height, min_pace, max_pace)

    def _format_and_setup_usb_drive(self, mount_path, name, height, min_pace, max_pace):
        """
        Quick-formats the drive at mount_path as exFAT, labels it from
        `name`, and writes a fresh poolwind_ind_defaults.txt -- then
        applies it immediately (no restart needed), the same way a
        pre-existing stick's file would be applied at startup.
        """
        try:
            device = subprocess.run(
                ["findmnt", "-no", "SOURCE", mount_path],
                capture_output=True, text=True, timeout=5
            ).stdout.strip()
            if not device:
                raise RuntimeError(f"Could not resolve the device for {mount_path}")

            disk = re.sub(r'\d+$', '', os.path.basename(device))
            with open(f"/sys/block/{disk}/removable") as f:
                removable = f.read().strip()
            if removable != "1":
                raise RuntimeError(f"{device} is not a removable drive -- refusing to format")

            # exFAT labels: keep it short/plain -- matches the length that
            # proved reliable across tools during earlier testing.
            label = re.sub(r'[^A-Za-z0-9_]', '', name).upper()[:11]
            if not label:
                label = "SWIMMER"

            subprocess.run(["sudo", "umount", mount_path], check=True, timeout=15)
            subprocess.run(["sudo", "mkfs.exfat", "-n", label, device], check=True, timeout=60)

            # The logged-in user's own media folder and IDs (not fixed to
            # 'poolwind' / 1000), so other builders' Pis work too.
            new_mount_path = os.path.join(os.path.dirname(mount_path), label)
            subprocess.run(["sudo", "mkdir", "-p", new_mount_path], check=True, timeout=10)
            subprocess.run(
                ["sudo", "mount", "-t", "exfat", "-o",
                 f"uid={os.getuid()},gid={os.getgid()},umask=000",
                 device, new_mount_path],
                check=True, timeout=15
            )

            ind_defaults = {
                self.KEY_HEIGHT: height,
                self.KEY_PACE: (Utils.DecimalToTime(max_pace), Utils.DecimalToTime(min_pace)),
                self.KEY_RECORD: self.REPdefaults[self.KEY_RECORD],
                # (no algorithm line: a developer choice since 2026-10-17)
                self.KEY_LOGRATE: self.REPdefaults[self.KEY_LOGRATE],
                self.KEY_EJECT: bool(self.REPdefaults.get(self.KEY_EJECT, True)),
            }
            ind_path = os.path.join(new_mount_path, "poolwind_ind_defaults.txt")
            with open(ind_path, "w") as f:
                f.write("# These are the individual user settings and will\n"
                        "# override the system settings while this stick is inserted.\n"
                        "{\n")
                for n, (key, value) in enumerate(ind_defaults.items()):
                    f.write(f"\n{'' if n == 0 else ','}'{key}': {value!r}\n")
                f.write("}\n")
            self._ind_path = ind_path
            self._ind_mtime = os.path.getmtime(ind_path)

            self._apply_individual_defaults(ind_defaults)
            self.usb_data_dir = new_mount_path
            self._stick_root = new_mount_path
            self.data_dir = os.path.join(new_mount_path, "CSV Vault")
            os.makedirs(self.data_dir, exist_ok=True)

            QMessageBox.information(
                None, "USB Drive Ready",
                f"'{label}' is formatted and set up. Swim data will be saved there."
            )

        except Exception as e:
            QMessageBox.critical(
                None, "USB Setup Failed",
                f"Could not set up the drive:\n{e}\n\n"
                "It may be left unformatted or partially set up -- check it before reuse."
            )

    # ---------------------------------------------------------------
    # User settings (since v7.44): the SAME names in the main defaults
    # file and on a swimmer's USB stick; the stick's values win.
    #   'swimmersHeight': 72                        (inches)
    #   'paceMin, Max': ('5:00', '1:42')            (min/100 yd, either order)
    #   'usablePoolLength': 162     (inches, back wall to the jet unit's edge;
    #                                calibration file only -- it belongs to
    #                                the pool; was 'poolLength' until v15.3)
    #   'recordTrainingVideo': False
    #   'algorithm (basic or swimmerPace)': 'swimmerPace'
    #   'logRate': 5        (rows + video frames per second, read at start)
    # The program works with internal keys DERIVED from these after every
    # load / reload: REPdefaults['PaceLimitsDec'] = (slow, fast) decimal
    # minutes and REPdefaults['swimmersHeight,usablePoolLength'] = (height, length).
    # Older names are still accepted (OLD_SETTING_NAMES). The program never
    # writes the main defaults file, so comments in it are kept.
    # ---------------------------------------------------------------
    KEY_PACE        = "paceMin, Max"
    KEY_HEIGHT      = "swimmersHeight"
    KEY_POOL_LENGTH = "usablePoolLength"
    KEY_RECORD      = "recordTrainingVideo"
    KEY_ALGO        = "algorithm (basic or swimmerPace)"
    KEY_LOGRATE     = "logRate"         # built in: 5
    KEY_EJECT       = "ejectStickOnClose"   # built in: True
    LOG_RATE_RANGE  = (1, 15)           # rows (and video frames) per second
    STICK_KEYS      = (KEY_HEIGHT, KEY_PACE, KEY_RECORD, KEY_LOGRATE,
                       KEY_EJECT)       # (algorithm: main file only, 2026-10-17)
    OLD_SETTING_NAMES = {
        "defaultPaceMin, Max":              KEY_PACE,
        "PaceLimitsDec":                    KEY_PACE,      # decimal minutes, e.g. (5, 1.5)
        "defaultSwimmersHeight":            KEY_HEIGHT,
        "defaultRecordTrainingVideo":       KEY_RECORD,
        "Algorithm (basic or swimmerPace)": KEY_ALGO,
        "defLogRate":                       KEY_LOGRATE,   # briefly used in v15.1
        "log recs per sec":                 KEY_LOGRATE,
        "poolLength":                       KEY_POOL_LENGTH,   # until v15.3
    }

    @classmethod
    def _rename_old_settings(cls, settings):
        """A settings dict with older names changed to the current ones
        (a current name already present wins)."""
        out = dict(settings)
        if "swimmersHeight,poolLength" in out:      # oldest form: one (height, length) pair
            h, length = out.pop("swimmersHeight,poolLength")
            out.setdefault(cls.KEY_HEIGHT, h)
            out.setdefault(cls.KEY_POOL_LENGTH, length)
        for old, new in cls.OLD_SETTING_NAMES.items():
            if old in out:
                value = out.pop(old)
                out.setdefault(new, value)
        return out

    @staticmethod
    def _parse_pace(value):
        """'5:00' -> 5.0, '1:42' -> 1.7; plain numbers (5, 1.7) pass through."""
        if isinstance(value, str):
            text = value.strip()
            if ":" in text:
                m, sec = text.split(":", 1)
                return int(m) + float(sec) / 60.0
            return float(text)
        return float(value)

    @classmethod
    def _pace_limits(cls, value):
        """Two paces in either order -> (slowest, fastest) in decimal minutes."""
        a, b = (cls._parse_pace(v) for v in value)
        return (max(a, b), min(a, b))

    def _derive_internal_defaults(self, defaults):
        """Returns REPdefaults: the settings plus the derived internal keys."""
        rep = dict(defaults)
        rep["PaceLimitsDec"] = self._pace_limits(defaults[self.KEY_PACE])
        rep["swimmersHeight,usablePoolLength"] = (defaults.get(self.KEY_HEIGHT, 72),
                                            defaults.get(self.KEY_POOL_LENGTH, 162))
        rep[self.KEY_RECORD] = bool(defaults.get(self.KEY_RECORD, False))
        return rep

    def _apply_individual_defaults(self, ind_defaults):
        """Overlay one swimmer's USB-stick settings onto REPdefaults."""
        ind = self._rename_old_settings(ind_defaults)
        if self.KEY_POOL_LENGTH in ind:
            print("usablePoolLength on the USB stick is ignored (it belongs to the pool: calibration file)")
        if self.KEY_PACE in ind:
            self.REPdefaults[self.KEY_PACE] = ind[self.KEY_PACE]
            self.REPdefaults["PaceLimitsDec"] = self._pace_limits(ind[self.KEY_PACE])
            if hasattr(self, "PaceLimitsDec"):      # after startup: keep the cached copy in step
                self.PaceLimitsDec = self.REPdefaults["PaceLimitsDec"]
        if self.KEY_HEIGHT in ind:
            _, usablePoolLength = self.REPdefaults["swimmersHeight,usablePoolLength"]
            self.REPdefaults[self.KEY_HEIGHT] = ind[self.KEY_HEIGHT]
            self.REPdefaults["swimmersHeight,usablePoolLength"] = (ind[self.KEY_HEIGHT], usablePoolLength)
        if self.KEY_RECORD in ind:
            self.REPdefaults[self.KEY_RECORD] = bool(ind[self.KEY_RECORD])
        if self.KEY_ALGO in ind:
            print("algorithm on the USB stick is ignored (a developer setting: main defaults file only)")
        if self.KEY_LOGRATE in ind:              # used at program start
            self.REPdefaults[self.KEY_LOGRATE] = ind[self.KEY_LOGRATE]
        if self.KEY_EJECT in ind:                # used at close
            self.REPdefaults[self.KEY_EJECT] = bool(ind[self.KEY_EJECT])
        self._ind_defaults = dict(ind_defaults)

    # ---------------------------------------------------------------
    # Calibration file (since v7.44): <program name>_calibration.txt
    # Pool/installation data that the program and the calibration tool
    # write -- not the user. SAFETY-CRITICAL: pace_voltage and
    # SafetyVoltageLimits decide which voltages the jet is driven to.
    # Read at startup only. Set Swim Area writes swimAreaPoints right away
    # when Save is pressed -- in camera mode only; in video mode the test
    # video's points live in the code. Same Python-dictionary format as
    # the defaults file.
    # ---------------------------------------------------------------
    CAL_KEYS = ("pace_voltage", "SafetyVoltageLimits", "swimAreaPoints",
                "usablePoolLength", "middleSwimZone %", "recordRawVideo")
    # Entries added after the file format first appeared: taken over from
    # the defaults file (where they lived before) or these values.
    CAL_FALLBACKS = {"usablePoolLength": 162, "middleSwimZone %": 35, "recordRawVideo": False}
    CAL_REQUIRED = ("pace_voltage", "SafetyVoltageLimits", "swimAreaPoints")
    OLD_CAL_KEYS = ("cameraSwimAreaPoints", "videoSwimAreaPoints")   # before v7.44: one per source
    OLD_CAL_NAMES = {"poolLength": "usablePoolLength"}               # renamed in v15.3

    def _load_calibration(self):
        """
        Returns the calibration dict. If the file doesn't exist yet, it is
        created from the same entries in the defaults file (how they were
        stored before v7.44). Exits if the pace table or safety limits
        can't be found -- the jet must never run without them.
        """
        if os.path.isfile(self.calibration_path):
            try:
                with open(self.calibration_path, "r") as f:
                    cal = ast.literal_eval(f.read())
            except Exception as e:
                print("Error loading calibration file:", self.calibration_path, e)
                sys.exit()
            changed = self._convert_old_swim_area(cal)
            changed = self._rename_old_cal_keys(cal) or changed
            for key, fallback in self.CAL_FALLBACKS.items():
                if key not in cal:           # was in the defaults file (or built in) before
                    cal[key] = self._defaults_file_value(key, fallback)
                    changed = True
            if changed:
                self.calibration = cal
                self.save_calibration()
        else:
            try:
                with open(self.defaults_path, "r") as f:
                    old = ast.literal_eval(f.read())
            except Exception:
                old = {}
            cal = {k: old[k] for k in self.CAL_KEYS + self.OLD_CAL_KEYS
                   + tuple(self.OLD_CAL_NAMES) if k in old}
            self._rename_old_cal_keys(cal)
            self._convert_old_swim_area(cal)
            for key, fallback in self.CAL_FALLBACKS.items():
                cal.setdefault(key, fallback)
            if all(k in cal for k in self.CAL_REQUIRED):
                self.calibration = cal
                self.save_calibration()
                print("Calibration file created from the defaults file:", self.calibration_path)
        missing = [k for k in self.CAL_REQUIRED if k not in cal]
        if missing:
            print("Calibration file", self.calibration_path, "is missing", ", ".join(missing),
                  "-- the jet can't be driven safely without it. Exiting.")
            sys.exit()
        return cal

    def _defaults_file_value(self, key, fallback):
        """One entry straight from the defaults file (for moving it over)."""
        try:
            with open(self.defaults_path, "r") as f:
                return ast.literal_eval(f.read()).get(key, fallback)
        except Exception:
            return fallback

    def _rename_old_cal_keys(self, cal):
        """Older calibration names changed to the current ones (the file
        is then saved with the new name). Returns True if anything changed."""
        changed = False
        for old, new in self.OLD_CAL_NAMES.items():
            if old in cal:
                value = cal.pop(old)
                cal.setdefault(new, value)
                changed = True
        return changed

    def _convert_old_swim_area(self, cal):
        """The camera's area becomes swimAreaPoints; the video one is
        dropped. Returns True if anything changed."""
        if not any(k in cal for k in self.OLD_CAL_KEYS):
            return False
        camera = cal.pop("cameraSwimAreaPoints", None)
        cal.pop("videoSwimAreaPoints", None)
        if "swimAreaPoints" not in cal and camera is not None:
            cal["swimAreaPoints"] = camera
        return True

    def save_calibration(self):
        """Writes self.calibration (written to a temporary file first, so a
        power cut can't leave a half-written file)."""
        lines = [
            "# PoolWind calibration -- SAFETY-CRITICAL, technician changes only.",
            "# Written by the program (Set Swim Area) and the calibration tool.",
            "# pace_voltage: (pace min/100 yd, Pace Display volts) measured on this",
            "# pool. SafetyVoltageLimits: the jet is never driven outside these volts.",
            "# swimAreaPoints: the swim area's corners in the camera picture (Set",
            "# Swim Area). usablePoolLength: the swim area's length in inches, from the back",
            "# wall to the jet unit's edge (not the whole pool). middleSwimZone %: the",
            "# center lane's width, side to side, as a percent of the swim area.",
            "# recordRawVideo: record the camera's full, uncorrected video (large",
            "# files) -- developer tool, used only when developerMode is on.",
            "# Read at program start.",
            "{",
        ]
        items = [(k, self.calibration[k]) for k in self.CAL_KEYS if k in self.calibration]
        items += [(k, v) for k, v in self.calibration.items() if k not in self.CAL_KEYS]
        for n, (key, value) in enumerate(items):
            lead = "" if n == 0 else ","
            if key == "pace_voltage":
                rows = ",\n".join(f"    {tuple(r)!r}" for r in value)
                lines.append(f"{lead}'{key}': [\n{rows}\n]")
            else:
                lines.append(f"{lead}'{key}': {value!r}")
            lines.append("")
        lines.append("}")
        tmp = self.calibration_path + ".tmp"
        with open(tmp, "w") as f:
            f.write("\n".join(lines) + "\n")
        os.replace(tmp, self.calibration_path)
        print("Calibration saved to", self.calibration_path)

    DEVELOPER_KEYS = ("workplace (home or pool or default)", "capture_device (camera or video)",
                      "display_device (work or pool)", "Valve (real or simulate)")

    def _read_defaults_file(self):
        """
        Reads the defaults file (older setting names changed to the current
        ones) and returns its entries laid over BUILT_IN_DEFAULTS, with the
        calibration on top and the workplace switch applied.
        """
        with open(self.defaults_path, 'r') as f:
            file_defaults = self._rename_old_settings(ast.literal_eval(f.read()))
        defaults = dict(BUILT_IN_DEFAULTS)
        defaults.update(file_defaults)
        stale = [k for k in self.CAL_KEYS + self.OLD_CAL_KEYS if k in file_defaults]
        if stale:
            print("Defaults file entries ignored (the calibration file holds them):", ", ".join(stale))
        for k in self.OLD_CAL_KEYS:
            defaults.pop(k, None)
        defaults.update(self.calibration)
        # Users (developerMode off): always the real pool setup, whatever
        # the file says.
        if not defaults["developerMode"]:
            for k in self.DEVELOPER_KEYS:
                defaults[k] = BUILT_IN_DEFAULTS[k]
            return defaults
        # The workplace switch only acts when the file has a workplace line;
        # otherwise the device settings (built-in or from the file) stand.
        _wp = file_defaults.get("workplace (home or pool or default)")
        if _wp == "pool":
            defaults["capture_device (camera or video)"] = "camera"
            defaults["display_device (work or pool)"]    = "pool"
            defaults["Valve (real or simulate)"]         = "real"
        elif _wp == "home":
            defaults["capture_device (camera or video)"] = "video"
            defaults["display_device (work or pool)"]    = "work"
            defaults["Valve (real or simulate)"]         = "simulate"
        return defaults

    def takeReading(self):
        """
        Returns the EMA-smoothed valve voltage (used for pool_pace and the
        relay drive). Also sets self.raw_voltage, the unsmoothed 5-read
        average (logged in the pace trace).
        """
        if self.valveOption == "simulate":
            self.valve.sim_update()
            self.raw_voltage = self.valve.sim_takeReading()
            return self.raw_voltage

        # --- REAL HARDWARE MODE ---
        total = 0.0
        good = 0

        # Take 5 readings for smoothing (a failed read is skipped, not
        # counted as 0 V -- the raw voltage would show that as a fake step)
        for _ in range(5):
            try:
                total += float(self.ina260.voltage)
                good += 1
            except Exception:
                pass

        if good:
            avgVolts = total / good
        else:
            avgVolts = self.raw_voltage if self.raw_voltage else 0.0
        self.raw_voltage = avgVolts

        # ----- EMA smoothing -----
        alpha = 0.1   # good starting point

        if self.ema_voltage is None:
            self.ema_voltage = avgVolts
        else:
            self.ema_voltage = alpha * avgVolts + (1 - alpha) * self.ema_voltage

        return round(self.ema_voltage, 3)

    def _write_pace_trace(self, timestamp, valveVoltage, raw_pace):
        """
        Developer trace (since 2026-09-21): one row per loop pass --
        voltage, pool pace, raw CoM, estimator internals, target step and
        relay -- for studying the jet control and the swim-pace estimator
        offline (none of this is in the swim log). Written only while
        'paceTrace' is True (built in False; switch it in the defaults file,
        live). About 15 MB per hour of swimming. Never allowed to break the
        app.
        """
        if not self.REPdefaults.get("paceTrace", False):
            f = getattr(self, "_pace_trace_f", None)
            if f is not None:             # switched off while running
                try:
                    f.close()
                except Exception:
                    pass
                self._pace_trace_f = None
            return
        try:
            if getattr(self, "_pace_trace_f", None) is None:
                path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "pace_trace_" + time.strftime("%Y-%m-%d_%H%M%S") + ".csv")
                self._pace_trace_f = open(path, "w", buffering=1)
                self._pace_trace_f.write(
                    "t,voltage,raw_pace,pool_pace,v_water_lag,blob_h,CoM_h_corr,"
                    "swimmerFound,logDistance,v_drift,swim_pace_est,swim_pace,"
                    "raw_voltage,target_idx,relay\n")
            blob_h = getattr(self.window, "blob_CoM_h", None)
            self._pace_trace_f.write(
                f"{timestamp:.3f},{valveVoltage:.3f},{raw_pace:.4f},{self.pool_pace:.4f},"
                f"{getattr(self, '_trace_v_water', 0.0):.3f},"
                f"{'' if blob_h is None else f'{blob_h:.1f}'},"
                f"{self.window.CoM_h},{int(bool(getattr(self.window, 'swimmerFound', False)))},"
                f"{int(bool(getattr(self.window, 'logDistance', False)))},"
                f"{getattr(self, '_trace_v_drift', 0.0):.3f},"
                f"{getattr(self, '_trace_est', 0.0):.4f},{self.swim_pace:.4f},"
                f"{self.raw_voltage:.4f},{self.desiredIndex},{self.currentDirection}\n")
        except Exception:
            pass

    def updateVoltageAndPace(self, valveVoltage, timestamp):
        """
        pool_pace = pace derived from valveVoltage (EMA-smoothed) → used for control.
        Infrastructure only -- swim_pace now comes from the selected
        algorithm (SwimController.runAlgorithm). Returns the unsmoothed
        raw pace for the trace.
        """

        # ------------------------------------------------------------
        # 1. Convert valveVoltage → raw pace (controller interpolation)
        # ------------------------------------------------------------
        raw_pace = self.controller._get_pace_from_voltage(valveVoltage)

        # ------------------------------------------------------------
        # 2. Update pool_pace (EMA smoothing stays exactly as before)
        # ------------------------------------------------------------
        if self._ema_pool_pace is None:
            self._ema_pool_pace = raw_pace
        else:
            a = self.PACE_ALPHA
            self._ema_pool_pace = a * raw_pace + (1 - a) * self._ema_pool_pace

        self.pool_pace = self._ema_pool_pace
        return raw_pace

    def _update_pace_display(self, timestamp):
        """PaceDisplay (swim_pace) updated only once per second, rounded to 0.05."""
        if not hasattr(self, "_last_disp_update"):
            self._last_disp_update = 0

        if timestamp - self._last_disp_update >= 1.0:
            self._last_disp_update = timestamp

            # Hold UP/DN: show the new step's pace until the real one is
            # within ANTICIPATE_CATCHUP of it (or Hold ends, or it times out)
            pace = self.swim_pace
            ant = getattr(self, "_anticipated_pace", None)
            if ant is not None:
                if (not self.hold_mode or timestamp > self._anticipate_until
                        or abs(self.swim_pace - ant) <= self.ANTICIPATE_CATCHUP):
                    self._anticipated_pace = None
                else:
                    pace = ant

            # Round to nearest 0.05 for stable display
            rounded_pace = round(pace * 20) / 20.0

            self.PaceDisplay = Utils.DecimalToTime(rounded_pace)

    def findClosestPlateauIndex(self, voltage, noiseAllowedPercent, plateau):
        """
        Convert a noisy voltage into a stable plateau index using:
        - noiseAllowed% of plateau width
        - sliding miniPlateau
        - overLap% intrusion threshold

        NOTE (2026-10-16): despite the "Schmitt trigger" comment below, this
        has no memory of the step it chose last time, so it is not
        hysteresis: it is nearest-step with the edges between steps moved a
        little where the steps are unevenly spaced (with the valve's 0.15 it
        differs from plain nearest-step at 11 of 6576 test voltages across
        the calibration table). It is steady in practice because the jet
        parks on its steps and the voltage is EMA-smoothed. It drives the
        relays (_hold_drive), so it is left as it is; the swim zone
        highlight has real hysteresis of its own (SwimController.jet_zone).
        """

        lastIndex = len(plateau) - 1

        # ------------------------------------------------------------
        # 1. Find the exact plateau index (closest center)
        # ------------------------------------------------------------
        exactIndex = min(
            range(len(plateau)),
            key=lambda i: abs(voltage - plateau[i])
        )

        # ------------------------------------------------------------
        # 2. Compute plateau width around exactIndex
        # ------------------------------------------------------------
        if exactIndex == 0:
            width = plateau[1] - plateau[0]
        elif exactIndex == lastIndex:
            width = plateau[lastIndex] - plateau[lastIndex - 1]
        else:
            width = (plateau[exactIndex + 1] - plateau[exactIndex - 1]) / 2

        # ------------------------------------------------------------
        # 3. Convert noiseAllowed% into volts
        # ------------------------------------------------------------
        noiseVolts = width * noiseAllowedPercent

        # ------------------------------------------------------------
        # 4. Build the sliding miniPlateau
        # ------------------------------------------------------------
        miniLower = voltage - noiseVolts / 2
        miniUpper = voltage + noiseVolts / 2

        # ------------------------------------------------------------
        # 5. Apply overLap threshold (Schmitt trigger)
        # ------------------------------------------------------------
        overLap = 0.75   # 75% intrusion required to switch plateau

        # Check upward neighbor
        if exactIndex < lastIndex:
            nextCenter = plateau[exactIndex + 1]
            boundaryToNext = nextCenter - plateau[exactIndex]
            intrusionUp = miniUpper - plateau[exactIndex]

            if intrusionUp > overLap * boundaryToNext:
                return exactIndex + 1

        # Check downward neighbor
        if exactIndex > 0:
            prevCenter = plateau[exactIndex - 1]
            boundaryToPrev = plateau[exactIndex] - prevCenter
            intrusionDown = plateau[exactIndex] - miniLower

            if intrusionDown > overLap * boundaryToPrev:
                return exactIndex - 1

        # ------------------------------------------------------------
        # 6. Otherwise stay on the original plateau
        # ------------------------------------------------------------
        return exactIndex

    def Suspend_btn_press(self):
        """
        Toggle between Suspend/Resume/Begin states.
        """
        if self.suspendButtonText in ("Begin", "Resume"):
            self.suspendButtonText = "Suspend"
            self.firstTime = False
        else:
            self.suspendButtonText = "Resume"

    def UP_relay(self): 
        if self.valveOption == "simulate":
            self.valve.sim_UP_relay_on()
        else:
            # Safety: never allow both relays active
            self.GPIO.output(self.PIN_DN, True)   # force DN off first
            self.GPIO.output(self.PIN_UP, False)  # energize UP
        self.currentDirection = "UP"

    def DN_relay(self):
        if self.valveOption == "simulate":
            self.valve.sim_DN_relay_on()
        else:
            # Safety: never allow both relays active
            self.GPIO.output(self.PIN_UP, True)   # force UP off first
            self.GPIO.output(self.PIN_DN, False)  # energize DN
        self.currentDirection = "DN"

    def relay_off(self):
        if self.valveOption == "simulate":
            self.valve.sim_relay_off()
        else:
            self.GPIO.output(self.PIN_UP, True)
            self.GPIO.output(self.PIN_DN, True)
            # why turn off pump? self.GPIO.output(self.PIN_PUMP, True)
        self.currentDirection = "LEVEL"

    def View_btn_press(self):
        if self.view_mode == 1:
            self.view_mode = 2
        elif self.view_mode == 2:
            self.view_mode = 3
        elif self.view_mode == 3:
            self.view_mode = 4
        else: self.view_mode = 1

    def Hold_btn_press(self):
        self.hold_mode = not self.hold_mode

        if self.hold_mode:
            # Freeze CoM_h at the last value seen while genuinely
            # auto-tracking (not the live value, which may already be
            # wind-down-decayed toward neutral if the swimmer left the
            # zone a while before walking over to press this button).
            # CoM_w is never frozen — it always tracks live blob detection.
            self.frozen_CoM_h = max(0.0, min(1000.0, self.window.last_real_CoM_h))
        else:
            # Returning to normal: the wind-down EMA was left frozen at
            # whatever it was right before Hold was first pressed, not
            # at the (possibly manually-adjusted) value CoM_h was just
            # held at. Resync it here so un-holding decays smoothly from
            # the held value instead of jumping back to that stale one.
            self.window.EMA_CoM_h = self.frozen_CoM_h

    # Hold mode, UP/DN: one jet step per press, repeated this often while
    # the button is held. The large Pace display shows the new step's pace
    # straight away (anticipated) until the real pace catches up.
    HOLD_STEP_REPEAT_S    = 1.0
    ANTICIPATE_CATCHUP    = 0.05    # min/100 yd: "caught up" when this close
    ANTICIPATE_TIMEOUT_S  = 20.0    # give up anticipating after this long

    def step_held_zone(self, direction):
        """Move the held position one zone (= one jet step) up or down,
        to the middle of that zone, never outside the pool."""
        n = len(self.controller._zone_steps())
        k = int(max(0.0, min(999.999, self.frozen_CoM_h)) / 1000.0 * n)
        k = max(0, min(n - 1, k + direction))
        self.frozen_CoM_h = (k + 0.5) * 1000.0 / n
        steps = self.controller._zone_steps()
        self._anticipated_pace = self.speedArray[steps[k]][0]
        self._anticipate_until = time.time() + self.ANTICIPATE_TIMEOUT_S
        self._last_disp_update = 0      # show it now, not at the next 1 s update

    def DN_btn_press(self, event=None):
        self.manual_direction = "DN"
        self._hold_first_step("DN")

    def UP_btn_press(self, event=None):
        self.manual_direction = "UP"
        self._hold_first_step("UP")

    def _hold_first_step(self, btn):
        """Hold mode: the first step happens on the touch itself, so even a
        tap shorter than one screen refresh counts; the screen refresh
        repeats it while the button stays held."""
        if self.hold_mode:
            self.step_held_zone(+1 if btn == "UP" else -1)
            self.window._hold_step_btn = btn
            self.window._hold_step_next = time.time() + self.HOLD_STEP_REPEAT_S

    # OnOff sequence timing. The relays press buttons on the pool's radio
    # remote, which can't send two buttons at once -- so UP/DN is released
    # first and the jet drive stays hands-off for the whole sequence.
    PUMP_PRE_DELAY_MS  = 300    # after releasing UP/DN, before pressing OnOff
    PUMP_PULSE_MS      = 2000   # OnOff held this long
    PUMP_POST_DELAY_MS = 500    # after releasing OnOff, before UP/DN may resume

    # Pump buttons off the main screen ask first (Bill, 2026-10-17: "they
    # are too easy to press ... a message pop up like: 'Are you sure? This
    # will toggle the pump on or off - OK, Cancel'"). The pool screen's
    # OnOff stays one touch, for emergencies. All pump buttons are tinted
    # a light red (PUMP_BTN_*).
    PUMP_BTN_BGR = (185, 185, 225)                  # pool screen (OpenCV, BGR)
    # Qt buttons, same tint. The border is needed: the Pi desktop's button
    # style ignores a background colour on its own (seen 2026-10-17).
    PUMP_BTN_STYLE = ("QPushButton { background-color: #e1b9b9; border: 1px solid #9c7c7c;"
                      " border-radius: 3px; padding: 5px; }"
                      " QPushButton:pressed { background-color: #c99d9d; }")

    def OnOff_confirm(self, parent=None):
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle("Pump On/Off")
        box.setText("Are you sure? This will turn the pool's pump on or off.")
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Cancel)
        if box.exec() == QMessageBox.Ok:
            self.OnOff_btn_press()

    def OnOff_btn_press(self):
        # Momentary pulse on Qt timers (mouse-release is not wired to any
        # button action, so we can't rely on btn_release() here). Takes
        # priority over the jet drive: UpdateLoop skips _hold_drive while
        # _pump_pulsing is set.
        if getattr(self, "_pump_pulsing", False):
            return  # ignore repeat presses while a pulse is in progress
        self._pump_pulsing = True
        self.relay_off()                         # let go of UP/DN first
        QTimer.singleShot(self.PUMP_PRE_DELAY_MS, self._pump_pulse_start)

    def _pump_pulse_start(self):
        self.relay_off()                         # still nothing else pressed
        self.GPIO.output(self.PIN_PUMP, False)   # False = ON, True = OFF
        QTimer.singleShot(self.PUMP_PULSE_MS, self._pump_pulse_release)

    def _pump_pulse_release(self):
        self.GPIO.output(self.PIN_PUMP, True)   # False = ON, True = OFF
        QTimer.singleShot(self.PUMP_POST_DELAY_MS, self._pump_pulse_done)

    def _pump_pulse_done(self):
        self._pump_pulsing = False

    def btn_release(self, event=None):
        self.manual_direction = "LEVEL"
        self.GPIO.output(self.PIN_PUMP, True)   # False = ON, True = OFF

    def shutdown(self):
        self.systemShutdown = True
        if getattr(self, "_already_shutdown", False):
            return
        self._already_shutdown = True

        print("Shutting down system...")

        # ------------------------------------------------------------
        # 0. Stop timers FIRST (prevents Qt from staying alive)
        # ------------------------------------------------------------
        try:
            if hasattr(self, "window") and hasattr(self.window, "logic_timer"):
                self.window.logic_timer.stop()
        except:
            pass

        try:
            if hasattr(self, "window") and hasattr(self.window, "video_timer"):
                self.window.video_timer.stop()
        except:
            pass

        # ------------------------------------------------------------
        # 1. Wind down pool voltage
        # ------------------------------------------------------------
        self.initial_voltage_winddown()

        # ------------------------------------------------------------
        # 2. TURN OFF ALL RELAYS
        # ------------------------------------------------------------
        try:
            self.relay_off()
        except Exception:
            pass

        # ------------------------------------------------------------
        # 3. CLOSE QT WINDOW (if still open)
        # ------------------------------------------------------------
        try:
            if hasattr(self, "window") and self.window is not None:
                self.window.close()
        except Exception:
            pass

        # (4. The defaults file is never written by the program since
        #     v7.44 -- the swim area is saved in the calibration file.)

        # ------------------------------------------------------------
        # 5. FORCE RELEASE OF VIDEO WRITERS (CRITICAL!)
        # ------------------------------------------------------------
        try:
            if self.myVideoCapture.raw_writer is not None:
                self.myVideoCapture.raw_writer.release()
                self.myVideoCapture.raw_writer = None
        except:
            pass

        try:
            if self.myVideoCapture.persp_writer is not None:
                self.myVideoCapture.persp_writer.release()
                self.myVideoCapture.persp_writer = None
        except:
            pass

        # ------------------------------------------------------------
        # 6. CLEAN UP GPIO
        # ------------------------------------------------------------
        try:
            self.GPIO.cleanup()
        except Exception:
            pass

        # ------------------------------------------------------------
        # 7. Compress RAW video (background, safe, non-blocking)
        # ------------------------------------------------------------
        rawfile = getattr(self.myVideoCapture, "raw_filename", None)

        if rawfile and os.path.exists(rawfile):
            outfile = rawfile + ".mp4"
            self.launch_background_compressor(rawfile, outfile)
            print("Background compression started.")
        else:
            print("No RAW file to compress.")

        # ------------------------------------------------------------
        # 7b. Pace sanity-check log (see poolwindAI_v7.39_pace_notes.txt
        #     section 5) -- avg(swim_pace) should converge to
        #     avg(pool_pace) over a full session; a persistent gap points
        #     at the drift gain/cap or the pace clamp, not a broken
        #     premise.
        # ------------------------------------------------------------
        n = getattr(self, "_pace_check_n", 0)
        if n > 0:
            avg_pool = self._pace_check_sum_pool / n
            avg_swim = self._pace_check_sum_swim / n
            calls = getattr(self, "_pace_check_estimator_calls", 0)
            capped = getattr(self, "_pace_check_drift_capped", 0)
            clamped = getattr(self, "_pace_check_pace_clamped", 0)
            capped_pct = (100.0 * capped / calls) if calls else 0.0
            clamp_pct = (100.0 * clamped / calls) if calls else 0.0
            print(
                f"[Pace sanity check] samples={n}  "
                f"avg pool_pace={avg_pool:.3f}  avg swim_pace={avg_swim:.3f}  "
                f"diff={avg_swim - avg_pool:+.3f}  "
                f"drift-capped={capped}/{calls} ({capped_pct:.1f}%)  "
                f"pace-clamped={clamped}/{calls} ({clamp_pct:.1f}%)"
            )
        else:
            print("[Pace sanity check] no pace samples logged this session.")

        # ------------------------------------------------------------
        # 7c. The swimmer's USB stick: eject it the OS way, so nothing
        #     is left waiting to be written (Linux can hold writes for
        #     up to 30 s) and it can be pulled at once. Bill, 2026-10-17:
        #     "eject every time with the developer setting", and a
        #     closing message for each case.
        # ------------------------------------------------------------
        self._close_stick()

        print("Shutdown complete.")

        # ------------------------------------------------------------
        # 8. EXIT PROGRAM IMMEDIATELY
        # ------------------------------------------------------------
        sys.exit(0)

    # ------------------------------------------------------------------
    # USB stick eject (since v15.2)
    # ------------------------------------------------------------------
    def _eject_stick(self, root):
        """
        Make the stick mounted at `root` safe to remove: write everything
        and unmount it (gio -> udisks). Unlike the desktop's eject icon it
        is not powered off, so if it stays in, the next start mounts it
        again (_mount_usb_sticks) with no replug. A stick PoolWind mounted
        itself (new-stick setup, sudo mount) is unmounted with sudo umount
        (allowed by the install's sudoers rule) instead.
        Returns True when it is no longer mounted.
        """
        if not root:
            return False
        try:
            os.sync()                  # whatever happens next, the data is written
        except Exception:
            pass
        if not os.path.ismount(root):
            return True
        try:
            subprocess.run(["gio", "mount", "-u", root],
                           capture_output=True, text=True, timeout=30)
        except Exception as e:
            print("Eject (gio) failed:", e)
        if os.path.ismount(root):
            try:
                subprocess.run(["sudo", "-n", "umount", root],
                               capture_output=True, text=True, timeout=30)
            except Exception as e:
                print("Eject (umount) failed:", e)
        ejected = not os.path.ismount(root)
        print(f"USB stick {root}: {'unmounted, safe to remove' if ejected else 'NOT unmounted (in use?)'}")
        return ejected

    def _close_stick(self):
        """At close: make the swimmer's stick safe to remove. A message only
        when it couldn't be (something else is using it). Bill, 2026-10-17:
        no other messages are needed now that a restart finds the stick
        again. With 'ejectStickOnClose' False everything is just written to
        the stick, and it stays mounted."""
        root = getattr(self, "_stick_root", None)
        if not root or not os.path.isdir(root):
            return                     # no stick in: nothing to say
        name = os.path.basename(os.path.normpath(root))
        if not self.REPdefaults.get(self.KEY_EJECT, True):
            try:
                os.sync()              # the swim is on the stick, not just in memory
            except Exception:
                pass
            print(f"USB stick '{name}' left in ('ejectStickOnClose' is False); everything written")
            return
        if self._eject_stick(root):
            return                     # safe to remove, or to leave in for the next start
        else:
            title = "USB stick not ejected"
            text = (f"Your swim is saved on '{name}', but the stick couldn't be "
                    "ejected: something else is using it (for example a file "
                    "manager window or an editor).\n\nClose anything showing "
                    "the stick, then eject it with the eject icon (\u23cf) in "
                    "the top bar before removing it.")
        print(title + ": " + text.replace("\n\n", " "))
        try:
            if QApplication.instance() is not None:
                QMessageBox.information(None, title, text)
        except Exception as e:
            print("Couldn't show the USB stick message:", e)

    def launch_background_compressor(self, rawfile, outfile):
        script_path = "/tmp/poolwind_compress.sh"
        log_path = "/tmp/poolwind_compress.log"

        if not os.path.exists(script_path):

            script = textwrap.dedent("""\
                #!/bin/bash
                RAW="$1"
                OUT="$2"
                LOG="$3"

                ffmpeg -y -i "$RAW" -vcodec libx264 -preset ultrafast -crf 23 "$OUT" >> "$LOG" 2>&1

                if [ $? -eq 0 ]; then
                    rm "$RAW"
                    mv "$OUT" "$RAW"
                    echo "Compression complete." >> "$LOG"
                else
                    echo "Compression failed." >> "$LOG"
                fi
            """)

            with open(script_path, "w") as f:
                f.write(script)

            os.chmod(script_path, os.stat(script_path).st_mode | stat.S_IEXEC)

        subprocess.Popen([script_path, rawfile, outfile, log_path])



    def reload_defaults_if_changed(self):
        """Hot-reload REPdefaults if the defaults file changed on disk."""
        try:
            new_mtime = os.path.getmtime(self.defaults_path)
        except FileNotFoundError:
            return  # file missing — ignore

        if new_mtime != self.defaults_mtime:
            print("Detected change in defaults file — reloading parameters...")
            self.defaults_mtime = new_mtime

            try:
                new_defaults = self._read_defaults_file()
            except Exception as e:
                print("Error reloading defaults:", e)
                return

            # Replace REPdefaults, then re-apply the swimmer's USB-stick
            # settings (before v7.44 a reload silently dropped them for the
            # rest of the session)
            self.original_defaults = new_defaults.copy()
            self.REPdefaults = self._derive_internal_defaults(new_defaults)
            if self._ind_defaults is not None:
                self._apply_individual_defaults(self._ind_defaults)
            self.PaceLimitsDec = self.REPdefaults["PaceLimitsDec"]   # zones rebuild on their own
            self.zoneWidth = self.REPdefaults["middleSwimZone %"] / 100

            print("Reload complete.")

        self._reload_individual_if_changed()

    def _reload_individual_if_changed(self):
        """
        Hot-reload the swimmer's USB-stick file (checked about once a second):
        its pace limits and height take effect right away (the zones are
        rebuilt automatically). recordTrainingVideo is applied too, but
        recording itself is only started/stopped at program start.
        If the stick is pulled or the file can't be read, the last good
        settings are kept.
        """
        if self._ind_path is None:
            return
        now = time.time()
        if now - self._ind_check_t < 1.0:
            return
        self._ind_check_t = now
        try:
            mtime = os.path.getmtime(self._ind_path)
        except OSError:
            return          # stick removed / unreadable: keep the last settings
        if mtime == self._ind_mtime:
            return
        self._ind_mtime = mtime
        try:
            with open(self._ind_path, "r") as f:
                ind_defaults = ast.literal_eval(f.read())
            self._pace_limits(self._rename_old_settings(ind_defaults).get(self.KEY_PACE, ("5:00", "1:30")))
        except Exception as e:
            print("Error reloading the USB stick's settings (keeping the previous ones):", e)
            return
        print("Detected change in the USB stick's settings -- reloading...")
        # Put the stick-controlled settings back to the main file's values,
        # then overlay the new stick file (so a setting removed from the
        # stick falls back to the main default). Everything else in
        # REPdefaults is left alone -- e.g. an unsaved Set Swim Area.
        base = self._derive_internal_defaults(self.original_defaults)
        for key in ("PaceLimitsDec", "swimmersHeight,usablePoolLength") + self.STICK_KEYS:
            if key in base:
                self.REPdefaults[key] = base[key]
        self._apply_individual_defaults(ind_defaults)
        self.PaceLimitsDec = self.REPdefaults["PaceLimitsDec"]
        print("USB stick settings reloaded.")

    def initial_voltage_winddown(self, title="Starting Up"):
        """
        Force the valve DOWN until voltage < minV: before the UI appears,
        at shutdown, and when leaving or returning to the main screen.
        Shows a small modal window with live voltage updates.
        """
        if self.valveOption != "real":
            return

        # --- Create modal popup ---
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        msg.setWindowModality(QtCore.Qt.ApplicationModal)

        # Initial text
        msg.setText("Please wait for voltage wind down…")
        msg.setInformativeText("Voltage: ---.--- V")
        msg.show()

        # --- Read limits ---
        minV, maxV = self.SafetyVoltageLimits

        # --- Read initial voltage ---
        volts = self.takeReading()

        # If already safe, nothing to do
        if volts <= minV:
            msg.close()
            return


        # --- Loop until voltage drops below minV ---
        # Time limit: if the voltage never gets there (Pace cable unplugged,
        # a pool that ignores DN while the pump is off, ...), stop pressing
        # DN instead of waiting forever.
        self._winding_down = True
        give_up_at = time.time() + self.WINDDOWN_TIMEOUT_S
        while True:
            QtWidgets.QApplication.processEvents()   # keep UI alive
            self.DN_relay()
            volts = self.takeReading()
            self.currentVoltage = volts

            # Update message text
            msg.setInformativeText(f"Voltage: {volts:.3f} V")
            if volts <= minV:
                break
            if time.time() > give_up_at:
                print(f"Wind-down stopped after {self.WINDDOWN_TIMEOUT_S:.0f} s: the voltage "
                      f"stayed at {volts:.3f} V, above {minV:.3f} V")
                break

            time.sleep(0.05)  # gentle polling

        # --- Stop relay ---
        self.relay_off()
        self._winding_down = False
        msg.close()

    WINDDOWN_TIMEOUT_S = 60.0     # longest a wind-down may hold DN

    # ------------------------------------------------------------------
    # Leaving the main screen (Swim Plot, Set Swim Area): the main loop
    # pauses there, and it is the only code that releases UP/DN. So wind
    # the jet down first, then disconnect the UP and DN relays until the
    # main screen is back. On/Off stays connected. (Bill, 2026-10-16: a
    # relay left on while a plot was open ran the jet up to high.)
    # ------------------------------------------------------------------
    # Swim zone highlight on/off, shared by the pool screen and Swim Plot
    # replay; starts as 'zoneHighlight' says.
    def zone_highlight_on(self):
        if not hasattr(self, "_zone_highlight"):
            self._zone_highlight = bool(self.REPdefaults.get("zoneHighlight", True))
        return self._zone_highlight

    def toggle_zone_highlight(self):
        self._zone_highlight = not self.zone_highlight_on()

    def leave_main_screen(self):
        self.hold_mode = False                  # no held speed to come back to
        self.initial_voltage_winddown("Leaving the pool screen")
        self.relay_off()
        self.GPIO.release(self.PIN_UP)
        self.GPIO.release(self.PIN_DN)

    def return_to_main_screen(self):
        self.GPIO.reclaim(self.PIN_UP)
        self.GPIO.reclaim(self.PIN_DN)
        self.relay_off()
        self.initial_voltage_winddown("Back to the pool screen")
        # Start the jet target from slow, as at startup: the swimmer has to
        # be found again before the jet speeds up, and nothing from before
        # the menu (position, grace window) carries over.
        w = self.window
        w.EMA_CoM_h = 10.0
        w.CoM_h = 10
        w.windDownStartTime = 0.0
        w._out_of_view_since_found = True
        self._last_update_loop_t = time.time()

    # ------------------------------------------------------------------
    # Relay watchdog: a timer of its own, outside the main loop. If the
    # main loop hasn't run for RELAY_WATCHDOG_S (a stall, a slow camera,
    # a dialog), let go of UP/DN, so a held button can never run the jet
    # away. The loop presses them again when it runs.
    # ------------------------------------------------------------------
    RELAY_WATCHDOG_S = 1.0

    def start_relay_watchdog(self):
        self._last_update_loop_t = time.time()
        self._relay_watchdog = QTimer()
        self._relay_watchdog.timeout.connect(self._relay_watchdog_check)
        self._relay_watchdog.start(250)

    def _relay_watchdog_check(self):
        if getattr(self, "_winding_down", False) or self.currentDirection == "LEVEL":
            return
        stalled = time.time() - getattr(self, "_last_update_loop_t", 0.0)
        if stalled > self.RELAY_WATCHDOG_S:
            print(f"Relay watchdog: main loop stalled {stalled:.1f} s, UP/DN released")
            self.relay_off()

    def detect_current_mode(self):
        try:
            out = subprocess.check_output(
                ["xrandr", "--verbose"],
                stderr=subprocess.STDOUT
            ).decode("utf-8")
        except Exception:
            return "work"

        current_mode = None
        rotation = None

        for line in out.splitlines():
            line = line.strip()

            # The first connected monitor (HDMI-1 on the author's Pi)
            if current_mode is None and rotation is None and re.match(r"\S+ connected", line):
                parts = line.split()

                # Extract mode (the token containing "x" and "+")
                for p in parts:
                    if "x" in p and "+" in p:
                        current_mode = p.split("+")[0]  # e.g. "600x800"
                        break

                # Extract rotation: the word AFTER the "(0xNN)" token
                # Find the index of the "(0xNN)" token
                for i, p in enumerate(parts):
                    if p.startswith("(") and p.endswith(")"):
                        if i + 1 < len(parts):
                            rotation = parts[i + 1]  # "normal" or "left"
                        break

        # Decide based on rotation first
        if rotation == "left":
            return "pool"

        # Fallback: decide based on mode
        if current_mode == "600x800":
            return "pool"

        return "work"

    def _parse_csv_file(self, csv_path, with_com=False):
        # with_com=True also returns CoM_h and the swimmer tick's CoM_w per
        # row (columns 6-7, logged since v7.43; NaN for older files).
        time_raw    = []
        pace_raw    = []
        dist_raw    = []
        segment_raw = []
        frame_raw   = []
        comh_raw    = []
        comw_raw    = []
        zone_raw    = []    # columns 8-9 (since v15.2): jet zone, number of zones
        zones_raw   = []

        if not os.path.isfile(csv_path):
            if with_com:
                return (time_raw, pace_raw, dist_raw, segment_raw, frame_raw,
                        comh_raw, comw_raw, zone_raw, zones_raw)
            return time_raw, pace_raw, dist_raw, segment_raw, frame_raw

        with open(csv_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) < 5:
                    continue

                try:
                    t   = float(parts[0])   # full epoch timestamp
                    p   = float(parts[1])
                    d   = float(parts[2])
                    seg = int(parts[3])
                    frm = int(parts[4])
                except:
                    continue

                try:
                    ch = float(parts[5]) if len(parts) >= 7 else float("nan")
                    cw = float(parts[6]) if len(parts) >= 7 else float("nan")
                except ValueError:
                    ch = cw = float("nan")
                try:
                    zn = float(parts[7]) if len(parts) >= 9 else float("nan")
                    zs = float(parts[8]) if len(parts) >= 9 else float("nan")
                except ValueError:
                    zn = zs = float("nan")

                time_raw.append(t)
                pace_raw.append(p)
                dist_raw.append(d)
                segment_raw.append(seg)
                frame_raw.append(frm)
                comh_raw.append(ch)
                comw_raw.append(cw)
                zone_raw.append(zn)
                zones_raw.append(zs)

        if with_com:
            return (time_raw, pace_raw, dist_raw, segment_raw, frame_raw,
                    comh_raw, comw_raw, zone_raw, zones_raw)
        return time_raw, pace_raw, dist_raw, segment_raw, frame_raw

    def load_today_csv(self):
        time_raw, pace_raw, dist_raw, segment_raw, frame_raw = self._parse_csv_file(self.todayCsvFile)

        # Ensure sorted by timestamp (important for multi‑day merges)
        zipped = sorted(zip(time_raw, pace_raw, dist_raw, segment_raw, frame_raw),
                        key=lambda x: x[0])
        if zipped:
            time_raw, pace_raw, dist_raw, segment_raw, frame_raw = map(list, zip(*zipped))
        else:
            time_raw, pace_raw, dist_raw, segment_raw, frame_raw = [], [], [], [], []

        return time_raw, pace_raw, dist_raw, segment_raw, frame_raw

    def load_csv_range(self, from_date, to_date, progress_cb=None):
        """
        Load and concatenate daily CSVs for every date in [from_date, to_date]
        (inclusive). Each row is tagged with its source date (as
        date.toordinal(), so it fits in the same float array as the other
        columns) so SwimPlotWindow can find the matching per-day AVI segment
        when scrubbing video across a multi-day range.

        progress_cb(day_num, total_days, d), if given, is called after each
        day's file is read — lets a caller (e.g. SwimPlotWindow) show
        incremental "loading..." progress on a large range instead of one
        long blocking call with no feedback.
        """
        time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw = [], [], [], [], [], []
        comh_raw, comw_raw, zone_raw, zones_raw = [], [], [], []

        # cumulative_distance_miles in each day's CSV restarts at 0 for
        # that day (App.total_distance resets on every new run/session).
        # Carry a running offset across days so a multi-day range shows one
        # continuously-accumulating distance instead of resetting per day.
        dist_offset = 0.0

        total_days = (to_date - from_date).days + 1
        day_num = 0
        d = from_date
        while d <= to_date:
            day_num += 1
            csv_path = os.path.join(self.data_dir, f"{d.isoformat()}.csv")
            t, p, dist, seg, frm, ch, cw, zn, zs = self._parse_csv_file(csv_path, with_com=True)
            if dist:
                days_own_total = dist[-1]   # this day's final distance, before offsetting
                dist = [x + dist_offset for x in dist]
                dist_offset += days_own_total
            date_raw.extend([d.toordinal()] * len(t))
            time_raw.extend(t)
            pace_raw.extend(p)
            dist_raw.extend(dist)
            segment_raw.extend(seg)
            frame_raw.extend(frm)
            comh_raw.extend(ch)
            comw_raw.extend(cw)
            zone_raw.extend(zn)
            zones_raw.extend(zs)
            if progress_cb is not None:
                progress_cb(day_num, total_days, d)
            d += timedelta(days=1)

        zipped = sorted(zip(time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw,
                            comh_raw, comw_raw, zone_raw, zones_raw),
                        key=lambda x: x[0])
        if zipped:
            (time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw,
             comh_raw, comw_raw, zone_raw, zones_raw) = map(list, zip(*zipped))
        else:
            time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw = [], [], [], [], [], []
            comh_raw, comw_raw, zone_raw, zones_raw = [], [], [], []

        return (time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw,
                comh_raw, comw_raw, zone_raw, zones_raw)

class QtMainWindow(QMainWindow):  # Version 4.0 original
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.windDownStartTime = time.time()
        self.windDownTime = self.app.REPdefaults['inactivity wind down time (sec)']
        self.last_x = None
        self.last_y = None
        self.clickWasButton = None
        self.pressed_btn = None      # button drawn recessed while touched
        self.pressed_t = 0.0
        self.logDistance = False
        
        self.debug_blob_mask = None

        from collections import deque

        # Temporal history for F-mask scoring
        self.prev_masks = deque(maxlen=10)
        self.prev_centroids = deque(maxlen=10)

        self.debug_session_id = int(time.time())

        # ---------------------------------------------------------
        # CoM tracking
        # ---------------------------------------------------------
        self.swimmerFound = None
        self.filteredCoM = None
        self.CoM_w = 1
        self.CoM_h = 1
        # Last CoM_h seen while genuinely auto-tracking (not held) and
        # swimmerFound was True. This is what Hold_btn_press freezes into
        # frozen_CoM_h, so toggling hold never snapshots a wind-down-decayed
        # neutral value instead of the swimmer's real last position.
        self.last_real_CoM_h = 1
        self.mouseDown = False
        self.last_hold_mode = False  # track Hold edge

        self.any_button_pressed = False

        # ---------------------------------------------------------
        # Apply window size
        # ---------------------------------------------------------
        self.setFixedSize(self.app.window_w, self.app.window_h)

        if self.app.display_device == "pool":
            # Remove title bar for full-screen portrait display
            self.setWindowFlags(Qt.FramelessWindowHint)

        elif self.app.display_device == "work":
            # Normal window with title bar
            self.setWindowFlags(Qt.Window)

        # Position window at top-left
        self.move(0, 0)

        # ---------------------------------------------------------
        # Full-window video display (QWidget-based, no QLabel pixmap)
        # ---------------------------------------------------------
        self.display_canvas = DisplayCanvas()
        self.display_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.display_canvas)



        self.setCentralWidget(container)

        # ---------------------------------------------------------
        # Floating menu button
        # ---------------------------------------------------------
        self.menu_button = QPushButton("≡", self)
        self.menu_button.setFixedSize(36, 36)

        self.menu_button.move(5, 5)
        self.menu_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 120);
                color: white;
                border: none;
                font-size: 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 160);
            }
        """)

        self.menu_button.clicked.connect(self.showMenu)

        # Mouse tracking + event forwarding
        self.display_canvas.setMouseTracking(True)
        self.display_canvas.installEventFilter(self)

        # ---------------------------------------------------------
        # Pull video from App
        # ---------------------------------------------------------
        self.myVideoCapture = app.myVideoCapture

        # ---------------------------------------------------------
        # FAST VIDEO LOOP (max FPS)
        # ---------------------------------------------------------
        QTimer.singleShot(0, self.qt_update_loop)


        # Button rects in WORKING-SPACE (480×640)
        self.btn_rects = {}     # you will fill these with 480×640 coords
        self.last_frame = None

    def qt_update_loop(self):  
        zone_mask = None
        corridor_mask = None
        if self.app.REPdefaults["Runtime: hotReloadParameters"]:
            self.app.reload_defaults_if_changed()

        # Auto-pause recording when the program is paused
        if self.app.pause_update_loop:
            if self.myVideoCapture.makeRawVideo == "Start":
                self.myVideoCapture.makeRawVideo = "Pause"
            if self.myVideoCapture.makePerspectVideo == "Start":
                self.myVideoCapture.makePerspectVideo = "Pause"


        ok, full_img, perspect_img = self.myVideoCapture.getImages()
        if not ok:
            QTimer.singleShot(0, self.qt_update_loop)
            return
        
        self.app.last_perspect_img = perspect_img.copy()

        #===========================================================
        # Auto swimmer blob detection — ALWAYS runs, regardless of hold_mode.
        # hold_mode only freezes the elongated/corrected CoM_h used for
        # jet control; CoM_w and CoM_h_raw must stay live so swimmerFound
        # can be evaluated in every state.
        #===========================================================

        # 1. Full-frame segmentation (always full perspect_img)
        full_mask = self.F_mask(perspect_img)

        # 2. Compute blob CoM on the FULL mask (never crop before this).
        # Captured before get_auto_CoM overwrites blob_CoM_w, so the
        # CoM_w EMA below can tell "blob just reappeared after being
        # fully absent" apart from "blob continuously tracked" -- see
        # that section for why it matters.
        blob_was_absent_last_frame = getattr(self, "blob_CoM_w", None) is None
        self.blob_CoM_w, self.blob_CoM_h, full_corridor_mask = self.get_auto_CoM(full_mask)

        # 3. Now crop ONLY for display (zone_mask + corridor_mask)
        half = self.app.zoneWidth / 2.0
        left  = int((0.5 - half) * self.app.work_size_w)
        right = int((0.5 + half) * self.app.work_size_w)

        zone_mask = full_mask[:, left:right]
        corridor_mask = full_corridor_mask[:, left:right]

        #===========================================================
        # CoM_w: EMA-smoothed the same way in every state — never
        # frozen, never wind-down'd to neutral (it exists only to
        # test whether the swimmer/blob is in the zone). No-blob default
        # rests at whichever off-zone edge (0 = right wall, 700 = left
        # wall) is closer to wherever the blob was last seen, rather
        # than always the same fixed edge -- both are safely outside the
        # zone/margin bounds either way, so this doesn't change
        # swimmerFound correctness, it just means a smaller visual jump
        # when a blob reappears and gets snapped to (see below) if it
        # shows up on the same side it was last seen on.
        #===========================================================
        alpha = self.app.REPdefaults["CoM filter Alpha"]

        if self.blob_CoM_w is not None:
            ema_input_w = self.blob_CoM_w
        else:
            ema_input_w = 0.0 if self.CoM_w < 350 else 700.0

        if not hasattr(self, "EMA_CoM_w"):
            self.EMA_CoM_w = ema_input_w
        elif self.blob_CoM_w is not None and blob_was_absent_last_frame:
            # Blob just reappeared after being fully absent -- snap
            # straight to its real position instead of blending from the
            # stale "no blob" resting placeholder (0 or 700 above).
            # Blending here would have
            # the EMA sweep across the whole width on its way to the
            # real position, transiently passing straight through the
            # swim zone and satisfying the width check along the way --
            # a brief, spurious swimmerFound blip with a real CoM_h jump
            # to match, even though no swimmer was ever actually in the
            # zone. The disappearing direction doesn't need this: while
            # blob_CoM_w is None, swimmerFound is already unconditionally
            # false regardless of what CoM_w's EMA is doing.
            self.EMA_CoM_w = ema_input_w
        else:
            self.EMA_CoM_w = alpha * ema_input_w + (1 - alpha) * self.EMA_CoM_w
        self.CoM_w = round(self.EMA_CoM_w)

        #===========================================================
        # CoM_h_raw: same always-live EMA treatment as CoM_w above, but
        # fed by the RAW (pre-BodyCoMCorrection) blob_CoM_h. Exists only
        # for the front/back swimmerFound test below -- the elongated
        # CoM_h (fingertip/toe reach correction) is still what drives
        # jet control and the on-screen display, computed separately.
        #===========================================================
        ema_input_h_raw = self.blob_CoM_h if self.blob_CoM_h is not None else 500.0

        if not hasattr(self, "EMA_CoM_h_raw"):
            self.EMA_CoM_h_raw = ema_input_h_raw
        else:
            self.EMA_CoM_h_raw = alpha * ema_input_h_raw + (1 - alpha) * self.EMA_CoM_h_raw
        self.CoM_h_raw = round(self.EMA_CoM_h_raw)

        #===========================================================
        # SwimmerFound test: live CoM_w must be within the middle swim
        # zone (side-to-side), AND live CoM_h_raw must be held back at
        # least a fixed margin from each pool end (front/back) -- keeps
        # jet froth near either wall from being mistaken for the
        # swimmer. Margin is applied to the raw centroid, never the
        # elongated/corrected CoM_h, so a genuine swimmer's reach being
        # elongated near a wall can't itself cause a false negative here.
        # A real detection (live, or within get_auto_CoM's bounded
        # dropout hold) is also required -- CoM_w/CoM_h_raw's EMA falls
        # back to fixed center defaults (375/500, see above) whenever
        # blob_CoM_w/h are None, which sit inside the zone/margin bounds
        # on their own and would otherwise read as a swimmer being
        # exactly centered in the pool with no blob present at all.
        #===========================================================
        half = self.app.zoneWidth / 2.0
        left  = int((0.5 - half) * self.app.CoM_size_w)
        right = int((0.5 + half) * self.app.CoM_size_w)
        w_ok = left <= self.CoM_w <= right

        FRONT_BACK_MARGIN_FT = 0.5
        _, usablePoolLength = self.app.REPdefaults["swimmersHeight,usablePoolLength"]
        margin_h = (FRONT_BACK_MARGIN_FT * 12.0 / usablePoolLength) * self.app.CoM_size_h
        h_ok = margin_h <= self.CoM_h_raw <= (self.app.CoM_size_h - margin_h)

        self.swimmerFound = w_ok and h_ok and (self.blob_CoM_w is not None)

        # Suspend button forces "not found"
        if self.app.suspendButtonText == "Resume":
            self.swimmerFound = False

        #===========================================================
        # CoM_h: frozen while holding (± UP/DN), live EMA'd + wind-down
        # otherwise.
        #===========================================================
        if self.app.hold_mode:
            # UP/DN on the touchscreen: one jet step per press (taken on the
            # touch itself, App._hold_first_step), repeated here while held
            # (the jet itself takes about a second per step). Only the
            # UP/DN buttons themselves count -- not another button pressed
            # after them.
            held = self.pressed_btn if (self.mouseDown and self.clickWasButton) else None
            if held in ("UP", "DN"):
                now = time.time()
                if held != getattr(self, "_hold_step_btn", None) or now >= self._hold_step_next:
                    self.app.step_held_zone(+1 if held == "UP" else -1)
                    self._hold_step_next = now + self.app.HOLD_STEP_REPEAT_S
                    self._hold_step_btn = held
            else:
                self._hold_step_btn = None

            self.CoM_h = self.app.frozen_CoM_h
            self.logDistance = self.swimmerFound
            self._com_h_decaying = False   # holding a real value, not decaying

        else:
            #===========================================================
            # Wind-down logic (decides whether EMA should be fed 10)
            #===========================================================

            branch_taken = "?"

            if self.app.firstTime:
                ema_input_h = 10.0
                self.logDistance = False
                branch_taken = "firstTime"

            elif self.swimmerFound:
                self.windDownStartTime = time.time()
                self.logDistance = True
                ema_input_h = self.blob_CoM_h
                self._out_of_view_since_found = False
                branch_taken = "swimmerFound"

            elif self.app.suspendButtonText == "Resume":
                ema_input_h = 10.0
                branch_taken = "suspended"

            elif self.blob_CoM_w is None:
                # No blob at all (beyond get_auto_CoM's bounded dropout
                # hold) -- skip the "still nearby" grace window below
                # entirely and start decaying to neutral immediately,
                # rather than waiting windDownTime like the case where a
                # real blob still exists just outside the zone. Also
                # mark that the swimmer has left the perspective view
                # entirely since they were last actually tracked -- see
                # the branch below.
                ema_input_h = 10.0
                self.logDistance = False
                self._out_of_view_since_found = True
                branch_taken = "no_blob"

            elif getattr(self, "_out_of_view_since_found", False):
                # A blob exists again, but the swimmer was fully outside
                # the perspective view at some point since they were last
                # actually tracked in the zone -- e.g. no_blob_zone (out
                # of frame entirely) then straight into no_swim_zone
                # (visible but still outside the zone). Once that's
                # happened, don't let the grace window below fire for the
                # rest of this "outing" just because some of the original
                # windDownTime happens to still be left over from the
                # earlier real tracking -- that grace period is only
                # meant for someone who stays continuously visible just
                # outside the zone the whole time (e.g. walking to the Pi
                # while still in frame), not someone who disappeared and
                # came back.
                ema_input_h = 10.0
                self.logDistance = False
                branch_taken = "was_out_of_view"

            elif time.time() - self.windDownStartTime >= self.windDownTime:
                # swimmer NOT found, grace period expired -> decay to neutral
                ema_input_h = 10.0
                self.logDistance = False
                branch_taken = "grace_expired"

            else:
                # swimmer NOT found, but a blob has been continuously
                # present (just outside the zone) since at least last
                # frame, and we're still within the short wind-down grace
                # window (e.g. swimmer walking to the Pi to adjust flow).
                # Freeze CoM_h at the last real value instead of feeding
                # the EMA the live (out-of-zone) blob position, which
                # otherwise sends the valve toward one extreme while the
                # swimmer is out of frame.
                self.CoM_h = self.last_real_CoM_h
                ema_input_h = None   # skip EMA update below
                branch_taken = "grace_freeze"

            #===========================================================
            # EMA FILTER (CoM_h) — skipped while frozen above
            #===========================================================
            if ema_input_h is not None:
                if not hasattr(self, "EMA_CoM_h"):
                    self.EMA_CoM_h = ema_input_h
                else:
                    self.EMA_CoM_h = alpha * ema_input_h + (1 - alpha) * self.EMA_CoM_h

                # Output CoM_h is the EMA result
                self.CoM_h = round(self.EMA_CoM_h)
                self.CoM_h = self.BodyCoMCorrection(self.CoM_h)

            # Display-only: whenever CoM_h is being decayed toward
            # neutral/zero (as opposed to actively tracking or frozen at
            # a real held value), also hide the CoM_w tick -- even
            # though a real blob may still be live-tracked internally
            # for zone-entry detection (see the CoM_w EMA above, which
            # deliberately keeps tracking it so re-entering the zone
            # doesn't hesitate). This only affects what's drawn, not the
            # tracking value itself.
            self._com_h_decaying = branch_taken in (
                "firstTime", "suspended", "no_blob", "was_out_of_view", "grace_expired"
            )

        # Remember the last CoM_h seen while genuinely auto-tracking
        # (not held) with the swimmer in the zone. Hold_btn_press freezes
        # from THIS, not from the live CoM_h, so a hold toggle never
        # snapshots a wind-down-decayed value.
        if not self.app.hold_mode and self.swimmerFound:
            self.last_real_CoM_h = self.CoM_h

        # ---------------------------------------------------------
        # 8. Select display frame based on view_mode from view button
        # ---------------------------------------------------------

        # view_mode 1 — perspective image
        if self.app.view_mode == 1:
            frame = perspect_img
            frame = self.apply_overlays(frame)
            self.last_frame = frame.copy()

        elif self.app.view_mode == 2:
            frame = self.place_mask_in_workspace(zone_mask)
            frame = self.apply_overlays(frame)
            self.last_frame = frame.copy()

        elif self.app.view_mode == 3:
            frame = self.place_mask_in_workspace(corridor_mask)
            frame = self.apply_overlays(frame)
            self.last_frame = frame.copy()

        elif self.app.view_mode == 4:
            blob = getattr(self, "debug_blob_mask", None)
            frame = self.place_mask_in_workspace(blob)
            frame = self.apply_overlays(frame)
            self.last_frame = frame.copy()

        else:
            frame = np.zeros((self.app.work_size_h, self.app.work_size_w, 3), dtype=np.uint8)

        frame = cv2.resize(frame, (self.app.window_w, self.app.window_h))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # --- PAINTING START ---
        pixmap = QPixmap.fromImage(qimg)
        self.display_canvas.setFrame(pixmap)


        # now do App functions
        self.app.UpdateLoop()

        # --- FPS COUNTER (unchanged) ---
        now = time.time()
        if not hasattr(self, "_fps_last"):
            self._fps_last = now
            self._fps_count = 0
        self._fps_count += 1
        if now - self._fps_last >= 1.0:
            # print(f"qt_update_loop: {self._fps_count} loops/sec")
            self._fps_last = now
            self._fps_count = 0

        # reschedule only if system is running AND not paused
        if not self.app.systemShutdown and not self.app.pause_update_loop:
            QTimer.singleShot(0, self.qt_update_loop)

    def F_mask(self, perspect_img):
        """
        Full-frame swimmer mask with:
        1. Sensitivity gate (minimum blob size)
        2. Largest-blob selector
        3. Scoring system (tie-breaker)
        """

        # ---------------------------------------------------------
        # 0. Load tuning parameters
        # ---------------------------------------------------------
        # keep this framework in case tuning is required
        # aaa, bbb, ccc, ddd, eee = self.app.REPdefaults["temp tuning vars aaa bbb ccc ddd eee"]
        # thresholdTune  = aaa
        # maxAreaTune    = bbb
        # hsvWeightTune  = ccc
        # morphTune      = ddd
        # sensitivity    = self.app.REPdefaults["Sensitivity"]  # minimum swimmer area

        # tuned by trial and error
        thresholdTune  = 50
        maxAreaTune    = 0.2
        hsvWeightTune  = 0.0
        morphTune      = 1.0
        sensitivity    = self.app.REPdefaults["Sensitivity"]  # minimum swimmer area

        # ---------------------------------------------------------
        # 1. Convert full frame to HSV and compute global average
        # ---------------------------------------------------------
        hsv_full = cv2.cvtColor(perspect_img, cv2.COLOR_BGR2HSV)
        # Utils.MakePNG(hsv_full, "F1_hsv_full.png")

        H_mean = int(np.mean(hsv_full[:, :, 0]))
        S_mean = int(np.mean(hsv_full[:, :, 1]))
        V_mean = int(np.mean(hsv_full[:, :, 2]))
        avg_hsv = np.array([H_mean, S_mean, V_mean], dtype=np.int16)

        #Utils.DumpMedianHSV(H_mean, S_mean, V_mean, "F1_avg_hsv.txt")

        # ---------------------------------------------------------
        # 2. HSV distance map
        # ---------------------------------------------------------
        hsv_zone = hsv_full.astype(np.int16)
        diff = np.abs(hsv_zone - avg_hsv)

        diff_h = diff[:, :, 0]
        diff_s = diff[:, :, 1]
        diff_v = diff[:, :, 2]

        dist = diff_h + diff_s + diff_v
        # Utils.MakePNG(dist.astype(np.uint8), "F2_dist_sum.png")

        # ---------------------------------------------------------
        # 3. Threshold
        # ---------------------------------------------------------
        threshold = 60 + int(thresholdTune)
        _, mask = cv2.threshold(dist.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY)

        # ---------------------------------------------------------
        # 4. Morphology cleanup
        # ---------------------------------------------------------
        k = int(max(1, morphTune))
        kernel = np.ones((k, k), np.uint8)

        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        mask = mask_open

        # ---------------------------------------------------------
        # 5. Find contours on FULL FRAME
        # ---------------------------------------------------------
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_img, contours, -1, (0,255,0), 1)
        # Utils.MakePNG(contour_img, "F5_contours.png")

        if not contours:
            # Utils.MakePNG(mask, "F5_no_contours.png")
            return np.zeros_like(mask)

        # ---------------------------------------------------------
        # 6. Sensitivity Gate + Largest Blob + Scoring
        # ---------------------------------------------------------
        h, w = mask.shape

        candidates = []
        candidate_canvas = np.zeros((h, w, 3), dtype=np.uint8)

        for cnt in contours:
            cnt = np.array(cnt, dtype=np.int32)
            area = cv2.contourArea(cnt)

            # Sensitivity gate
            if area < sensitivity:
                continue

            # Max area gate
            if area > maxAreaTune * (h * w):
                continue

            # Draw candidate outline
            cv2.drawContours(candidate_canvas, [cnt], -1, (255,255,255), 1)
            #Utils.DumpTXT(f"Candidate area = {area}", "F6_scores.txt")

            # Compute scoring features
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # HSV similarity score
            mask_cnt = np.zeros_like(mask)
            cv2.drawContours(mask_cnt, [cnt], -1, 255, -1)
            mean_hsv = cv2.mean(hsv_full, mask=mask_cnt)[:3]
            hsv_diff = abs(mean_hsv[0] - H_mean) + abs(mean_hsv[1] - S_mean) + abs(mean_hsv[2] - V_mean)
            hsv_score = max(0, 255 - hsv_diff) * hsvWeightTune

            # Position score (favor center)
            pos_score = max(0, 1.0 - abs(cx - w/2) / (w/2)) * 100

            # Area score
            area_score = min(area / (h*w), 1.0) * 100

            # Temporal score (if available)
            temporal_score = 0
            if hasattr(self, "prev_centroids") and len(self.prev_centroids) > 0:
                prev_cx, prev_cy = self.prev_centroids[-1]
                dist_prev = np.hypot(cx - prev_cx, cy - prev_cy)
                temporal_score = max(0, 100 - dist_prev)

            # Total score
            total_score = hsv_score + pos_score + area_score + temporal_score

            candidates.append((total_score, cnt, area, (cx, cy)))

        # Utils.MakePNG(candidate_canvas, "F6_candidate_blobs.png")

        if not candidates:
            #Utils.DumpTXT("No candidate survived Sensitivity gate", "F6_scores.txt")
            return np.zeros_like(mask)

        # Pick highest scoring blob
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_cnt, best_area, best_centroid = candidates[0]

        #Utils.DumpTXT(f"Selected area = {best_area}, score = {best_score}", "F6_scores.txt")

        # ---------------------------------------------------------
        # 7. Final full-frame mask
        # ---------------------------------------------------------
        final_mask = np.zeros_like(mask)
        cv2.drawContours(final_mask, [best_cnt], -1, 255, thickness=-1)
        # Utils.MakePNG(final_mask, "F7_final_mask.png")

        # ---------------------------------------------------------
        # 8. Update temporal history
        # ---------------------------------------------------------
        if not hasattr(self, "prev_masks"):
            from collections import deque
            self.prev_masks = deque(maxlen=10)
            self.prev_centroids = deque(maxlen=10)

        self.prev_masks.append(final_mask.copy())
        self.prev_centroids.append(np.array(best_centroid))

        return final_mask

    # Consecutive no-detection frames a dropout is held through before
    # get_auto_CoM starts reporting None instead of the last known
    # position (see the DROPOUT_HOLD_FRAMES note in get_auto_CoM).
    DROPOUT_HOLD_FRAMES = 3

    def _dropout_hold(self, z_mask):
        """
        Called from every "nothing detected this frame" branch in
        get_auto_CoM. Rides through a brief, normal dropout (water
        motion/splash briefly obscuring the swimmer -- happens routinely
        during real swimming) by holding the last known position/mask
        for up to DROPOUT_HOLD_FRAMES consecutive misses. Beyond that,
        reports None (genuinely not found) rather than holding
        indefinitely -- this bound is what fixes the earlier bug where
        an unbounded version of this same idea let a brief false blob
        (e.g. an elbow) get stuck on-screen and driving the jet for the
        rest of the session once real detection stopped.
        """
        self._auto_com_miss_count = getattr(self, "_auto_com_miss_count", 0) + 1
        if (self._auto_com_miss_count <= self.DROPOUT_HOLD_FRAMES
                and hasattr(self, "_last_blob_CoM_w")):
            return self._last_blob_CoM_w, self._last_blob_CoM_h, self._last_corridor_mask
        return None, None, np.zeros_like(z_mask)

    def get_auto_CoM(self, z_mask):

        # 0. Empty-mask guard.
        if z_mask.sum() == 0:
            return self._dropout_hold(z_mask)

        # 1. Clean mask
        kernel = np.ones((5,5), np.uint8)
        cleaned = cv2.morphologyEx(z_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)
        cleaned = cv2.dilate(cleaned, kernel, iterations=1)

        # 2. Find blobs
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned, 8)

        blobs = []
        for label in range(1, num_labels):
            x, y, w, h, area = stats[label]
            cx, cy = centroids[label]
            blob_mask = (labels == label).astype(np.uint8) * 255
            blobs.append({"area": area, "bbox": (x,y,w,h), "centroid": (cx,cy), "mask": blob_mask})

        # Fallback if no blobs found.
        if not blobs:
            return self._dropout_hold(z_mask)

        # 3. Select largest blob
        swimmer_blob = max(blobs, key=lambda b: b["area"])
        mask = swimmer_blob["mask"]
        cx, cy = swimmer_blob["centroid"]
        h, w = mask.shape

        # 4. Adaptive corridor around cx
        corridor_frac = getattr(self, "corridor_frac", 0.01) #0.30)  # wider, safer
        half = (w * corridor_frac / 2)

        left  = max(int(cx - half), 0)
        right = min(int(cx + half), w)

        corridor_mask = np.zeros_like(mask)
        corridor_mask[:, left:right] = mask[:, left:right]

        if corridor_mask.sum() < 50:
            corridor_mask = mask

        # 5. Recompute centroid from narrowed mask.
        ys, xs = np.where(corridor_mask > 0)
        if len(xs) == 0:
            return self._dropout_hold(z_mask)

        cy_cent = np.mean(ys)
        cx_cent = np.mean(xs)

        # Convert to CoM space with inversion
        cy_raw = (z_mask.shape[0] - cy_cent) * (self.app.CoM_size_h / z_mask.shape[0])
        cx_raw = (z_mask.shape[1] - cx_cent) * (self.app.CoM_size_w / z_mask.shape[1])

        # 6. No extra smoothing here -- removed 2026-08-30. The 3-sample
        # rolling median that used to sit here (CoM_hist_h/CoM_hist_w)
        # was measured against a real recorded video to cause a
        # hold-then-jump artifact (needs 2-of-3 window samples to agree
        # before it moves): 73 hold events in a 400-frame clip with the
        # filter on vs. 13 with it off. The downstream EMA (see
        # qt_update_loop) already does the real smoothing job.
        self.blob_CoM_w = cx_raw
        self.blob_CoM_h = cy_raw

        # Real detection this frame -- reset the dropout counter and
        # remember this as the position/mask a following brief dropout
        # would hold.
        self._auto_com_miss_count = 0
        self._last_blob_CoM_w = self.blob_CoM_w
        self._last_blob_CoM_h = self.blob_CoM_h
        self._last_corridor_mask = corridor_mask

        return self.blob_CoM_w, self.blob_CoM_h, corridor_mask

    def BodyCoMCorrection(self, CoM):
        height, usablePoolLength = self.app.REPdefaults["swimmersHeight,usablePoolLength"]
        back_corr, front_corr = body_corr_spans(height, usablePoolLength)

        # Piecewise-linear stretch (2026-08-27): the raw (measured) CoM
        # range the body-center can physically occupy while both toes
        # and fingertips stay within the pool -- [back_corr,
        # 1000-front_corr] -- is stretched to fill the full elongated
        # 0-1000 range. Both halves evaluate to exactly 500 at CoM==500,
        # so the transition is continuous (no jump) all the way through
        # the center, not just asymptotically -- toes at the back wall
        # -> exactly 0, fingertips at the front wall -> exactly 1000,
        # dead center -> exactly the measured CoM. Replaces the older
        # tapered (distance-from-center-scaled) correction, which never
        # actually reached 0/1000 at the true wall-touch points.
        back_span  = 500 - back_corr
        front_span = (1000 - front_corr) - 500

        if CoM <= 500:
            Out = (CoM - back_corr) / back_span * 500 if back_span > 0 else (0 if CoM < back_corr else 500)
        else:
            Out = 500 + (CoM - 500) / front_span * 500 if front_span > 0 else (1000 if CoM > 1000 - front_corr else 500)

        # Clamp and round
        Out = round(max(0, min(1000, Out)))
        return Out

    def mouse_processor(self, event_type, event):
        # ---------------------------------------------------------------
        # Handle mouse/touch press & release for on-screen buttons. Move,
        # double-click, and scroll used to drive the mouse-CoM debug
        # override (see poolwindAI_v7.33_holdmode_notes.txt for the
        # original design); that feature was removed 2026-08-27 since it
        # was only ever needed for testing without a live swimmer, so
        # those event types are now no-ops.
        # ---------------------------------------------------------------

        x_w = None
        y_h = None

        # PRESS ---------------------------------------------------------
        if event_type == "press":
            x_w = int(event.position().x())
            y_h = int(event.position().y())
            if x_w is None:
                return
            self.mouseDown = True
            self.clickWasButton = False

        # MOVE ----------------------------------------------------------
        elif event_type == "move":
            return

        # RELEASE -------------------------------------------------------
        elif event_type == "release":
            self.mouseDown = False
            self.clickWasButton = False
            return   # no coordinates needed on release

        # DOUBLE-CLICK ----------------------------------------------------
        elif event_type == "dblclick":
            return

        # SCROLL --------------------------------------------------------
        elif event_type == "scroll":
            return

        # ---------------------------------------------------------------
        # End of mouse operation section
        # x_w and y_h are display space coordinates
        # ---------------------------------------------------------------
        # If no coordinates were produced (e.g., release), stop here
        if x_w is None or y_h is None:
            return

        # store last known working-space coordinate
        self.last_x = x_w
        self.last_y = y_h

        # 1) Convert raw Qt coords → working space
        w_h = (y_h / app.window_h) * app.work_size_h
        w_w = (x_w / app.window_w) * app.work_size_w

        # 2) Button hit-test (now in correct coordinate space)
        for name, (bx, by, bw, bh) in self.btn_rects.items():
            if bx <= w_w <= bx + bw and by <= w_h <= by + bh:
                if name == "__CLOSE__":
                    self.close()
                    return
                self.handle_button(name)
                self.clickWasButton = True
                self.pressed_btn = self._btn_key(name)
                self.pressed_t = time.time()
                return
        # End button handling

        # 3) Anywhere else on the picture: swim zone highlight on/off
        self.app.toggle_zone_highlight()

    def eventFilter(self, obj, event):
        p = obj
        while p is not None:
            if isinstance(p, DraggableOverlay):
                return False
            p = p.parent()



        if obj is self.display_canvas:

            if event.type() in (QEvent.MouseButtonPress,
                                QEvent.MouseButtonDblClick,
                                QEvent.MouseMove,
                                QEvent.Wheel):

                if event.type() == QEvent.MouseButtonPress:
                    self.mousePressEvent(event)
                    return True

                elif event.type() == QEvent.MouseButtonDblClick:
                    self.mouseDoubleClickEvent(event)
                    return True

                elif event.type() == QEvent.MouseMove:
                    self.mouseMoveEvent(event)
                    return True

                elif event.type() == QEvent.Wheel:
                    self.wheelEvent(event)
                    return True

        return super().eventFilter(obj, event)

    def draw_com_bar(self, frame):
        """
        Draws the live CoM bar onto `frame` (main view). The swimmer tick is
        skipped when there's no real detection (blob_CoM_w is None -- CoM_w
        then just rests at an off-zone edge) or CoM_h is being decayed to
        neutral (_com_h_decaying, see qt_update_loop).
        """
        if self.CoM_h is None: self.CoM_h = 1
        if self.CoM_w is None: self.CoM_w = 1
        draw_com_bar_on(frame, self.CoM_h, self.com_w_tick(), self.app.zoneWidth,
                        self.app.CoM_size_h, self.app.CoM_size_w)

    def com_w_tick(self):
        """CoM_w if the swimmer tick should be shown, else None."""
        if self.blob_CoM_w is not None and not getattr(self, "_com_h_decaying", False):
            return self.CoM_w
        return None

    def apply_overlays(self, frame):

        # ---------------------------------------------------------
        # Working-space size (always 480×640)
        # ---------------------------------------------------------
        h, w = frame.shape[:2]   # should be 640×480

        # ---------------------------------------------------------
        # 0. Swim zone highlight (tap the picture to switch it)
        # ---------------------------------------------------------
        if self.app.zone_highlight_on():
            draw_zone_band_on(frame, getattr(self.app, "jetZone", None),
                              getattr(self.app, "jetZones", 0),
                              float(self.app.REPdefaults.get("zoneHighlightLevel", 0.10)))

        # ---------------------------------------------------------
        # 1. + 2. Development readouts: the CoM bar and the dIdx / V / CoM
        #         numbers. Hidden unless 'developerMode' is True.
        # ---------------------------------------------------------
        if self.app.REPdefaults["developerMode"]:
            # CoM line (CoM is 0–1000 normalized); 'comBar' False hides it
            if self.app.REPdefaults.get("comBar", True):
                self.draw_com_bar(frame)

            # Numeric fields (positions in 480×640 working space); 'readouts'
            # False hides them (e.g. a screenshot for the user manual)
            if self.app.REPdefaults.get("readouts", True):
                cv2.putText(frame,
                            f"dIdx: {self.app.desiredIndex}",
                            (75, 217),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 0),
                            2)

                cv2.putText(frame,
                            f"V: {self.app.currentVoltage:.3f}",
                            (250, 217),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 0),
                            2)

                cv2.putText(frame,
                            f"CoM: {self.CoM_h}",
                            (165, 340),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 0),
                            2,
                            cv2.LINE_AA)

        # ---------------------------------------------------------
        # 3. Pace, Avg Pace, Distance
        # ---------------------------------------------------------
        avgLabel = "" if self.app.avgPaceDisplay == "" else " avg"

        cv2.putText(frame,
                    self.app.PaceDisplay,
                    (-12,  175),
                    cv2.FONT_HERSHEY_COMPLEX,
                    7, 
                    (0, 255, 204),
                    9) 

        cv2.putText(frame,
                    self.app.avgPaceDisplay + avgLabel,
                    (10, 300),
                    cv2.FONT_HERSHEY_COMPLEX,
                    3,
                    (0, 255, 204),
                    5)

        cv2.putText(frame,
                    self.app.distanceSwam ,
                    (10, 425),
                    cv2.FONT_HERSHEY_COMPLEX,
                    3,
                    (0, 255, 204),
                    5)

        # ---------------------------------------------------------
        # 4. Buttons (all in 480×640 working space)
        # ---------------------------------------------------------
        bw  = 90
        bh  = 45
        gap = 15

        bottom_y = 560   # self.app.work_size_h - 80

        total_w = 5*bw + 4*gap
        start_x = (self.app.work_size_w - total_w) // 2

        self.btn_rects = {
            "Hold":  (start_x + 0*(bw+gap), bottom_y, bw, bh),
            "View":  (start_x + 1*(bw+gap), bottom_y, bw, bh),
            "UP":    (start_x + 2*(bw+gap), bottom_y, bw, bh),
            "DN":    (start_x + 3*(bw+gap), bottom_y, bw, bh),
            "OnOff": (start_x + 4*(bw+gap), bottom_y, bw, bh),
        }

        # Close button (POOL mode only)
        if self.app.display_device == "pool":
            size     = 25
            margin_x = 15
            margin_y = 15
            self.btn_rects["__CLOSE__"] = (self.app.work_size_w - size - margin_x,
                                        margin_y,
                                        size,
                                        size)

        # Suspend button
        susp_w = 200
        susp_h = 55
        susp_y = bottom_y - susp_h - 20
        susp_x = (self.app.work_size_w - susp_w) // 2

        self.btn_rects[self.app.suspendButtonText] = (susp_x, susp_y, susp_w, susp_h)

        # ---------------------------------------------------------
        # 5. Draw buttons
        # ---------------------------------------------------------
        font_face   = cv2.FONT_HERSHEY_DUPLEX
        font_scale  = 0.6
        thickness   = 1

        for name, (bx, by, bw, bh) in self.btn_rects.items():

            x1, y1 = bx, by
            x2, y2 = bx + bw, by + bh

            if name == "__CLOSE__":
                t = 2
                cv2.line(frame, (x1, y1), (x2, y2), (255,255,255), t)
                cv2.line(frame, (x2, y1), (x1, y2), (255,255,255), t)
                continue

            if name == "Hold" and self.app.hold_mode:
                fill_color = (0, 255, 255)
                label = "Vary"

            # Suspend button special coloring
            elif name == "Resume":
                fill_color = (0, 0, 200)      # RED
                label = "Resume"

            elif name == "OnOff":
                fill_color = self.app.PUMP_BTN_BGR   # light red: the pump
                label = name

            else:
                fill_color = (200, 200, 200)
                label = name

            # Recessed look while touched (held at least 0.15 s so a quick
            # tap shorter than a frame still shows): darker fill, bevel
            # reversed, label nudged down-right.
            pressed = (self._btn_key(name) == self.pressed_btn and
                       (self.mouseDown or time.time() - self.pressed_t < 0.15))
            if pressed:
                fill_color = tuple(int(c * 0.75) for c in fill_color)
                hi, sh, nudge = (120, 120, 120), (255, 255, 255), 2
            else:
                hi, sh, nudge = (255, 255, 255), (120, 120, 120), 0

            cv2.rectangle(frame, (x1, y1), (x2, y2), fill_color, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 80, 80), 2)

            # Bevel highlight (top/left) -- shadow color when pressed
            cv2.line(frame, (x1+1, y1+1), (x2-1, y1+1), hi, thickness)
            cv2.line(frame, (x1+1, y1+1), (x1+1, y2-1), hi, thickness)

            # Bevel shadow (bottom/right) -- highlight color when pressed
            cv2.line(frame, (x1+1, y2-1), (x2-1, y2-1), sh, thickness)
            cv2.line(frame, (x2-1, y1+1), (x2-1, y2-1), sh, thickness)

            # Centered text
            text_size = cv2.getTextSize(label, font_face, font_scale, thickness)[0]
            tx = x1 + ((bw - text_size[0]) // 2) + nudge
            ty = y1 + ((bh + text_size[1]) // 2) + nudge

            cv2.putText(frame, label, (tx, ty),
                        font_face, font_scale, (0,0,0),
                        thickness, cv2.LINE_AA)

        return frame

    @staticmethod
    def _btn_key(name):
        # Suspend/Resume/Begin are one button whose label changes the
        # moment it's pressed -- give it one key so it still draws pressed.
        return "Suspend" if name in ("Suspend", "Resume", "Begin") else name

    def mousePressEvent(self, event):
        self.mouse_processor("press", event)

    def mouseMoveEvent(self, event):
        self.mouse_processor("move", event)

    def mouseReleaseEvent(self, event):
        self.mouse_processor("release", event)

    def mouseDoubleClickEvent(self, event):
        self.mouse_processor("dblclick", event)

    def wheelEvent(self, event):
        self.mouse_processor("scroll", event)

    def handle_button(self, name):
        self.any_button_pressed = True
        if name in ("Suspend", "Resume", "Begin"):
            self.app.Suspend_btn_press()
        elif name == "Hold":
            self.app.Hold_btn_press()
        elif name == "View":
            self.app.View_btn_press()
        elif name == "OnOff":
            self.app.OnOff_btn_press()
        elif name == "UP":
            self.app.UP_btn_press()
        elif name == "DN":
            self.app.DN_btn_press()

    def closeEvent(self, event):
        print("QtMainWindow closeEvent triggered")
        try:
            self.app.shutdown()
        except Exception as e:
            print("Error during shutdown:", e)
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.menu_button.move(0, 0)

    def showMenu(self):
        menu = QMenu(self)

        item1 = QAction("Set Swim Area...", self)
        item1.triggered.connect(self.openPlacePoints)
        menu.addAction(item1)

        item2 = QAction("Swim Plot...", self)
        item2.triggered.connect(self.openSwimPlot)
        menu.addAction(item2)

        menu.addSeparator()

        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def _enter_submenu(self):
        self.menu_button.hide()

        # qt_update_loop's auto-pause (triggered by pause_update_loop) only
        # ever flips Start -> Pause; nothing flips it back on its own. Remember
        # what was actively recording so _exit_submenu can resume it, but only
        # if it was really running (don't override an explicit user Pause/Close).
        self._was_recording_persp = (self.myVideoCapture.makePerspectVideo == "Start")
        self._was_recording_raw   = (self.myVideoCapture.makeRawVideo == "Start")

        # Finalize the current perspective-video segment so it's safe to
        # read/scrub (e.g. in SwimPlot's video view). OpenCV's writer doesn't
        # finish the file's frame index until release() is called, so a
        # still-open segment reads back as garbled/random frames.
        if self.myVideoCapture.persp_writer is not None:
            self.myVideoCapture.persp_writer.release()
            self.myVideoCapture.persp_writer = None

    def _exit_submenu(self):
        self.menu_button.show()

        # Resume recording (into a fresh segment/file — the existing
        # new-segment logic in _perspect_video_writer handles that) if it
        # was actively running before the submenu paused it.
        if getattr(self, '_was_recording_persp', False):
            self.myVideoCapture.makePerspectVideo = "Start"
        if getattr(self, '_was_recording_raw', False):
            self.myVideoCapture.makeRawVideo = "Start"

    def openPlacePoints(self):
        self.app.pause_update_loop = True
        self.app.leave_main_screen()
        self._enter_submenu()
        dlg = PlacePointsWindow(self.app, self)
        dlg.exec()
        self._exit_submenu()
        self.app.return_to_main_screen()
        self.app.pause_update_loop = False
        QTimer.singleShot(0, self.qt_update_loop)   # <-- restart

    def openSwimPlot(self):
        self.app.pause_update_loop = True
        self.app.leave_main_screen()
        self._enter_submenu()

        # qt_update_loop only stops RESCHEDULING itself once pause_update_loop
        # is seen True — a call already queued (QTimer.singleShot) before we
        # set that flag above still runs to completion, repainting one more
        # live (button-laden) frame onto display_canvas. That queued call
        # only gets a chance to run once we start pumping events again
        # (e.g. inside the calendar's exec() below), which would repaint
        # right over our clear() and undo it. Flush it out now so it's
        # already done before we ever call clear().
        QApplication.processEvents()

        # Closing SwimPlotWindow returns to the date-range calendar (not
        # straight back to the main program) so a new date can be picked
        # without reopening SwimPlot from the menu. Only closing the
        # calendar itself exits the loop. The calendar remembers the last
        # picked range so it reappears with the same dates highlighted
        # instead of resetting to today.
        from_date, to_date = None, None
        while True:
            # Even though the calendar is now a full-screen frameless
            # dialog covering the same geometry as this window, blank the
            # main display before showing it anyway -- clear() only
            # schedules a repaint (update()), it doesn't paint
            # synchronously, and the dialog's own exec() starts a nested
            # event loop right on the next line. Without forcing that
            # repaint through first, a sliver of the actual last-rendered
            # frame (CoM bar, wherever it happened to be) can stay stuck
            # on screen for the dialog's whole lifetime -- previously
            # invisible only because the old (now-removed) title bar
            # happened to sit on top of that exact spot.
            self.display_canvas.clear()
            QApplication.processEvents()
            range_dlg = SwimDateRangeDialog(self.app, self, from_date, to_date)
            if range_dlg.exec() != QDialog.Accepted:
                break
            from_date, to_date = range_dlg.get_range()
            dlg = SwimPlotWindow(self.app, self, from_date, to_date)
            dlg.exec()

        self._exit_submenu()
        self.app.return_to_main_screen()
        self.app.pause_update_loop = False
        QTimer.singleShot(0, self.qt_update_loop)   # <-- restart

    def place_mask_in_workspace(self, mask):
        """
        Insert a zone-sized or corridor-sized mask into a full workspace frame,
        centered, without resizing or distortion.
        """
        H, W = self.app.work_size_h, self.app.work_size_w
        frame = np.zeros((H, W, 3), dtype=np.uint8)

        if mask is None or mask.size == 0:
            return frame

        # Convert to BGR
        zm = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        zh, zw = mask.shape

        # Center placement
        x0 = (W - zw) // 2
        y0 = (H - zh) // 2

        frame[y0:y0+zh, x0:x0+zw] = zm
        return frame

class MyVideoCapture:
    def __init__(self, app):
        self.app = app

        self.latest_frame = None
        self.grabber_running = False

        self.makeRawVideo = "Close"
        self.makePerspectVideo = "Close"

        self.raw_writer = None
        self.persp_writer = None
        self.video_write_stopped = False

        # ---------------------------------------------------------
        # 1. Open the video source
        # ---------------------------------------------------------
        self.vidSrc = cv2.VideoCapture(self.app.video_source)

        # ---------------------------------------------------------
        # 2. Configure camera BEFORE starting grabber
        # ---------------------------------------------------------
        if self.app.capture_device == "camera":

            # Force MJPEG (critical for 30 FPS at 1280x720)
            self.vidSrc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

            # Force resolution
            self.vidSrc.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.vidSrc.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            # Force FPS
            self.vidSrc.set(cv2.CAP_PROP_FPS, 30)

        # Keep buffer size at one so we always read the latest frame
        self.vidSrc.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # ---------------------------------------------------------
        # 3. NOW check if camera opened successfully
        # ---------------------------------------------------------
        if not self.vidSrc.isOpened():
            raise ValueError("Unable to open video source", self.vidSrc)

        # 4. Start grabber thread ONLY for camera mode

        # ⭐ Warm-up loop: absorb corrupted MJPEG frames safely
        if self.app.capture_device == "camera":
            for _ in range(30):  # ~0.6 sec max
                try:
                    ok, frame = self.vidSrc.read()
                except cv2.error:
                    # Corrupted JPEG during startup — ignore it
                    time.sleep(0.02)
                    continue

                if ok and frame is not None:
                    self.latest_frame = frame
                    break

                time.sleep(0.02)
            # ⭐ Now start grabber thread
            self.grabber_running = True
            import threading
            self.grabber_thread = threading.Thread(target=self._grabber, daemon=True)
            self.grabber_thread.start()

        else:
            self.grabber_running = False
            self.grabber_thread = None

    def getImages(self):
        
        # ------------------------------------------------------------
        # 1. Read frame (or advance video timestamp)
        # ------------------------------------------------------------
        if self.app.capture_device == "video":
            frame_is_read, rawImg = self.getVideoFrame()
        else:
            rawImg = self.latest_frame
            frame_is_read = rawImg is not None
        if not frame_is_read:
            return False, None, None

        # ------------------------------------------------------------
        # 2. NORMALIZE: resize first, then rotate
        # ------------------------------------------------------------
        # 1) Resize raw image to working size (this becomes the raw-video frame)
        raw_resized = cv2.resize(
            rawImg,
            (self.app.work_size_h, self.app.work_size_w),
            interpolation=cv2.INTER_LINEAR
        )

        # 2) Rotate the resized image upright (this becomes full_img)
        full_img = cv2.rotate(raw_resized, cv2.ROTATE_90_CLOCKWISE)

        # ------------------------------------------------------------
        # 3. Perspective transform (same size, no rotation)
        # ------------------------------------------------------------
        # ⭐ Optimization: precompute matrix once
        if not hasattr(self, "_persp_matrix_cache"):
            pts1 = np.float32(self.app.swimAreaPoints)
            pts2 = np.float32([
                [0, 0],
                [self.app.work_size_w, 0],
                [self.app.work_size_w, self.app.work_size_h],
                [0, self.app.work_size_h]
            ])
            self._persp_matrix_cache = cv2.getPerspectiveTransform(pts1, pts2)

        matrix = self._persp_matrix_cache

        perspect_img = cv2.warpPerspective(
            full_img,
            matrix,
            (self.app.work_size_w, self.app.work_size_h),
            flags=cv2.INTER_LINEAR
        )

        # ------------------------------------------------------------
        # 4. Write raw video if requested
        # ------------------------------------------------------------
        self._raw_video_writer(raw_resized)

        return True, full_img, perspect_img

    def getVideoFrame(self):
        now = time.time()

        # ------------------------------------------------------------
        # 1. First-time initialization
        # ------------------------------------------------------------
        if not hasattr(self, "video_initialized"):
            self.video_initialized = True

            # Open video file
            self.cap = cv2.VideoCapture(self.app.video_source)

            # Timing setup
            self.video_start_time = now
            self.last_call_time = now
            self.video_pause_offset = 0.0

            # Frame index tracking
            self.current_frame_index = 0
            self.last_returned_frame = None

            # From App.__init__
            self.frame_period = 1.0 / self.app.video_fps

            # Seek to starting point
            start_ms = self.app.startLater_inSeconds * 1000
            self.cap.set(cv2.CAP_PROP_POS_MSEC, start_ms)

            ok, frame = self.cap.read()
            if not ok:
                return False, None

            self.last_returned_frame = frame
            self.current_frame_index = int(self.app.startLater_inSeconds * self.app.video_fps)

            # Master clock starts NOW
            self.video_start_time = time.time()
            self.last_call_time = self.video_start_time

            return True, frame

        # ------------------------------------------------------------
        # 2. Pause compensation logic + single-step detection
        # ------------------------------------------------------------
        pause_delta = now - self.last_call_time
        single_step = pause_delta > 0.2     # VS Code break or manual stepping

        if single_step:
            # Freeze the video clock (normal behavior)
            self.video_pause_offset += pause_delta

            # BUT return the next frame anyway (new behavior)
            ok, frame = self.cap.read()
            if not ok:
                return False, None

            self.current_frame_index += 1
            self.last_returned_frame = frame

            print(f"[STEP] frame={self.current_frame_index}")

            self.last_call_time = now
            return True, frame

        # Normal running
        self.last_call_time = now

        # ------------------------------------------------------------
        # 3. Compute master-clock playback time
        # ------------------------------------------------------------
        elapsed = (now - self.video_start_time - self.video_pause_offset) * self.app.video_speed
        playback_sec = self.app.startLater_inSeconds + elapsed

        # Ideal frame index
        ideal_index = int(playback_sec / self.frame_period)

        # ------------------------------------------------------------
        # 4. CASE 1 — Too early → reuse previous frame
        # ------------------------------------------------------------
        if ideal_index == self.current_frame_index:
            return True, self.last_returned_frame

        # ------------------------------------------------------------
        # 5. CASE 2 — On time → read exactly one new frame
        # ------------------------------------------------------------
        if ideal_index == self.current_frame_index + 1:
            ok, frame = self.cap.read()
            if not ok:
                return False, None

            self.current_frame_index += 1
            self.last_returned_frame = frame

            return True, frame

        # ------------------------------------------------------------
        # 6. CASE 3 — Behind → skip ahead sequentially
        # ------------------------------------------------------------
        if ideal_index > self.current_frame_index + 1:
            frames_to_skip = ideal_index - self.current_frame_index

            frame = None
            ok = True

            for _ in range(frames_to_skip):
                ok, frame = self.cap.read()
                if not ok:
                    return False, None

            self.current_frame_index = ideal_index
            self.last_returned_frame = frame
            return True, frame

        # ------------------------------------------------------------
        # 7. CASE 4 — ideal_index < current_frame_index (should never happen)
        # ------------------------------------------------------------
        return True, self.last_returned_frame

    def _grabber(self):
        while self.grabber_running:
            ok, frame = self.vidSrc.read()
            if not ok or frame is None:
                continue   # skip bad frames instead of crashing

            self.latest_frame = frame

    def _make_filename(self, prefix):
        import datetime
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{prefix}_{ts}.mp4"
    
    def _raw_video_writer(self, full):
        if self.makeRawVideo == "Start":
            full_img = full.copy()

            if self.raw_writer is None:
                fname = self._make_filename("Raw")
                self.raw_filename = fname  # store for compression
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                self.raw_writer = cv2.VideoWriter(
                    fname,
                    fourcc,
                    30.0,
                    (self.app.work_size_h, self.app.work_size_w)
                )

            self.raw_writer.write(full_img)

        elif self.makeRawVideo == "Pause":
            pass

        elif self.makeRawVideo == "Close":
            if self.raw_writer is not None:
                self.raw_writer.release()
                self.raw_writer = None

    def _perspect_video_writer(self, perspect):

        # ------------------------------------------------------------
        # Ensure segment_id exists (initialize from app on first use)
        # ------------------------------------------------------------
        if not hasattr(self, "segment_id"):
            self.segment_id = getattr(self.app, "last_segment_id", 0)

        # ------------------------------------------------------------
        # Mid-session low-space guard. This already runs once per CSV
        # log tick (a few times/sec at most), so the disk_usage() call
        # here is effectively free -- no separate polling needed. Once
        # free space drops below the reserve, video writing stops for
        # the rest of this session (no resume, even if space frees up
        # later); CSV logging is unaffected and is what actually matters.
        # ------------------------------------------------------------
        VIDEO_WRITE_RESERVE_BYTES = 10 * 1024 * 1024

        if self.video_write_stopped:
            if getattr(self, "persp_writer", None) is not None:
                self.persp_writer.release()
                self.persp_writer = None
            return self.segment_id, getattr(self, "persp_frame_num", 0)

        if self.makePerspectVideo == "Start":
            try:
                free = shutil.disk_usage(self.app.data_dir).free
            except Exception:
                free = None
            if free is not None and free < VIDEO_WRITE_RESERVE_BYTES:
                self.video_write_stopped = True
                if getattr(self, "persp_writer", None) is not None:
                    self.persp_writer.release()
                    self.persp_writer = None
                return self.segment_id, getattr(self, "persp_frame_num", 0)

        # ------------------------------------------------------------
        # Not in Start mode → handle Close and return
        # ------------------------------------------------------------
        if self.makePerspectVideo != "Start":

            if self.makePerspectVideo == "Close":
                if getattr(self, "persp_writer", None) is not None:
                    self.persp_writer.release()
                    self.persp_writer = None

            return self.segment_id, getattr(self, "persp_frame_num", 0)

        # ------------------------------------------------------------
        # Detect new segment (no writer or closed writer)
        # ------------------------------------------------------------
        new_segment = (
            getattr(self, "persp_writer", None) is None or
            not self.persp_writer.isOpened()
        )

        if new_segment:
            # Increment segment counter and sync back to App
            self.segment_id += 1
            self.app.last_segment_id = self.segment_id

            # Reset frame counter
            self.persp_frame_num = 0

            # Build filename: YYYY-MM-DD_XX.avi
            base = str(self.app.todayCsvFile).replace(".csv", "")
            avi_path = f"{base}_{self.segment_id:02d}.avi"
            self.current_segment_file = avi_path

            # Create writer sized to perspect image
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            h, w = perspect.shape[:2]
            self.persp_writer = cv2.VideoWriter(
                avi_path,
                fourcc,
                self.app.data_recs_per_sec,
                (w, h)
            )

            if not self.persp_writer.isOpened():
                return self.segment_id, self.persp_frame_num

        # ------------------------------------------------------------
        # Build special overlay (Pace / Avg / Distance) on raw perspect
        # ------------------------------------------------------------
        perspect_img = perspect.copy()
        h, w = perspect_img.shape[:2]

        # (No CoM bar in the recording: CoM is logged to the CSV instead and
        # drawn on replay in the swim plot, toggled by left-click.)

        pace_txt = f"Pace: {Utils.DecimalToTime(self.app.swim_pace)}"
        avg_txt  = f"Avg: {self.app.avgPaceDisplay}"
        dist_txt = f"Dist: {self.app.distanceSwam}"

        font  = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.65
        thick = 2
        color = (255, 255, 255)

        y_row = h - 15   # single bottom row for all three fields

        # Avg Pace — left
        cv2.putText(perspect_img, avg_txt, (10, y_row), font, scale, color, thick, cv2.LINE_AA)

        # Pace — centered. This is self.app.swim_pace from the selected
        # algorithm (see SwimController.runAlgorithm /
        # poolwindAI_v7.39_pace_notes.txt), baked in unsmoothed per-frame;
        # the SwimPlot pace plot shows a Savitzky-Golay smoothed version
        # of the same CSV column (see SwimPlotWindow._prepare_display_arrays),
        # so the two will legitimately differ slightly.
        (text_w, _), _ = cv2.getTextSize(pace_txt, font, scale, thick)
        (char_w, _), _ = cv2.getTextSize("xx", font, scale, thick)
        x_pace = (w - text_w) // 2 - char_w
        cv2.putText(perspect_img, pace_txt, (x_pace, y_row), font, scale, color, thick, cv2.LINE_AA)

        # Distance — right
        (text_w, _), _ = cv2.getTextSize(dist_txt, font, scale, thick)
        x_dist = w - text_w - 10
        cv2.putText(perspect_img, dist_txt, (x_dist, y_row), font, scale, color, thick, cv2.LINE_AA)

        # ------------------------------------------------------------
        # Write frame and update counters
        # ------------------------------------------------------------
        self.persp_writer.write(perspect_img)
        self.persp_frame_num += 1

        return self.segment_id, self.persp_frame_num

class DisplayCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def setFrame(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def clear(self):    
        self._pixmap = None
        self.update()

    def paintEvent(self, event):
        if self._pixmap is not None:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self._pixmap)

def body_corr_spans(height, usablePoolLength):
    """
    BodyCoMCorrection's reach, in CoM units (0-1000 = the pool's length):
    (back_corr, front_corr) = back-center to toes, back-center to
    fingertips, for a swimmer `height` inches tall.

    Anatomy proportions -- from Bill's own measured reach (2026-08-27):
    35" back-center to fingertips, 56" back-center to toes, 91" combined.
    Restored after the previous 0.6/1.0 fractions (which don't even sum to
    1.0) were found to push back_corr past 500, breaking the front/back
    branch selection in BodyCoMCorrection for realistic anatomy.
    """
    L = height * 1.29                 # full body length
    front_len = L * (35 / 91)         # back-center -> fingertips
    back_len  = L * (56 / 91)         # back-center -> toes
    return (back_len / usablePoolLength) * 1000, (front_len / usablePoolLength) * 1000


def draw_zone_band_on(frame, zone, zones, level):
    """
    Lights up swim zone `zone` of `zones` across the whole frame: the
    picture is divided into `zones` equal bands, slowest (0) at the very
    bottom (back of the pool), fastest at the very top. `level` = how much
    white is blended in (0.10 is faint).

    (First drawn where the swimmer's body center has to be for the zone,
    which left the bottom and top of the picture unused; Bill, 2026-10-17:
    "when the Suspend button is pressed and the voltage goes low, the zone
    highlight shows about a third of the way up. It should be at the very
    bottom.")
    """
    if zone is None or not zones or zone < 0 or zone >= zones or level <= 0:
        return
    h, w = frame.shape[:2]
    y_top = int(round((zones - zone - 1) * h / zones))
    y_bot = int(round((zones - zone) * h / zones))
    if y_bot <= y_top:
        return
    band = frame[y_top:y_bot]
    cv2.addWeighted(band, 1.0 - level, np.full_like(band, 255), level, 0, dst=band)


def draw_com_bar_on(frame, com_h, com_w, zone_width, size_h=1000.0, size_w=700.0):
    """
    Draws the CoM bar onto `frame`, scaled to the frame's size: a horizontal
    line at com_h (0-size_h, 0 = back of the pool at the bottom of the
    image), small ticks at the swim-zone edges (zone_width = fraction of the
    width), and a longer tick at com_w (0-size_w) unless com_w is None.
    Used live (QtMainWindow.draw_com_bar) and on swim plot replay.
    """
    h, w = frame.shape[:2]
    com_y = int((size_h - com_h) * h / size_h)        # invert + scale
    cv2.line(frame, (0, com_y), (w, com_y), (255, 255, 255), 2)

    half = zone_width / 2.0
    left  = int((0.5 - half) * w)
    right = int((0.5 + half) * w)
    tick = 12  # height of the zone-edge markers
    cv2.line(frame, (left,  com_y - tick//2), (left,  com_y + tick//2), (255, 255, 255), 2)
    cv2.line(frame, (right, com_y - tick//2), (right, com_y + tick//2), (255, 255, 255), 2)

    if com_w is not None:
        com_x = int((size_w - com_w) * w / size_w)
        tick = 20  # longer than the zone-edge markers
        cv2.line(frame, (com_x, com_y - tick//2), (com_x, com_y + tick//2), (255, 255, 255), 2)

class SwimController:
    def __init__(self, app):

        # ---------------------------------------------------------
        # App access
        # ---------------------------------------------------------
        self.app = app
        self.REPdefaults = app.REPdefaults

        self.priorDesiredIndex = None

        # Loop timing
        self.lastLoopTime = None
        self.loop_dt = 0.02  # for now, should have a dynamic value

        # ---------------------------------------------------------
        # Build sorted pace/voltage arrays
        # ---------------------------------------------------------
        speed_np = np.array(self.app.speedArray)
        idx = np.argsort(speed_np[:, 0])
        self.pace_asc = speed_np[idx, 0]       # ascending pace
        self.voltage_desc = speed_np[idx, 1]   # descending voltage

        # Add these two lines for symmetry
        self.voltage_asc = self.voltage_desc[::-1]   # ascending voltage
        self.pace_desc   = self.pace_asc[::-1]       # descending pace

        # ---------------------------------------------------------
        # Compute PaceLimitsIndex (slow_index, fast_index)
        # ---------------------------------------------------------
        slow_pace, fast_pace = self.app.PaceLimitsDec
        slow_voltage = self._get_voltage_from_pace(slow_pace)
        fast_voltage = self._get_voltage_from_pace(fast_pace)

        slow_index = self.app.findClosestPlateauIndex(
            slow_voltage,
            self.app.noiseAllowedPercent_desired,
            self.app.plateau_voltages
        )

        fast_index = self.app.findClosestPlateauIndex(
            fast_voltage,
            self.app.noiseAllowedPercent_desired,
            self.app.plateau_voltages
        )

        self.PaceLimitsIndex = (slow_index, fast_index)

    # Defaults-file key selecting the algorithm (hot-reloadable).
    ALGO_KEY = App.KEY_ALGO
    ALGORITHMS = ("basic", "swimmerPace")

    def runAlgorithm(self, CoM, timestamp, pool_pace):
        """
        Runs the algorithm selected in the defaults file and returns
        (desiredIndex, swim_pace). Everything upstream (CoM smoothing,
        BodyCoMCorrection, voltage/pool_pace smoothing) and downstream
        (relays, logging, display) is shared infrastructure; only what
        happens in here differs between algorithms.
        """
        # A developer choice since 2026-10-17, from the main defaults file
        # only (a stick's line is ignored), whatever developerMode is.
        name = self.app.REPdefaults.get(self.ALGO_KEY, "swimmerPace")
        if name not in self.ALGORITHMS:
            if getattr(self, "_bad_algo_name", None) != name:
                print(f"Unknown algorithm {name!r} in defaults -- using 'swimmerPace'")
                self._bad_algo_name = name
            name = "swimmerPace"

        if name != getattr(self, "_active_algo", None):
            # Switched (or first run): restart any algorithm state so the
            # new one starts clean instead of from the other's leftovers.
            print(f"Algorithm: {name}")
            self._active_algo = name
            self._est_last_t = None
            self._ema_swim_pace = None

        if name == "swimmerPace":
            desiredIndex, swim_pace = self._swimmerPaceAlgo(CoM, timestamp, pool_pace)
        else:
            desiredIndex, swim_pace = self._basicAlgo(CoM, timestamp, pool_pace)

        self.priorDesiredIndex = desiredIndex
        return desiredIndex, swim_pace

    def _basicAlgo(self, CoM, timestamp, pool_pace):
        """
        Simplest possible algorithm, for testing the infrastructure:
        CoM (already smoothed and BodyCoMCorrection'd to 0-1000) maps
        linearly to a desired pace/plateau, and swim_pace = pool_pace
        (no estimator).
        """
        app = self.app

        # 1-4. CoM -> pace -> voltage -> plateau index
        desiredIndex = self._index_for_CoM(CoM)

        # 5. swim_pace is simply pool_pace (trace columns match)
        app._trace_v_water = 100.0 / max(pool_pace, 0.1)
        app._trace_v_drift = 0.0
        app._trace_est = pool_pace

        return desiredIndex, pool_pace

    def _zone_steps(self):
        """
        The jet steps the pool is divided into, slowest first, as plateau
        indexes. Taken from pace_voltage:
          - only paces inside PaceLimitsDec (a limit that falls between two
            table paces snaps INWARD, so the jet never goes past the limit
            the swimmer chose);
          - only voltages the jet may actually reach (<= the safety max), so
            no part of the pool asks for a speed it can't get;
          - entries within 0.01 V of the previous kept one are treated as
            the same step (e.g. 1.185 / 1.186).
        Cached; recomputed if PaceLimitsDec or SafetyVoltageLimits change
        (e.g. a swimmer's USB stick is set up mid-session).
        """
        app = self.app
        key = (tuple(app.PaceLimitsDec), tuple(app.SafetyVoltageLimits))
        if getattr(self, "_zone_steps_key", None) != key:
            slow_pace, fast_pace = app.PaceLimitsDec
            _, maxV = app.SafetyVoltageLimits
            steps = []
            for i, v in enumerate(app.plateau_voltages):          # ascending voltage = faster
                pace = app.speedArray[i][0]
                if fast_pace - 1e-6 <= pace <= slow_pace + 1e-6 and v <= maxV + 1e-6:
                    if steps and v - app.plateau_voltages[steps[-1]] < 0.01:
                        continue
                    steps.append(i)
            if not steps:   # limits outside the table: fall back to the nearest step
                mid_v = self._get_voltage_from_pace((slow_pace + fast_pace) / 2)
                steps = [app.findClosestPlateauIndex(
                    mid_v, app.noiseAllowedPercent_desired, app.plateau_voltages)]
            self._zone_steps_cache = steps
            self._zone_steps_key = key
            print("Zone steps (reachable, inside PaceLimits): " + ", ".join(Utils.DecimalToTime(app.speedArray[i][0]) for i in steps)
                  + f"  ({len(steps)} zones of {1000.0 / len(steps):.0f} CoM)")
        return self._zone_steps_cache

    def _index_for_CoM(self, CoM):
        """
        CoM (0-1000) -> desired plateau index. The pool is divided into
        equal-width zones, one per reachable jet step between the
        PaceLimits (_zone_steps), slowest at the back.

        Since v7.43. Up to v7.42, CoM was spread linearly over PACE and
        rounded to the nearest step, which squeezed the fast steps into
        1-2 inch zones (the calibrated steps bunch together at the fast
        end) and left the front of the pool asking for speeds above the
        safety limit. Even zones fixed the "ping-pong" feel in the pool
        (pace notes sections 17-19).
        """
        steps = self._zone_steps()
        n = len(steps)
        k = int(max(0.0, min(1000.0, CoM)) / 1000.0 * n)
        return steps[min(n - 1, k)]

    # How far past the halfway point between two steps the voltage must go
    # before the highlight moves to the next zone, as a fraction of the gap:
    # 0.25 = three quarters of the way to the next step (the 75% the
    # "Schmitt trigger" in findClosestPlateauIndex was meant to have).
    JET_ZONE_HYSTERESIS = 0.25

    def jet_zone(self, volts):
        """
        The zone (0 = slowest, at the back) whose jet step the pool is on
        now, from the smoothed Pace Display voltage, for the swim zone
        highlight. Returns (zone, number of zones), or (None, n) when the
        jet is outside the zones (below the slow limit after a wind-down,
        above the fast limit).

        Real hysteresis (Bill, 2026-10-16: "valveIndex is fine as the basis
        for highlighting. It shows what the pool is doing in relationship
        to what the swimmer is doing."): it remembers the zone it showed
        and moves to a neighbour only when the voltage is past the halfway
        point plus JET_ZONE_HYSTERESIS of the gap, so it can't flicker on
        an edge. Zones come from _zone_steps, which already treats
        near-duplicate steps (1.185 / 1.186 V) as one.
        """
        # Smoothed first with the WATER LAG, WATER_TAU seconds (the same lag
        # the Swimmer Pace estimator gives the water after a jet step), so
        # the band moves when the water has caught up, not when the voltage
        # steps. Time-based, so the loop speed doesn't change it; WATER_TAU
        # is read every pass (hot reload). Display only: the relay drive
        # doesn't see it. (Bill, 2026-10-17: first 'Zone_HL_alpha' per
        # loop pass "to keep it from jumping around so much", then: "The
        # EMF delay could actually represent the lag in moving the mass of
        # water after a voltage change." -> "use WATER_TAU for the zone
        # highlight smoothing.")
        now = time.time()
        try:
            tau = max(0.05, float(self.app.REPdefaults.get("WATER_TAU", 5.0)))
        except (TypeError, ValueError):
            tau = 5.0
        # In Hold the band follows the jet directly (Bill, 2026-10-17: with
        # the smoothing, UP/DN in Hold made the highlight "slow or jumpy");
        # leaving Hold, the smoothing carries on from where the jet is.
        prev = getattr(self, "_zhl_volts", None)
        last_t = getattr(self, "_zhl_t", None)
        if prev is not None and last_t is not None and not self.app.hold_mode:
            dt = max(0.0, now - last_t)
            volts = prev + (1.0 - math.exp(-dt / tau)) * (volts - prev)
        self._zhl_volts = volts
        self._zhl_t = now

        steps = self._zone_steps()
        V = [self.app.plateau_voltages[i] for i in steps]
        n = len(V)
        if n == 0:
            return None, 0
        if getattr(self, "_jet_zone_key", None) != self._zone_steps_key:
            self._jet_zone = None             # zones changed (e.g. a stick's limits)
            self._jet_zone_key = self._zone_steps_key

        # Outside the zones by more than half a step: no highlight
        gap_lo = (V[1] - V[0]) if n > 1 else 0.05
        gap_hi = (V[-1] - V[-2]) if n > 1 else 0.05
        if volts < V[0] - gap_lo / 2 or volts > V[-1] + gap_hi / 2:
            self._jet_zone = None
            return None, n

        z = self._jet_zone
        if z is None or z >= n:
            z = min(range(n), key=lambda i: abs(volts - V[i]))
        else:
            h = self.JET_ZONE_HYSTERESIS
            while z < n - 1 and volts > (V[z] + V[z + 1]) / 2 + h * (V[z + 1] - V[z]):
                z += 1
            while z > 0 and volts < (V[z] + V[z - 1]) / 2 - h * (V[z] - V[z - 1]):
                z -= 1
        self._jet_zone = z
        return z, n

    def _swimmerPaceAlgo(self, CoM, timestamp, pool_pace):
        """
        Same jet target as _basicAlgo (calls it, so infrastructure fixes
        there apply here too), plus the speed-domain Swimmer Pace estimator
        for swim_pace and a final alpha=0.1 smoothing.
        """
        desiredIndex, _ = self._basicAlgo(CoM, timestamp, pool_pace)

        raw_swim_pace = self._estimate_swim_pace(timestamp, pool_pace)
        self.app._trace_est = raw_swim_pace

        if getattr(self, "_ema_swim_pace", None) is None:
            self._ema_swim_pace = raw_swim_pace
        else:
            alpha = 0.1
            self._ema_swim_pace = alpha * raw_swim_pace + (1 - alpha) * self._ema_swim_pace

        return desiredIndex, self._ema_swim_pace

    def _estimate_swim_pace(self, timestamp, pace_from_voltage):
        """
        Estimate swimmer pace in the SPEED domain (yd/min), not by adding a
        fudge to pace (pace = 100/speed is inverse, so adding is wrong):

            swim_speed = lagged_water_speed + DRIFT_SCALE * drift_speed

        - lagged_water_speed: pool speed from voltage (100/pool_pace),
          low-passed with WATER_TAU seconds. The jet's water doesn't jump
          when the voltage plateau steps -- it takes time to catch up --
          so this smooths the index-zone steps.
        - drift_speed: swimmer's speed across the pool floor, from the RAW
          blob position (blob_CoM_h, NOT the height-compensated CoM_h --
          that one is stretched 1.66x-2.74x by BodyCoMCorrection and would
          distort the drift), converted to real inches via usablePoolLength,
          smoothed with DRIFT_TAU seconds. Moving toward the fast end
          (higher CoM_h) = swimming faster than the water, so it lowers
          pace. Only used while swimmerFound.
        Both filters preserve the long-run mean, so avg(swim_pace) still
        converges to avg(pool_pace) (see poolwindAI_v7.39_pace_notes.txt).
        """
        app = self.app
        pool_pace = pace_from_voltage
        v_pool = 100.0 / max(pool_pace, 0.1)          # yd/min

        last_t = getattr(self, "_est_last_t", None)
        self._est_last_t = timestamp
        if last_t is None or timestamp - last_t <= 0 or timestamp - last_t > 2.0:
            # First sample, bad timestamp, or a long stall (submenu pause,
            # etc.): restart the filters from the current values.
            self._est_v_water = v_pool
            self._est_pos_s = None
            app._trace_v_water = v_pool
            app._trace_v_drift = 0.0
            return pool_pace
        dt = timestamp - last_t

        # Lagged water speed
        tau_w = max(0.05, float(app.REPdefaults.get("WATER_TAU", 2.0)))
        self._est_v_water += (1.0 - math.exp(-dt / tau_w)) * (v_pool - self._est_v_water)

        # Drift speed from raw (uncorrected) blob position
        blob_h = getattr(app.window, "blob_CoM_h", None)
        found = getattr(app.window, "swimmerFound", False)
        v_drift = 0.0
        if found and blob_h is not None:
            _, usablePoolLength = app.REPdefaults["swimmersHeight,usablePoolLength"]
            pos_in = blob_h / app.CoM_size_h * usablePoolLength      # inches
            if getattr(self, "_est_pos_s", None) is None:
                self._est_pos_s = pos_in
            else:
                tau_d = max(0.05, float(app.REPdefaults.get("DRIFT_TAU", 2.0)))
                prev = self._est_pos_s
                self._est_pos_s = prev + (1.0 - math.exp(-dt / tau_d)) * (pos_in - prev)
                v_drift = (self._est_pos_s - prev) / dt * (60.0 / 36.0)   # in/s -> yd/min
        else:
            self._est_pos_s = None      # no re-entry step from a stale position

        # Glitch guard: no real swimmer drifts faster than this
        cap = float(app.REPdefaults.get("DRIFT_MAX", 15.0))
        app._pace_check_estimator_calls = getattr(app, "_pace_check_estimator_calls", 0) + 1
        if abs(v_drift) > cap:
            v_drift = cap if v_drift > 0 else -cap
            app._pace_check_drift_capped = getattr(app, "_pace_check_drift_capped", 0) + 1

        # DRIFT_SCALE is now a plain gain: 1.0 = full physical drift,
        # <1.0 trusts it less (blob centroid is noisy -- see notes).
        gain = app.REPdefaults["DRIFT_SCALE"]
        v_swim = max(1.0, self._est_v_water + gain * v_drift)
        swim_pace_est = 100.0 / v_swim

        min_pace = 0.5   # faster than this is unrealistic
        max_pace = 5.0   # slower than this is unrealistic
        if swim_pace_est < min_pace or swim_pace_est > max_pace:
            swim_pace_est = min(max_pace, max(min_pace, swim_pace_est))
            app._pace_check_pace_clamped = getattr(app, "_pace_check_pace_clamped", 0) + 1

        app._trace_v_water = self._est_v_water
        app._trace_v_drift = v_drift
        return swim_pace_est

    def _get_voltage_from_pace(self, pace):
        return float(np.interp(pace, self.pace_asc, self.voltage_desc))

    def _get_pace_from_voltage(self, voltage):
        return float(np.interp(voltage, self.voltage_asc, self.pace_desc))

class GPIOWrapper:
    """
    Drop-in replacement for RPi.GPIO using lgpio on Raspberry Pi 5.
    Supports:
        - BCM pin numbering
        - setup(pin, OUT)
        - output(pin, True/False)
        - cleanup()
    """

    OUT = "out"

    def __init__(self):
        # Open the RP1 GPIO chip
        self.chip = lgpio.gpiochip_open(0)
        self.claimed_pins = set()
        self.released_pins = set()   # disconnected while off the main screen

    def setwarnings(self, value):
        pass  # no warnings in lgpio

    def setmode(self, mode):
        pass  # BCM is the only mode on Pi 5

    def setup(self, pin, direction):
        # Ignore pin if simulate mode assigned pin=None
        if pin is None:
            return

        if direction == self.OUT:
            # Level 1 = relay OFF (the relay board is active low), so the
            # relay doesn't flick on for an instant while being claimed.
            lgpio.gpio_claim_output(self.chip, pin, 1)
            self.claimed_pins.add(pin)
            self.released_pins.discard(pin)

    def release(self, pin):
        """Disconnect an output: the pin becomes an input, so the relay
        board gets no signal at all (its relay can't switch on), and
        output() ignores the pin until reclaim()."""
        if pin is None or pin in self.released_pins:
            return
        lgpio.gpio_write(self.chip, pin, 1)          # relay OFF first
        lgpio.gpio_claim_input(self.chip, pin)
        self.released_pins.add(pin)

    def reclaim(self, pin):
        """Make a released pin an output again, starting OFF."""
        if pin is None or pin not in self.released_pins:
            return
        self.setup(pin, self.OUT)

    def output(self, pin, value):
        # Ignore pin if simulate mode assigned pin=None, or while released
        if pin is None or pin in self.released_pins:
            return

        # App logic: True = ON, False = OFF
        # Relay board: LOW = ON, HIGH = OFF
        # Therefore invert the write:
        # lgpio.gpio_write(self.chip, pin, 0 if value else 1)
        # DEBUG - problem here when shutting down with suspend button active
        lgpio.gpio_write(self.chip, pin, 1 if value else 0)
       
    def cleanup(self):
        for pin in self.claimed_pins:
            try:
                lgpio.gpio_free(self.chip, pin)
            except:
                pass
        lgpio.gpiochip_close(self.chip)

class Utils:
    # To use in functions, place:
    # from Utils import Utils
    # then:
    # # Utils.MakePNG(best_img, "A_best.png")
    # Utils.MakeMaskTXT(best_mask, "A_mask.txt")
    # Utils.MakeMaskedHSV(hsv, best_mask, "B_masked.png")
    # Utils.DumpHSVpixels(pixels, "B_pixels.txt")
    # Utils.DumpMedianHSV(H, S, V, "B_median.txt")

    @staticmethod
    def DecimalToTime(decimalIn):
        s_min = math.trunc(decimalIn)
        s_dec = decimalIn - s_min
        s_sec = math.trunc(round(s_dec * 60, 0))

        if s_sec > 9:
            return f"{s_min}:{s_sec}"
        else:
            return f"{s_min}:0{s_sec}"

    @staticmethod
    def MakePNG(img, filename):
         # return
        """Save any image (BGR, HSV, or mask) as a PNG."""
        cv2.imwrite(filename, img)

    @staticmethod
    def MakeMaskTXT(mask, filename):
        """Save a binary mask as ASCII (# for 255, . for 0)."""
        with open(filename, "w") as f:
            f.write("\n".join(
                "".join('#' if v else '.' for v in row)
                for row in mask
            ))

    @staticmethod
    def MakeGrayTXT(gray_img, filename):
        """Save grayscale image as ASCII (# for bright, . for dark)."""
        with open(filename, "w") as f:
            f.write("\n".join(
                "".join('#' if v > 128 else '.' for v in row)
                for row in gray_img
            ))

    @staticmethod
    def DumpHSVpixels(pixels, filename):
        """Dump list of HSV pixels to a text file."""
        with open(filename, "w") as f:
            for (h, s, v) in pixels:
                f.write(f"{h},{s},{v}\n")

    @staticmethod
    def DumpMedianHSV(H, S, V, filename):
        """Dump median HSV values."""
        with open(filename, "w") as f:
            f.write(f"H={H}, S={S}, V={V}\n")

    @staticmethod
    def MakeMaskedHSV(hsv_img, mask, filename):
        """Save HSV image with pool blacked out."""
        masked = hsv_img.copy()
        masked[mask == 0] = (0, 0, 0)
        bgr = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
        cv2.imwrite(filename, bgr)

    _elapsed_timers = {}
    @staticmethod
    def measureElapsedTime(label, edge):
        now = time.time()
        timers = Utils._elapsed_timers

        if edge.lower() == "begin":
            if label not in timers and len(timers) >= 5:
                print(f"[TIMER] Ignored '{label}' (max timers reached)")
                return
            timers[label] = now
            #print(f"[TIMER INIT] {label}")
            return

        elif edge.lower() == "end":
            if label not in timers:
                print(f"[TIMER] End ignored for '{label}' (no active timer)")
                return
            elapsed = now - timers[label]
            #print(f"[TIMER] {label}: {elapsed:.6f} seconds")
            print(f" {elapsed:.6f} seconds")
            timers.pop(label, None)
            return

        else:
            print(f"[TIMER] Unknown edge '{edge}' for label '{label}'")


    @staticmethod
    def DumpTXT(text, filename):
        with open(filename, "a") as f:   # <-- append instead of overwrite
            f.write(text + "\n")

class SimulatedValve:
    def __init__(self, app):
        self.app = app

        # Timing characteristics (realistic)
        self.min_press_up = 0.040
        self.min_press_dn = 0.060
       
        self.interval_up = 0.897
        self.interval_dn = 0.894

        # Simulation state
        self.up_pressed = False
        self.dn_pressed = False
        self.press_start_time = None
        self.last_step_time = time.time()

        # Noise (optional)
        self.noise = 0.00

        # Limits based on plateau count
        self.max_index = len(self.app.plateau_voltages) - 1
        self.min_index = 1

    def sim_UP_relay_on(self):
        self.dn_pressed = False      # force DN off
        if not self.up_pressed:
            self.up_pressed = True
            self.press_start_time = time.time()

    def sim_DN_relay_on(self):
        self.up_pressed = False      # force UP off
        if not self.dn_pressed:
            self.dn_pressed = True
            self.press_start_time = time.time()

    def sim_relay_off(self):
        self.up_pressed = False
        self.dn_pressed = False

    def sim_takeReading(self):
        idx = self.app.valveIndex
        idx = max(self.min_index, min(self.max_index, idx))
        base_v = self.app.plateau_voltages[idx]
        return base_v + random.uniform(-self.noise, self.noise)

    def sim_update(self):
        now = time.time()

        # No button pressed ? no movement
        if not (self.up_pressed or self.dn_pressed):
            return
        
        # Safety: never allow both relays active
        if self.up_pressed and self.dn_pressed:
            # force safe state
            self.up_pressed = False
            self.dn_pressed = False
            return


        # How long has the button been held?
        press_duration = now - self.press_start_time

        # Determine direction + timing
        if self.up_pressed:
            if press_duration < self.min_press_up:
                return
            interval = self.interval_up
            direction = +1
        else:
            if press_duration < self.min_press_dn:
                return
            interval = self.interval_dn
            direction = -1

        # Enforce mechanical delay between steps
        if now - self.last_step_time < interval:
            return

        # Perform a step
        new_index = self.app.valveIndex + direction

        # Clamp to limits
        new_index = max(self.min_index, min(self.max_index, new_index))

        # Update state
        self.app.valveIndex = new_index
        self.last_step_time = now

class PlacePointsCanvas(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app

        # Load working-space image (480×640)
        self._load_snapshot()

        # Points stored in WORKING SPACE (480×640)
        self.points = []
        self.drag_index = None
        self.drag_radius = 12

        # Canvas fills the entire PlacePointsWindow
        self.setMouseTracking(True)

    def _load_snapshot(self):
        time.sleep(3)  # give user time to move away

        # Throw away stale frames
        for _ in range(5):
            self.app.myVideoCapture.vidSrc.read()

        ok, full_img, perspect_img = \
            self.app.myVideoCapture.getImages()

        # full_img is already 480×640
        rgb = cv2.cvtColor(full_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.full_img_pixmap = QPixmap.fromImage(qimg)

    # ---------------------------------------------------------
    # Convert mouse → working space (480×640)
    # ---------------------------------------------------------
    def convert_mouse_to_working(self, event):
        win_w = self.width()
        win_h = self.height()

        fw = int(event.position().x() * (self.app.work_size_w / win_w))
        fh = int(event.position().y() * (self.app.work_size_h / win_h))

        fw = max(0, min(479, fw))
        fh = max(0, min(639, fh))

        return fw, fh

    # ---------------------------------------------------------
    # Paint: stretch working image to window size
    # ---------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Stretch 480×640 → window_w × window_h
        scaled = self.full_img_pixmap.scaled(
            self.width(), self.height(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )

        painter.drawPixmap(0, 0, scaled)

        # Draw lines if 4 points exist
        if len(self.points) == 4:
            ul, ur, lr, ll = self.get_sorted_placePoints()

            painter.setPen(QPen(QColor(0, 255, 255), 2))
            draw_pts = [ul, ur, lr, ll]

            for i in range(4):
                p1 = self._to_display(draw_pts[i])
                p2 = self._to_display(draw_pts[(i + 1) % 4])
                painter.drawLine(p1, p2)

        # Draw points
        painter.setBrush(QBrush(QColor(255, 255, 0)))
        painter.setPen(QPen(QColor(0, 0, 0), 1))

        for p in self.points:
            dp = self._to_display(p)
            painter.drawEllipse(dp, 6, 6)

        # Instructions
        if True: #len(self.points) == 0:
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 14, QFont.Bold))

            text = (
                "Click the 4 corners of swim area.\n"
                "Follow the inner benches except rear.\n"
                "Click on the water surface.\n"
                "\n"
                "Left-click to place or drag.\n"
                "Reset to start over.\n"
                "Save when finished."
            )

            rect = painter.boundingRect(self.rect(), Qt.AlignCenter, text)
            painter.fillRect(rect.adjusted(-10, -10, 10, 10), QColor(0, 0, 0, 140))
            painter.drawText(rect, Qt.AlignCenter, text)

    # ---------------------------------------------------------
    # Convert working-space point → display-space point
    # ---------------------------------------------------------
    def _to_display(self, p):
        x, y = p
        dx = int(x * (self.width() / self.app.work_size_w))
        dy = int(y * (self.height() / self.app.work_size_h))
        return QPoint(dx, dy)

    # ---------------------------------------------------------
    # Mouse handling
    # ---------------------------------------------------------
    def _find_point_at(self, fw, fh):
        for i, (px, py) in enumerate(self.points):
            if math.hypot(px - fw, py - fh) <= self.drag_radius:
                return i
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            fw, fh = self.convert_mouse_to_working(event)

            idx = self._find_point_at(fw, fh)
            if idx is not None:
                self.drag_index = idx
            else:
                if len(self.points) < 4:
                    self.points.append((fw, fh))
                    self.update()

    def mouseMoveEvent(self, event):
        if self.drag_index is not None:
            fw, fh = self.convert_mouse_to_working(event)
            self.points[self.drag_index] = (fw, fh)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_index = None

    # ---------------------------------------------------------
    # Reset points to corners
    # ---------------------------------------------------------
    def reset_points(self):
        self.points = [
            (5, 5),
            (475, 5),
            (475, 635),
            (5, 635)
        ]
        self.drag_index = None
        self.update()

    # ---------------------------------------------------------
    # UL, UR, LR, LL ordering
    # ---------------------------------------------------------
    def get_sorted_placePoints(self):
        if len(self.points) != 4:
            return None

        pts = list(self.points)
        pts_sorted = sorted(pts, key=lambda p: p[1])  # top → bottom
        top = sorted(pts_sorted[:2], key=lambda p: p[0])
        bottom = sorted(pts_sorted[2:], key=lambda p: p[0])

        ul, ur = top
        ll, lr = bottom

        return [ul, ur, lr, ll]

class PlacePointsWindow(QDialog):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.app = app

        self.setWindowTitle("Place Swim Area Corners")
        self.setModal(True)

        # Window matches QtMainWindow size
        self.setFixedSize(self.app.window_w, self.app.window_h)

        # Force window to top-left corner
        self.move(0, 0)

        # Canvas fills the window
        self.canvas = PlacePointsCanvas(app, self)
        self.canvas.setGeometry(0, 0, self.width(), self.height())

        # ⭐ REQUIRED FIXES — these stop truncation ⭐
        self.setContentsMargins(0, 0, 0, 0)
        self.canvas.setContentsMargins(0, 0, 0, 0)

        # Load existing points (already 480×640)
        if self.app.swimAreaPoints and len(self.app.swimAreaPoints) == 4:
            self.canvas.points = self.app.swimAreaPoints[:]
            self.canvas.update()

        # Buttons
        self.save_button = QPushButton("Save", self)
        self.reset_button = QPushButton("Reset", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.save_button.clicked.connect(self.on_save)
        self.reset_button.clicked.connect(self.on_reset)
        self.cancel_button.clicked.connect(self.reject)

        # Position buttons at top-right
        btn_y = 10
        spacing = 10

        self.save_button.move(self.width() - self.save_button.width() - 10, btn_y)
        self.cancel_button.move(self.save_button.x() - self.cancel_button.width() - spacing, btn_y)
        self.reset_button.move(self.cancel_button.x() - self.reset_button.width() - spacing, btn_y)

    def on_reset(self):
        self.canvas.reset_points()

    def on_save(self):
        swim_area_window = self.canvas.get_sorted_placePoints()
        if swim_area_window is None:
            print("Need exactly 4 points before saving.")
            return

        # Keep window-space points for current session
        self.app.swimAreaPoints = swim_area_window
        if hasattr(self.app, "window"):
            self.app.window.myVideoCapture.swimAreaPoints = swim_area_window
            # Force perspective matrix to be recomputed with the new corners
            if hasattr(self.app.window.myVideoCapture, "_persp_matrix_cache"):
                del self.app.window.myVideoCapture._persp_matrix_cache

        if self.app.capture_device == "camera":
            self.app.REPdefaults["swimAreaPoints"] = swim_area_window
            self.app.calibration["swimAreaPoints"] = swim_area_window
            try:
                self.app.save_calibration()
            except Exception as e:
                print("Error saving the calibration file:", e)
        else:
            # Video mode (desk testing): used for this run only. Each test
            # video's points are set in the code next to its file name.
            line = f"self.swimAreaPoints = {swim_area_window!r}"
            print("Swim Area not saved to defaults (video mode). To keep it, paste into the program:")
            print("    " + line)
            box = QMessageBox(self)
            box.setWindowTitle("Set Swim Area")
            box.setText("Swim Area not saved to defaults (video mode).\n\n"
                        "It is used until the program closes. To keep it, paste this\n"
                        "line into the program next to the video's file name\n"
                        "(also printed in the terminal):\n\n" + line)
            box.setTextInteractionFlags(Qt.TextSelectableByMouse)
            box.exec()

        self.accept()

class _MonthOnlyCalendar(QCalendarWidget):
    """
    Qt's default QCalendarWidget paints previous/next month's padding days
    in a fixed gray and ignores any per-date QTextCharFormat set via
    setDateTextFormat() for them — so the bold-green "has data" marking
    that works fine for in-month days never shows up on those adjacent
    cells. Only way around it is a full manual paintCell for those cells
    specifically (in-month cells still go through the normal
    super().paintCell(), so their look — including selection highlight —
    is unchanged).

    Also overlays a small avg-pace line under the day number for any date
    with swim data (see setAvgPaceSource) -- computed lazily per displayed
    month rather than for the whole history up front, and cached in a
    dict shared between both calendars in SwimDateRangeDialog so
    revisiting an already-computed month (in either calendar) is free.
    """
    def setDataDates(self, data_dates):
        self._data_dates = set(data_dates)

    def setAvgPaceSource(self, data_dir, cache, months_loaded):
        # cache: date -> "M:SS" string (or None if that date's CSV had no
        # usable pace). months_loaded: set of (year, month) already
        # scanned. Both are shared (same dict/set object) with the other
        # calendar in the dialog, so pace computed while browsing one
        # calendar is instantly available in the other.
        self._pace_data_dir = data_dir
        self._avg_pace_cache = cache
        self._avg_pace_months_loaded = months_loaded
        self.currentPageChanged.connect(self._on_page_changed)
        self._on_page_changed(self.yearShown(), self.monthShown())

    def _on_page_changed(self, year, month):
        key = (year, month)
        if key not in self._avg_pace_months_loaded:
            self._avg_pace_months_loaded.add(key)
            self._load_month_averages(year, month)
        self.updateCells()

    def _load_month_averages(self, year, month):
        days_in_month = QDate(year, month, 1).daysInMonth()
        for day in range(1, days_in_month + 1):
            d = date(year, month, day)
            if d not in getattr(self, "_data_dates", ()) or d in self._avg_pace_cache:
                continue
            self._avg_pace_cache[d] = self._compute_avg_pace_for_date(d)

    def _compute_avg_pace_for_date(self, d):
        # Distance/time-weighted, gap-aware -- matches the live "Avg
        # Pace" display's formula (App.accrue_log_disp / UpdateLoop),
        # not a flat mean of the CSV's raw per-row pace column.
        GAP_SEC = 3
        YARDS_PER_MILE = 1760.0
        csv_path = os.path.join(self._pace_data_dir, f"{d.isoformat()}.csv")
        try:
            prev_t = None
            total_swimtime_min = 0.0
            final_distance = 0.0
            with open(csv_path, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) < 3:
                        continue
                    try:
                        t = float(parts[0])
                        dist = float(parts[2])
                    except ValueError:
                        continue
                    if prev_t is not None:
                        dt_sec = t - prev_t
                        if dt_sec <= GAP_SEC:
                            total_swimtime_min += dt_sec / 60.0
                    prev_t = t
                    final_distance = dist
        except OSError:
            return None

        if total_swimtime_min <= 0 or final_distance <= 0:
            return None
        avg_rate = final_distance / total_swimtime_min          # miles/min
        avg_pace = (100.0 / YARDS_PER_MILE) / avg_rate          # min per 100yd
        return Utils.DecimalToTime(avg_pace)

    def paintCell(self, painter, rect, qdate):
        if qdate.month() == self.monthShown() and qdate.year() == self.yearShown():
            super().paintCell(painter, rect, qdate)
        else:
            painter.save()
            painter.fillRect(rect, self.palette().color(QPalette.Base))

            d = date(qdate.year(), qdate.month(), qdate.day())
            if d in getattr(self, "_data_dates", ()):
                painter.setPen(QColor("green"))
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
            else:
                painter.setPen(QColor(170, 170, 170))   # same muted gray Qt uses normally

            painter.drawText(rect, Qt.AlignCenter, str(qdate.day()))
            painter.restore()

        # Avg-pace overlay, drawn on top of whichever day-number painting
        # happened above, for both in-month and padding-month cells.
        pace_txt = getattr(self, "_avg_pace_cache", {}).get(
            date(qdate.year(), qdate.month(), qdate.day())
        )
        if pace_txt:
            painter.save()
            font = painter.font()
            font.setBold(False)
            font.setPointSize(max(6, font.pointSize() - 3))
            painter.setFont(font)
            painter.setPen(QColor("blue"))
            # Bottom-aligned, inside the cell: Qt 6 (PySide6) clips each
            # cell's painting to its rect, so the old nudge below the
            # bottom edge cut the numbers off. The cell is tall enough
            # for the day number above it.
            pace_rect = rect.adjusted(0, 0, 0, -1)
            painter.drawText(pace_rect, Qt.AlignHCenter | Qt.AlignBottom, pace_txt)
            painter.restore()

class USBDriveSetupDialog(QDialog):
    """
    Shown when App finds a removable USB drive with no
    poolwind_ind_defaults.txt on it. Collects the three swimmer-specific
    values, gated behind an explicit "I understand this erases the drive"
    checkbox before OK can be pressed -- App only formats the drive after
    this dialog is accepted.
    """
    def __init__(self, mount_path, size_bytes, parent=None, default_min_pace=None, default_max_pace=None):
        super().__init__(parent)
        self.setWindowTitle("New USB Drive Detected")
        self._result = None

        size_gb = size_bytes / (1024 ** 3)

        layout = QVBoxLayout(self)

        info = QLabel(
            f"A new USB drive was found at:\n{mount_path}  (~{size_gb:.1f} GB)\n\n"
            "Set it up as a personal swimmer drive?"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        warn = QLabel("This will ERASE ALL DATA currently on the drive.")
        warn.setStyleSheet("color: red; font-weight: bold;")
        warn.setWordWrap(True)
        layout.addWidget(warn)

        form = QtWidgets.QFormLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setMaxLength(11)
        form.addRow("Name (for drive label):", self.name_edit)

        self.height_edit = QtWidgets.QDoubleSpinBox()
        self.height_edit.setRange(0, 999)
        self.height_edit.setDecimals(0)
        form.addRow("Swimmer height (inches):", self.height_edit)

        self.min_pace_edit = QtWidgets.QDoubleSpinBox()
        self.min_pace_edit.setRange(0, 99)
        self.min_pace_edit.setDecimals(2)
        if default_min_pace is not None:
            self.min_pace_edit.setValue(default_min_pace)
        form.addRow("Fastest (min) pace:", self.min_pace_edit)

        self.max_pace_edit = QtWidgets.QDoubleSpinBox()
        self.max_pace_edit.setRange(0, 99)
        self.max_pace_edit.setDecimals(2)
        if default_max_pace is not None:
            self.max_pace_edit.setValue(default_max_pace)
        form.addRow("Slowest (max) pace:", self.max_pace_edit)

        layout.addLayout(form)

        self.confirm_check = QCheckBox("I understand this will erase all data on the drive")
        layout.addWidget(self.confirm_check)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.ok_button = buttons.button(QtWidgets.QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        self.confirm_check.toggled.connect(self.ok_button.setEnabled)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_accept(self):
        name = self.name_edit.text().strip()
        height = self.height_edit.value()
        min_pace = self.min_pace_edit.value()
        max_pace = self.max_pace_edit.value()

        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a name.")
            return
        if height <= 0:
            QMessageBox.warning(self, "Missing Height", "Please enter the swimmer's height.")
            return
        if min_pace <= 0 or max_pace <= 0:
            QMessageBox.warning(self, "Missing Pace", "Please enter both the fastest and slowest pace.")
            return
        if min_pace >= max_pace:
            QMessageBox.warning(
                self, "Invalid Pace Range",
                "The fastest (min) pace must be less than the slowest (max) pace."
            )
            return

        self._result = (name, height, min_pace, max_pace)
        self.accept()

    def get_values(self):
        return self._result

class SwimDateRangeDialog(QDialog):
    """
    Two side-by-side calendars ("From" / "To") for picking which day(s) of
    CSV/video to load in SwimPlot. Both default to today (the common
    single-day case). An OK button (default — Enter triggers it) confirms;
    Close exits SwimPlot entirely back to the main program. Shown again
    (loop, in QtMainWindow.openSwimPlot) whenever SwimPlotWindow itself
    is closed, so a new date can be picked without reopening SwimPlot
    from the menu.
    """
    def __init__(self, app, parent=None, initial_from=None, initial_to=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("Select Swim Date(s)")
        self.setModal(True)

        # Keep the native title bar (unlike PlacePointsWindow/SwimPlotWindow,
        # which go fully frameless -- Bill wants this one to keep showing
        # "Select Swim Date(s)"), but pin it flush to the top-left and
        # size its content so title bar + content together fit exactly on
        # screen -- previously, with no explicit position/size at all,
        # the WM auto-centered it and the content alone already used the
        # full screen height, so adding the title bar on top pushed the
        # OK/Close buttons off the bottom.
        # Measured via screenshot 2026-08-30: 36px WM gap above the title
        # bar (the WM was overriding the move(0, 0) below at initial
        # placement) + 28px for the title bar itself = 64px total
        # overhead to reserve.
        TITLE_BAR_OVERHEAD = 64
        self.setFixedSize(self.app.window_w, self.app.window_h - TITLE_BAR_OVERHEAD)
        self.move(0, 0)
        # The WM re-centers/repositions modal decorated dialogs when they
        # actually get mapped to the screen, overriding the move() above
        # (that's the 36px gap) -- reassert the position once more after
        # the dialog is shown, which wins against that.
        QTimer.singleShot(0, lambda: self.move(0, 0))

        today = QDate.currentDate()
        from_qdate = QDate(initial_from.year, initial_from.month, initial_from.day) \
            if initial_from is not None else today
        to_qdate = QDate(initial_to.year, initial_to.month, initial_to.day) \
            if initial_to is not None else today

        # Stacked top/bottom instead of side by side so each calendar can
        # use nearly the full portrait-mode screen width (self.app.window_w
        # — same value the pool display and SwimPlotWindow itself are
        # sized to) rather than splitting it — bigger cells, room for the
        # avg-pace line below each day number. QCalendarWidget's own
        # default size hint is fairly small and leaves most of that space
        # unused, so give it an explicit minimum size too rather than just
        # capping the max -- reserve room for the two "From"/"To" labels
        # and the OK/Close button row, split the rest evenly between the
        # two calendars.
        outer_margin = 20      # dialog layout margins (both sides)
        cal_width = self.app.window_w - outer_margin
        reserved_v = 160       # labels + button row + layout spacing
        cal_height = max(200, (self.app.window_h - reserved_v) // 2)

        layout = QVBoxLayout()
        # Qt's default ~10-11px contents margin on all four sides was
        # invisible before (the OK/Close buttons were clipped off-screen
        # entirely), but now that the dialog is exactly window-sized,
        # it shows up as unused space below the buttons. Shrink it
        # rather than remove it outright, so there's still some
        # breathing room on every edge.
        layout.setContentsMargins(4, 4, 4, 4)

        # Mark dates that actually have swim data instead of the default
        # (fairly useless) Saturday/Sunday red styling.
        data_dates = self._find_data_dates()
        self._data_dates = set(data_dates)

        # Avg-pace cache + loaded-months set are shared (same dict/set
        # object) between both calendars, so browsing to a given month in
        # either one makes it instantly available in the other too.
        self._avg_pace_cache = {}
        self._avg_pace_months_loaded = set()

        from_col = QVBoxLayout()
        from_col.addWidget(QLabel("From                        Average Pace (blue)"))
        self.from_cal = _MonthOnlyCalendar()
        self.from_cal.setSelectedDate(from_qdate)
        self.from_cal.setMinimumWidth(cal_width)
        self.from_cal.setMaximumWidth(cal_width)
        self.from_cal.setMinimumHeight(cal_height)
        self.from_cal.setDataDates(data_dates)
        self._keep_highlight_visible(self.from_cal)
        self._style_calendar_dates(self.from_cal, data_dates)
        self.from_cal.setAvgPaceSource(self.app.data_dir, self._avg_pace_cache, self._avg_pace_months_loaded)
        from_col.addWidget(self.from_cal)
        layout.addLayout(from_col)

        to_col = QVBoxLayout()
        to_col.addWidget(QLabel("To"))
        self.to_cal = _MonthOnlyCalendar()
        self.to_cal.setSelectedDate(to_qdate)
        self.to_cal.setMinimumWidth(cal_width)
        self.to_cal.setMaximumWidth(cal_width)
        self.to_cal.setMinimumHeight(cal_height)
        self.to_cal.setDataDates(data_dates)
        self._keep_highlight_visible(self.to_cal)
        self._style_calendar_dates(self.to_cal, data_dates)
        self.to_cal.setAvgPaceSource(self.app.data_dir, self._avg_pace_cache, self._avg_pace_months_loaded)
        to_col.addWidget(self.to_cal)
        layout.addLayout(to_col)

        # "From" and "To" are fully independent -- picking a date in one
        # no longer moves the other. "To" just stays wherever it already
        # is (today by default, or the previously-remembered end date
        # when reopening) until explicitly clicked.

        # Absorb any leftover vertical space here (between the calendars
        # and the buttons) rather than letting it strand below the
        # buttons at the very bottom of the fixed-size window -- the
        # calendars' setMinimumHeight() is a floor, not exact, so the
        # actual leftover amount depends on font metrics/DPI and isn't
        # worth hardcoding.
        layout.addStretch(1)

        # Shown when OK is pressed on a range without any swims (Bill,
        # 2026-10-16: the plot screen then said "No data ... Press Esc",
        # and without a keyboard there was no way out).
        self.no_data_lbl = QLabel("")
        self.no_data_lbl.setAlignment(Qt.AlignCenter)
        self.no_data_lbl.setStyleSheet("color: #b00; font-weight: bold;")
        layout.addWidget(self.no_data_lbl)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setDefault(True)      # Enter key triggers this
        self.ok_btn.setAutoDefault(True)
        self.close_btn = QPushButton("Close")   # consistent with SwimPlotWindow's Close
        # The pool's On/Off, also off the main screen (Bill, 2026-10-16)
        self.pump_btn = QPushButton("Pump On/Off")
        self.pump_btn.setAutoDefault(False)
        self.pump_btn.setStyleSheet(self.app.PUMP_BTN_STYLE)
        self.ok_btn.clicked.connect(self._ok_if_data)
        self.close_btn.clicked.connect(self.reject)
        self.pump_btn.clicked.connect(lambda: self.app.OnOff_confirm(self))
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.close_btn)
        btn_layout.addWidget(self.pump_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Position the OS cursor over today's cell in the From calendar so
        # the common "just view today" case is a fast click. This pokes at
        # QCalendarWidget's internal QTableView (undocumented but stable
        # across Qt5) — if it ever fails, we just skip the cursor move.
        QTimer.singleShot(0, lambda: self._position_cursor_on_today(self.from_cal))

    def _ok_if_data(self):
        """OK: open the plot only if a day in the range has swim data
        (green dates); otherwise say so and stay on the calendar."""
        from_date, to_date = self.get_range()
        if any(from_date <= d <= to_date for d in self._data_dates):
            self.no_data_lbl.setText("")
            self.accept()
        else:
            self.no_data_lbl.setText("No swims on the chosen date(s). Pick a green date.")

    def _position_cursor_on_today(self, calendar):
        try:
            view = calendar.findChild(QTableView)
            if view is None:
                return
            index = view.currentIndex()
            if not index.isValid():
                return
            rect = view.visualRect(index)
            center = rect.center()
            global_pt = view.viewport().mapToGlobal(center)
            QCursor.setPos(global_pt)
        except Exception:
            pass   # cosmetic only — never block the dialog over this

    def _keep_highlight_visible(self, calendar):
        # Qt dims the selected-date highlight to a muted "inactive" color
        # once keyboard focus moves to the other calendar, which reads as
        # the selection having been lost. Force the inactive Highlight
        # colors to match the active ones so both dates stay clearly
        # marked no matter which calendar currently has focus.
        pal = calendar.palette()
        pal.setColor(QPalette.Inactive, QPalette.Highlight,
                     pal.color(QPalette.Active, QPalette.Highlight))
        pal.setColor(QPalette.Inactive, QPalette.HighlightedText,
                     pal.color(QPalette.Active, QPalette.HighlightedText))
        calendar.setPalette(pal)

    def _find_data_dates(self):
        """Dates (python `date`) with a YYYY-MM-DD.csv file in data_dir."""
        data_dates = []
        try:
            for name in os.listdir(self.app.data_dir):
                if not name.endswith(".csv"):
                    continue
                try:
                    data_dates.append(date.fromisoformat(name[:-len(".csv")]))
                except ValueError:
                    continue   # not a YYYY-MM-DD.csv file — ignore
        except OSError:
            pass   # cosmetic only — never block the dialog over this
        return data_dates

    def _style_calendar_dates(self, calendar, data_dates):
        # Week-number gutter column is Qt's default and not useful here
        # either, and it eats into the already-tight side-by-side width.
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # US-style weeks: Sunday first (Qt's default follows the system
        # locale, which gave Monday-first here).
        calendar.setFirstDayOfWeek(Qt.Sunday)

        # Weekend red is default Qt styling and not useful here — clear it.
        plain = QTextCharFormat()
        calendar.setWeekdayTextFormat(Qt.Saturday, plain)
        calendar.setWeekdayTextFormat(Qt.Sunday, plain)

        # Bold green marks any date that actually has swim data.
        has_data_fmt = QTextCharFormat()
        has_data_fmt.setFontWeight(QFont.Bold)
        has_data_fmt.setForeground(QColor("green"))
        for d in data_dates:
            calendar.setDateTextFormat(QDate(d.year, d.month, d.day), has_data_fmt)

    def _on_from_clicked(self, qdate):
        if not self._to_touched:
            self.to_cal.setSelectedDate(qdate)

    def _on_to_clicked(self, qdate):
        self._to_touched = True

    def get_range(self):
        from_qdate = self.from_cal.selectedDate()
        to_qdate = self.to_cal.selectedDate()
        if to_qdate < from_qdate:
            from_qdate, to_qdate = to_qdate, from_qdate
        from_date = date(from_qdate.year(), from_qdate.month(), from_qdate.day())
        to_date = date(to_qdate.year(), to_qdate.month(), to_qdate.day())
        return from_date, to_date

class SwimPlotWindow(QDialog):
    def __init__(self, app, parent=None, from_date=None, to_date=None):
        super().__init__(parent)

        self.app = app
        # Date range to load — defaults to today only if not given.
        self.from_date = from_date if from_date is not None else date.today()
        self.to_date = to_date if to_date is not None else date.today()
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(self.app.window_w, self.app.window_h)
        self.move(0, 0)

        # --- tuning variables ---
        self.plotDataInterval_sec = 2.0   # downsample interval (must be even)
        self.reducedGap_sec = 4.0         # compressed gap size (must be even)
        self.gap_threshold_sec = 10.0     # real gap threshold
        self.samples_per_sec = 2.0        # CSV sampling rate ~2 Hz

        # Compress Gaps state — lives here (not on a button widget) because
        # it has to be readable by _prepare_display_arrays() before the
        # video overlay (and its Compress button) exists yet, on first open.
        self.compress_gaps_checked = False

        # --- Main layout --- just a loading message; there's no "first
        # screen" of big plots anymore — opening SwimPlotWindow goes
        # straight to the video screen (see on_open/_build_video_overlay).
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Shown until the first build_arrays() completes — CSV read + the
        # gap-fill pass can take a noticeable few seconds on the Pi for a
        # large date range (e.g. a full month), during which the dialog
        # would otherwise just sit there with nothing else visible.
        self.loading_label = QLabel("Please wait, loading data...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 16px; color: #333;")
        self.layout.addWidget(self.loading_label)

        self.setLayout(self.layout)

        # Auto-load data and jump straight to the video screen once the
        # window loads.
        QTimer.singleShot(0, self.on_open)

    def build_arrays(self):
        # Load CSV(s) for the selected date range (epoch timestamps),
        # tagged per-row with source date (as toordinal()) for video lookup.
        # Updating loading_label + processing events after EACH day's file
        # (rather than once before the whole call) is what actually makes
        # the "please wait" text/progress visible — a single processEvents()
        # before one long blocking call wasn't reliably flushing the paint.
        # Per-file CSV parsing is fast enough that firing an update on
        # EVERY file can outrun the display pipeline (RealVNC in Bill's
        # case) — only the very first paint would ever actually be seen.
        # Throttle to roughly 6 updates/sec of wall-clock time so each one
        # gets a real chance to reach the screen; always show the last file
        # regardless, for a clean "done loading" moment.
        progress_state = {"last_update": 0.0}

        def _progress(day_num, total_days, d):
            if getattr(self, "loading_label", None) is None:
                return
            now = time.time()
            is_last = (day_num == total_days)
            if not is_last and (now - progress_state["last_update"] < 0.15):
                return
            progress_state["last_update"] = now
            self.loading_label.setText(
                f"Please wait, loading data...\n({day_num}/{total_days}: {d.strftime('%m-%d-%Y')})"
            )
            QApplication.processEvents()

        (time_raw, pace_raw, dist_raw, segment_raw, frame_raw, date_raw,
         comh_raw, comw_raw, zone_raw, zones_raw) = \
            self.app.load_csv_range(self.from_date, self.to_date, progress_cb=_progress)

        if time_raw is None or len(time_raw) == 0:
            return None

        # Convert epoch timestamps → relative seconds
        t0 = time_raw[0]
        real_times = [t - t0 for t in time_raw]

        # Derive recording interval from the data itself so playback and gap
        # detection adapt automatically when loading CSV files recorded at a
        # different rate than the current defaults setting.
        if len(real_times) > 1:
            deltas = np.diff(real_times)
            dt = float(np.median(deltas))
            if dt <= 0:
                dt = self.app.data_interval_sec
        else:
            dt = self.app.data_interval_sec
        self.derived_dt = dt

        short_rows = []
        full_rows  = []

        # ------------------------------------------------------------
        # INITIALIZE TIMELINES
        # ------------------------------------------------------------
        last_real_t = real_times[0]      # real time from CSV
        last_t      = last_real_t        # full-gap timeline (real)
        last_syn_t  = last_real_t        # short-gap synthetic timeline

        last_p      = pace_raw[0]
        last_d      = dist_raw[0]
        last_seg    = segment_raw[0]
        last_frame  = frame_raw[0]
        last_date   = date_raw[0]

        # First row goes into both arrays
        last_ch, last_cw = comh_raw[0], comw_raw[0]
        last_zn, last_zs = zone_raw[0], zones_raw[0]
        short_rows.append([last_syn_t, last_p, last_d, last_seg, last_frame, last_date, last_ch, last_cw, last_zn, last_zs])
        full_rows.append([last_t,      last_p, last_d, last_seg, last_frame, last_date, last_ch, last_cw, last_zn, last_zs])

        # Track last normal delta for synthetic time
        last_delta_real = dt

        # ------------------------------------------------------------
        # GAP DETECTOR
        # ------------------------------------------------------------
        # A real pause (out of the lane, Suspend) lasts seconds. Rows are
        # written from the program loop, so they come a little early or
        # late, and a range can mix recording rates (5 and 15 per second):
        # a gap needs BOTH 1.5 x the typical interval and MIN_GAP_SEC.
        # (Up to v15.1 only the 1.5 x rule: a mixed-rate day drew a spike
        # to 7:00 at every slower row.)
        MIN_GAP_SEC = 1.0

        def gap_detector(last_real_t, new_real_t, dt):
            delta = new_real_t - last_real_t
            return delta >= max(dt * 1.5, MIN_GAP_SEC)

        # A CLUSTER of pauses with only moments of swimming between them
        # (getting out, putting the cover back: the camera loses and finds
        # the swimmer again and again) is ONE pause when compressed: a
        # pause starting less than CLUSTER_SEC after the previous one ended
        # gets no compressed filler of its own. Bill, 2026-10-17: on 10/16
        # "there is a gap that will not compress" -- ten pauses in 51 s at
        # 18:55 got ten fillers, ~25 s wide on the plot. Day boundaries
        # always keep theirs.
        CLUSTER_SEC = 2.0
        prev_gap_end_t = None

        # ------------------------------------------------------------
        # MAIN LOOP
        # ------------------------------------------------------------
        for i in range(1, len(real_times)):

            new_real_t = real_times[i]
            new_p      = pace_raw[i]
            new_d      = dist_raw[i]
            new_seg    = segment_raw[i]
            new_frame  = frame_raw[i]
            new_date   = date_raw[i]

            delta_real = new_real_t - last_real_t

            if gap_detector(last_real_t, new_real_t, dt):

                # ----------------------------------------------------
                # GAP FOUND
                # ----------------------------------------------------
                real_gap = new_real_t - last_real_t
                max_fill = int(real_gap // dt)
                short_fill = min(int(4.0 // dt), max_fill)
                if (prev_gap_end_t is not None and new_date == last_date
                        and last_real_t - prev_gap_end_t < CLUSTER_SEC):
                    short_fill = 0          # same cluster: one filler already shown
                prev_gap_end_t = new_real_t

                # ====================================================
                # FULL-GAP FILL (REAL TIME)
                # ====================================================
                # A long gap (e.g. the ~20 hours between one day's swim
                # session and the next) doesn't need a filler row every
                # dt seconds — that exploded full_gap_array to millions
                # of rows for a month-long range (measured: 11.3M rows,
                # ~28s of a ~37s on_plot). Cap the row count per gap; the
                # true elapsed time is still spanned exactly (just with
                # coarser spacing), so the "showing gaps" plateau still
                # reads correctly on the plot.
                #
                # Day-boundary gaps get a wider fixed placeholder (~0.5
                # "virtual" hour at the recording rate) than an ordinary
                # in-session pause, so day divisions are visually
                # distinguishable on the plot instead of looking like
                # just another short pause.
                MAX_GAP_FILL_ROWS = 200
                DAY_BOUNDARY_FILL_ROWS = int(1800 / dt)  # ~0.5 hr placeholder width
                crosses_day = (new_date != last_date)
                cap = DAY_BOUNDARY_FILL_ROWS if crosses_day else MAX_GAP_FILL_ROWS
                full_fill_count = min(max_fill, cap)
                full_fill_step  = (real_gap / full_fill_count) if full_fill_count > 0 else dt

                t_full = last_t
                for _ in range(full_fill_count):
                    t_full += full_fill_step
                    full_rows.append([t_full, 7.0, last_d, last_seg, last_frame, last_date] + [float("nan")] * 4)

                # ====================================================
                # SHORT-GAP FILL (SYNTHETIC TIME — FROZEN)
                # ====================================================
                for _ in range(short_fill):
                    short_rows.append([last_syn_t, 7.0, last_d, last_seg, last_frame, last_date] + [float("nan")] * 4)

                # ====================================================
                # ADVANCE TIMELINES AFTER GAP
                # ====================================================

                # FULL-GAP timeline jumps to real time
                last_t = new_real_t

                # SHORT-GAP timeline advances ONLY by last normal delta
                last_syn_t = last_syn_t + last_delta_real

                # Update real time tracker
                last_real_t = new_real_t

            else:
                # ----------------------------------------------------
                # NO GAP — NORMAL ROW
                # ----------------------------------------------------

                # FULL-GAP timeline uses real time
                last_t = new_real_t

                # SHORT-GAP timeline advances by real delta
                last_syn_t = last_syn_t + delta_real

                # Update last normal delta
                last_delta_real = delta_real

                # Update real time tracker
                last_real_t = new_real_t

            # --------------------------------------------------------
            # APPEND REAL ROW TO BOTH ARRAYS
            # --------------------------------------------------------
            last_p     = new_p
            last_d     = new_d
            last_seg   = new_seg
            last_frame = new_frame
            last_date  = new_date

            full_rows.append([last_t,     last_p, last_d, last_seg, last_frame, last_date,
                              comh_raw[i], comw_raw[i], zone_raw[i], zones_raw[i]])
            short_rows.append([last_syn_t, last_p, last_d, last_seg, last_frame, last_date,
                               comh_raw[i], comw_raw[i], zone_raw[i], zones_raw[i]])

        # ------------------------------------------------------------
        # Insert Idx as column 0
        # ------------------------------------------------------------
        short_rows = [[i] + row for i, row in enumerate(short_rows)]
        full_rows  = [[i] + row for i, row in enumerate(full_rows)]

        # Convert to numpy arrays
        self.short_gap_array = np.array(short_rows, dtype=float)
        self.full_gap_array  = np.array(full_rows,  dtype=float)

        return True

    def pace_to_mph(self, pace):
        if pace >= 7.0:   # gap sentinel
            return 0.0

        miles_per_100yd = 0.05681818
        mph = miles_per_100yd * (60.0 / pace)
        return mph

    def _prepare_display_arrays(self):
        """
        Select the active gap array (Compress Gaps state), build the
        canonical per-row display arrays, and smooth X_pace for display.
        Shared by the initial video-screen build and by toggling Compress
        Gaps — neither needs a separate big Pace/MPH plot screen to run
        first; that screen was removed (see poolwindAI_v7.36 header).
        """
        if self.compress_gaps_checked:
            array_in = self.short_gap_array
        else:
            array_in = self.full_gap_array

        # Canonical arrays
        self.X_idx   = array_in[:, 0]
        self.X_time  = array_in[:, 1]
        self.X_pace  = array_in[:, 2]
        self.X_dist  = array_in[:, 3]
        self.X_seg   = array_in[:, 4]
        self.X_frame = array_in[:, 5]
        self.X_date  = array_in[:, 6]   # date.toordinal(), for per-day AVI lookup
        self.X_comh  = array_in[:, 7]   # CoM_h when logged (NaN: older CSV / gap)
        self.X_comw  = array_in[:, 8]   # swimmer tick CoM_w (-1: none, NaN: unknown)
        self.X_zone  = array_in[:, 9]   # jet zone (-1: none, NaN: before v15.2 / gap)
        self.X_zones = array_in[:, 10]  # number of zones then

        # ------------------------------------------------------------
        # SMOOTH X_pace FOR DISPLAY (does not affect runtime data)
        # ------------------------------------------------------------
        try:
            from scipy.signal import savgol_filter
            pace_work  = self.X_pace.copy().astype(float)
            gap_mask   = pace_work == 7.0
            real_mask  = ~gap_mask

            if real_mask.sum() > 11:
                # Interpolate across gap markers so they don't bleed into neighbors
                idx_all  = np.arange(len(pace_work))
                pace_work = np.interp(idx_all, idx_all[real_mask], pace_work[real_mask])

                # Smoothing window: the same ~6 seconds at any recording
                # rate (was 31 rows: 6 s at 5 rows/s but 2 s at 15).
                # Odd number of rows, at least 5.
                dt = getattr(self, "derived_dt", 0.2) or 0.2
                win = max(5, int(round(6.0 / dt)) | 1)
                if win >= real_mask.sum():
                    win = max(5, (int(real_mask.sum()) - 1) | 1)
                pace_work = savgol_filter(pace_work, window_length=win, polyorder=2)

            # Restore gap spikes exactly
            pace_work[gap_mask] = 7.0
            self.X_pace = pace_work
        except Exception:
            pass   # if scipy missing or data too short, use raw pace

        # ------------------------------------------------------------
        # SUMMARY STATS FOR MINI-PLOT LABELS
        # ------------------------------------------------------------
        real_pace  = self.X_pace[self.X_pace < 7.0]
        self.avg_pace   = float(np.mean(real_pace)) if len(real_pace) > 0 else 0.0
        self.total_dist = float(self.X_dist[-1])    if len(self.X_dist) > 0 else 0.0

    def on_open(self):
        # Entry point: load data, then jump straight to the video screen —
        # there's no separate big-plot screen to visit first anymore.
        QApplication.processEvents()

        if not self.build_arrays():
            # No data for the selected date(s) — nothing to show.
            if getattr(self, "loading_label", None) is not None:
                self.loading_label.setText("No data for the selected date(s).")
            back_btn = QPushButton("Back to the calendar")
            back_btn.clicked.connect(self.reject)
            self.layout.addWidget(back_btn, alignment=Qt.AlignCenter)
            return

        self._prepare_display_arrays()

        if getattr(self, "loading_label", None) is not None:
            self.layout.removeWidget(self.loading_label)
            self.loading_label.deleteLater()
            self.loading_label = None

        # Default to the most recent data point in the range so opening a
        # multi-day range lands on the latest swim, not the oldest.
        self._build_video_overlay(start_idx=len(self.X_idx) - 1)

    def _repair_avi_if_needed(self, avi_path, seg, date_ord):
        # A power failure (or any hard interruption) leaves that segment's
        # AVI writer un-released, which leaves the MJPG/AVI container
        # without a finalized frame index -- cv2 then reports frame_count
        # 0 for it and CAP_PROP_POS_FRAMES seeking silently does nothing
        # (always lands on frame 1), which is what caused the multi-
        # segment scrub desync on 2026-08-03. The frame data itself is
        # still intact, so an `ffmpeg -c copy` remux rebuilds a valid
        # index without re-encoding. Checked on every segment open, but
        # self-limiting: a repaired file reports a real frame count next
        # time and is skipped.
        if not os.path.isfile(avi_path):
            return

        # Never touch the segment currently being recorded -- its frame
        # count legitimately reads 0 until it's actually closed.
        myvc = self.app.myVideoCapture
        is_live_segment = (
            date_ord == date.today().toordinal() and
            seg == getattr(myvc, "segment_id", None) and
            getattr(myvc, "persp_writer", None) is not None and
            myvc.persp_writer.isOpened()
        )
        if is_live_segment:
            return

        cap = cv2.VideoCapture(avi_path)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        if frame_count > 0:
            return

        fixed_path = avi_path + ".fixed.avi"
        try:
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", avi_path, "-c", "copy", fixed_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120
            )
        except Exception:
            return

        if result.returncode != 0 or not os.path.isfile(fixed_path):
            if os.path.isfile(fixed_path):
                os.remove(fixed_path)
            return

        check_cap = cv2.VideoCapture(fixed_path)
        fixed_count = check_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        check_cap.release()
        if fixed_count <= 0:
            os.remove(fixed_path)
            return

        bak_path = avi_path + ".bak"
        if not os.path.isfile(bak_path):
            os.rename(avi_path, bak_path)
        else:
            os.remove(avi_path)
        os.rename(fixed_path, avi_path)

    def _build_video_overlay(self, start_idx):
        start_idx = int(np.clip(start_idx, 0, len(self.X_idx) - 1))

        # --------------------------------------------------------
        # LOAD FRAME FROM AVI AT THE STARTING ROW
        # --------------------------------------------------------
        seg  = int(self.X_seg[start_idx])
        fnum = int(self.X_frame[start_idx])
        date_ord = int(self.X_date[start_idx])
        base = os.path.join(self.app.data_dir, date.fromordinal(date_ord).isoformat())
        avi_path = f"{base}_{seg:02d}.avi"

        self._repair_avi_if_needed(avi_path, seg, date_ord)
        cap = cv2.VideoCapture(avi_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, fnum - 1))
        ok, frame = cap.read()
        cap.release()

        if not ok or frame is None:
            frame = np.zeros(
                (self.app.work_size_h, self.app.work_size_w, 3),
                dtype=np.uint8
            )

        # Treat AVI frame like perspect_img (full-sized)
        frame = cv2.resize(frame, (self.app.window_w, self.app.window_h))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        # Display in QtMainWindow
        self.app.window.display_canvas.setFrame(pixmap)

        # ------------------------------------------------------------
        # CREATE SEMI-TRANSPARENT OVERLAY BOX (MINI-PLOT HOLDER)
        # ------------------------------------------------------------

        # Parent the overlay to the main window so it sits above display_canvas
        # and is completely outside display_canvas's event filter chain.
        overlay_parent = self.app.window

        overlay = DraggableOverlay(overlay_parent)

        overlay.setEnabled(True)
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        overlay.setMouseTracking(True)

        # Geometry
        screen_w = self.app.window_w
        screen_h = self.app.window_h

        overlay_x = 25
        overlay_w = screen_w - 50
        overlay_h = int(screen_h * 0.33)
        text_strip = int(35 * screen_h / self.app.work_size_h)
        overlay_y  = screen_h - overlay_h - text_strip

        overlay.setGeometry(overlay_x, overlay_y, overlay_w, overlay_h)
        overlay.show()
        QTimer.singleShot(0, overlay.raise_)

        # ------------------------------------------------------------
        # MINI PLOTS inside overlay
        # ------------------------------------------------------------
        PLOT_ALPHA = 0.55   # 0.0 = fully transparent, 1.0 = fully opaque

        dpi    = 80
        fig_w  = overlay_w / dpi
        fig_h  = (overlay_h - DraggableOverlay.HANDLE_H) / dpi / 2

        fig_pace, ax_pace = plt.subplots(figsize=(fig_w, fig_h))
        fig_mph,  ax_mph  = plt.subplots(figsize=(fig_w, fig_h))

        for fig, ax in ((fig_pace, ax_pace), (fig_mph, ax_mph)):
            fig.patch.set_facecolor((1, 1, 1, PLOT_ALPHA))
            ax.patch.set_facecolor((1, 1, 1, PLOT_ALPHA))

        fig_pace.subplots_adjust(left=0.13, right=0.98, top=0.90, bottom=0.28)
        fig_mph.subplots_adjust( left=0.13, right=0.98, top=0.90, bottom=0.28)

        ax_pace.plot(self.X_idx, self.X_pace, color="blue",  linewidth=0.6)
        # Faster (lower pace number) plots HIGHER, like the MPH plot -- the
        # y-axis labels still read in min/100 yd, increasing downward.
        ax_pace.invert_yaxis()
        # Top of the axis = the whole number just above the fastest real
        # pace shown (1 for paces of 1:00-1:59, 0 below 1:00) instead of
        # matplotlib's margin, so no space is wasted on paces nobody swims.
        # The bottom keeps its usual small margin below the slowest point.
        real_paces = self.X_pace[(self.X_pace > 0) & (self.X_pace < 7.0)]
        if len(real_paces):
            pace_top = math.ceil(float(real_paces.min())) - 1
            pace_bottom = ax_pace.get_ylim()[0]          # inverted: [0] is the bottom
            ax_pace.set_ylim(pace_bottom, max(0, pace_top))
        ax_pace.set_ylabel("Pace (min/100 yd)", fontsize=7)
        ax_pace.set_xlabel(
            f"Time  overall: Avg Pace = {Utils.DecimalToTime(getattr(self, 'avg_pace', 0.0))}",
            fontsize=7, loc='left')
        ax_pace.tick_params(labelsize=6)

        mph_vals = np.where(self.X_pace >= 7.0, 0,
                            (0.05681818 / self.X_pace) * 100)
        ax_mph.plot(self.X_idx, mph_vals, color="green", linewidth=0.6)
        ax_mph.set_ylabel("Speed (MPH)", fontsize=7)
        ax_mph.set_xlabel(
            f"Distance (miles)  overall: {getattr(self, 'total_dist', 0.0):.3f}",
            fontsize=7, loc='left')

        ax_mph.tick_params(labelsize=6)

        from matplotlib.ticker import MaxNLocator

        def mini_time_fmt(x, pos):
            idx = int(np.clip(round(x), 0, len(self.X_time) - 1))
            t = self.X_time[idx]
            return f"{int(t//3600)}:{int((t%3600)//60):02d}:{int(t%60):02d}"

        def mini_dist_fmt(x, pos):
            idx = int(np.clip(round(x), 0, len(self.X_dist) - 1))
            return f"{self.X_dist[idx]:.2f}"

        ax_pace.xaxis.set_major_formatter(mini_time_fmt)
        ax_mph.xaxis.set_major_formatter(mini_dist_fmt)
        ax_pace.xaxis.set_major_locator(MaxNLocator(nbins=8))
        ax_mph.xaxis.set_major_locator(MaxNLocator(nbins=8))
        ax_pace.tick_params(axis='x', labelsize=5, rotation=30)
        ax_mph.tick_params(axis='x', labelsize=5, rotation=30)

        mini_canvas_pace = FigureCanvas(fig_pace)
        mini_canvas_mph  = FigureCanvas(fig_mph)

        for mc in (mini_canvas_pace, mini_canvas_mph):
            mc.setStyleSheet("background: transparent;")
            mc.setAttribute(Qt.WA_TranslucentBackground, True)

        overlay.content_layout.addWidget(mini_canvas_pace)
        overlay.content_layout.addWidget(mini_canvas_mph)
        # Pace shown first; a rebuild (Compress/Expand Gaps) keeps whichever
        # view was showing -- _mini_show_pace survives on self, and each
        # newly opened plot window starts fresh on Pace.
        self._mini_show_pace = getattr(self, "_mini_show_pace", True)
        if self._mini_show_pace:
            mini_canvas_mph.hide()
        else:
            mini_canvas_pace.hide()

        # Crosshair lines
        hline_p = ax_pace.axhline(color='red', linewidth=0.8, linestyle='--')
        vline_p = ax_pace.axvline(color='red', linewidth=0.8, linestyle='--')
        hline_m = ax_mph.axhline( color='red', linewidth=0.8, linestyle='--')
        vline_m = ax_mph.axvline( color='red', linewidth=0.8, linestyle='--')

        # Draw initial crosshair at the starting row
        for hl, vl, ax in [(hline_p, vline_p, ax_pace),
                            (hline_m, vline_m, ax_mph)]:
            hl.set_ydata([ax.lines[0].get_ydata()[start_idx]] * 2)
            vl.set_xdata([self.X_idx[start_idx]] * 2)
            hl.set_visible(True)
            vl.set_visible(True)

        # Day header — sits in the blank margin matplotlib already
        # leaves above the axes (subplots_adjust top=0.90), centered
        # over the plot. Shows the date of whichever frame is
        # currently active/playing; updated in _update_crosshair as
        # the crosshair moves across a multi-day range.
        def _day_title(ni):
            return date.fromordinal(int(self.X_date[ni])).strftime("%m-%d-%Y")

        ax_pace.set_title(_day_title(start_idx), fontsize=8)
        ax_mph.set_title(_day_title(start_idx), fontsize=8)

        # Floating coordinate box.
        self.coord_label_mini = QLabel(overlay)
        self.coord_label_mini.setStyleSheet(
            "background-color: rgba(200,200,200,160);"
            "border: 1px solid black;"
            "padding: 1px;"
        )
        self.coord_label_mini.show()
        self.coord_label_mini.raise_()

        def position_mini_label():
            margin = 8
            self.coord_label_mini.adjustSize()
            self.coord_label_mini.move(
                overlay.width() - self.coord_label_mini.width() - margin,
                overlay.height() - self.coord_label_mini.height() - 2
            )

        def update_mini_label(ni):
            t = self.X_time[ni]
            h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
            if self._mini_show_pace:
                self.coord_label_mini.setText(
                    f"({h}:{m:02d}:{s:02d}, {Utils.DecimalToTime(self.X_pace[ni])})")
            else:
                mph_v = 0 if self.X_pace[ni] >= 7.0 else \
                        (0.05681818 / self.X_pace[ni]) * 100
                self.coord_label_mini.setText(f"({self.X_dist[ni]:.3f}, {mph_v:.2f})")
            position_mini_label()

        # Toggle between pace / MPH (button names the OTHER view)
        overlay.toggle_btn.setText("MPH" if self._mini_show_pace else "Pace")
        update_mini_label(start_idx)

        def on_toggle():
            self._mini_show_pace = not self._mini_show_pace
            if self._mini_show_pace:
                mini_canvas_mph.hide()
                mini_canvas_pace.show()
                overlay.toggle_btn.setText("MPH")
            else:
                mini_canvas_pace.hide()
                mini_canvas_mph.show()
                overlay.toggle_btn.setText("Pace")
            update_mini_label(_ps['idx'])
        overlay.toggle_btn.clicked.connect(on_toggle)
        overlay.plot_btn.clicked.connect(self.on_close)
        overlay.pump_btn.clicked.connect(lambda: self.app.OnOff_confirm(self))

        # Compress Gaps toggle — rebuilds the whole overlay against the
        # other array (short_gap_array vs full_gap_array), preserving the
        # current row position as best it can (row counts differ between
        # the two arrays, same approximation the old Plot-screen toggle
        # relied on).
        overlay.compress_btn.setChecked(self.compress_gaps_checked)
        overlay.compress_btn.setText("Expand Gaps" if self.compress_gaps_checked else "Compress Gaps")

        def on_compress_toggle(checked):
            self.compress_gaps_checked = checked
            preserved_idx = _ps['idx']
            self._prepare_display_arrays()
            self._teardown_video_overlay()
            self._build_video_overlay(start_idx=preserved_idx)
        overlay.compress_btn.toggled.connect(on_compress_toggle)

        # Cached VideoCapture — reopen only when (date, segment) changes.
        # Segment numbers reset every day, so the date must be part of
        # the cache key, not just the segment number.
        self._mini_cap     = None
        self._mini_cap_key = None

        def _load_video_frame(seg, fnum, date_ord, ni=None):
            if seg <= 0 or fnum <= 0:
                return
            base = os.path.join(self.app.data_dir, date.fromordinal(int(date_ord)).isoformat())
            cache_key = (int(date_ord), seg)
            if self._mini_cap_key != cache_key:
                if self._mini_cap is not None:
                    self._mini_cap.release()
                avi_path = f"{base}_{seg:02d}.avi"
                self._repair_avi_if_needed(avi_path, seg, int(date_ord))
                self._mini_cap     = cv2.VideoCapture(avi_path)
                self._mini_cap_key = cache_key
            self._mini_cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, fnum - 1))
            ok, frame = self._mini_cap.read()
            if ok and frame is not None:
                self._replay_frame = cv2.resize(frame, (self.app.window_w, self.app.window_h))
                self._replay_ni = ni
                _show_replay_frame()

        def _show_replay_frame():
            # Plain recorded frame, plus (switched by a tap on the video,
            # the same switch as on the pool screen) the swim zone
            # highlight where this row has a logged zone (since v15.2), and
            # for developers the CoM bar where it has a logged CoM.
            if self._replay_frame is None:
                return
            frame = self._replay_frame.copy()
            ni = self._replay_ni
            on = self.app.zone_highlight_on()
            if on and ni is not None and not np.isnan(self.X_zone[ni]) and self.X_zone[ni] >= 0:
                draw_zone_band_on(frame, int(self.X_zone[ni]), int(self.X_zones[ni]),
                                  float(self.app.REPdefaults.get("zoneHighlightLevel", 0.10)))
            if (on and self.app.REPdefaults["developerMode"]
                    and self.app.REPdefaults.get("comBar", True)
                    and ni is not None and not np.isnan(self.X_comh[ni])):
                cw = self.X_comw[ni]
                draw_com_bar_on(frame, float(self.X_comh[ni]),
                                None if (np.isnan(cw) or cw < 0) else float(cw),
                                self.app.zoneWidth, self.app.CoM_size_h, self.app.CoM_size_w)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h2, w2, ch = rgb.shape
            qimg = QImage(rgb.data, w2, h2, ch * w2, QImage.Format_RGB888)
            self.app.window.display_canvas.setFrame(QPixmap.fromImage(qimg))

        def _toggle_replay_bar():
            # Swim zone highlight (everyone) and, for developers, the CoM
            # bar (it also moves with swim angle and depth, not just the
            # stroke -- confusing for a swimmer)
            self.app.toggle_zone_highlight()
            _show_replay_frame()

        # A left-click on the video switches the swim zone highlight (and the
        # developer CoM bar). The filter also keeps clicks on the replay
        # from reaching the pool screen.
        self._replay_frame = None
        self._replay_ni = None
        self._bar_filter = _LeftClickFilter(
            _toggle_replay_bar,
            exclude=lambda pos: overlay.isVisible() and overlay.geometry().contains(pos))
        self.app.window.installEventFilter(self._bar_filter)

        # Load initial frame
        _load_video_frame(int(self.X_seg[start_idx]),
                          int(self.X_frame[start_idx]),
                          int(self.X_date[start_idx]),
                          start_idx)

        if getattr(self, '_shared_xlim', None) is not None:
            ax_pace.set_xlim(self._shared_xlim)
            ax_mph.set_xlim(self._shared_xlim)

        _mini_drag = {'active': False, 'press_px': 0, 'orig_xlim': None}

        # --------------------------------------------------------
        # PLAY / PAUSE
        # --------------------------------------------------------
        SPEED_STEPS = [0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        _SPEED_START = 2  # index of 1x
        def _speed_str(s):
            return f"1/{round(1/s)}x" if s < 1 else f"{int(s)}x"

        _ps = {'playing': False, 'idx': start_idx, 'speed': 1, 'speed_idx': _SPEED_START,
               'user_moving': False, 'anchor_frac': 0.5, 'step': 1}
        # Playback clock: each row is shown for as long as it really lasted,
        # so a range mixing recording rates (5 and 15 rows/s) plays at true
        # speed throughout. Gap-filler rows keep one typical interval each
        # (as before), so a long break or a night doesn't play in real
        # time. (Up to v15.1 every row got the range's typical interval.)
        _gap = self.X_pace >= 7.0
        _dur = np.diff(self.X_time)
        _dur = np.where(_gap[:-1] | _gap[1:], self.derived_dt, np.clip(_dur, 0.0, 1.0))
        play_T = np.concatenate([[0.0], np.cumsum(_dur)])
        PLAY_TICK_MS = 40
        # Anchor fraction: screen position (0–1) where the crosshair sits during playback
        x0_i, x1_i = ax_pace.get_xlim()
        if x1_i > x0_i:
            _ps['anchor_frac'] = float(np.clip(
                (self.X_idx[start_idx] - x0_i) / (x1_i - x0_i), 0.05, 0.95))

        def _update_crosshair(ni):
            self.active_idx = ni
            nx = self.X_idx[ni]
            hline_p.set_ydata([self.X_pace[ni]] * 2)
            vline_p.set_xdata([nx] * 2)
            hline_p.set_visible(True); vline_p.set_visible(True)
            mph_v = 0 if self.X_pace[ni] >= 7.0 else \
                    (0.05681818 / self.X_pace[ni]) * 100
            hline_m.set_ydata([mph_v] * 2)
            vline_m.set_xdata([nx] * 2)
            hline_m.set_visible(True); vline_m.set_visible(True)
            day_str = _day_title(ni)
            if ax_pace.get_title() != day_str:
                ax_pace.set_title(day_str, fontsize=8)
                ax_mph.set_title(day_str, fontsize=8)
            mini_canvas_pace.draw_idle()
            mini_canvas_mph.draw_idle()
            update_mini_label(ni)
            _load_video_frame(int(self.X_seg[ni]), int(self.X_frame[ni]), int(self.X_date[ni]), ni)

        def _set_interval():
            self._play_timer.setInterval(PLAY_TICK_MS)
            _ps['tick_idx'] = None      # resync the playback clock on the next tick

        def _do_pause():
            _ps['playing'] = False
            overlay.play_btn.setText("▶ Play")
            self._play_timer.stop()

        def _do_play():
            _ps['playing'] = True
            overlay.play_btn.setText("⏸ Pause")
            _set_interval()
            self._play_timer.start()

        def on_play_tick():
            if _ps['user_moving']:
                return
            now = time.monotonic()
            if _ps.get('tick_idx') != _ps['idx']:
                # just started, sped up/down, or the user moved the cursor
                _ps['ptime'] = play_T[_ps['idx']]
            else:
                _ps['ptime'] += (now - _ps['wall']) * _ps['speed']
            _ps['wall'] = now
            _ps['tick_idx'] = _ps['idx']
            if _ps['idx'] >= len(self.X_idx) - 1:
                _do_pause()
                return
            ni = min(len(self.X_idx) - 1,
                     int(np.searchsorted(play_T, _ps['ptime'], side='right')) - 1)
            if ni <= _ps['idx']:
                return                  # not yet time for the next row
            _ps['idx'] = ni
            _ps['tick_idx'] = ni
            _update_crosshair(ni)
            # Scroll plot so crosshair stays at its anchored screen fraction
            # (skip while user is panning — don't fight the drag)
            if not _mini_drag['active']:
                nx = self.X_idx[ni]
                x0, x1 = ax_pace.get_xlim()
                span   = x1 - x0
                new_x0 = nx - _ps['anchor_frac'] * span
                ax_pace.set_xlim(new_x0, new_x0 + span)
                ax_mph.set_xlim(new_x0,  new_x0 + span)

        def on_play_toggle():
            # A Pause pressed by the user sticks (through Compress/Expand
            # Gaps too) until the user presses Play again.
            if _ps['playing']:
                self._user_paused = True
                _do_pause()
            else:
                self._user_paused = False
                _do_play()

        def _auto_resume():
            # Playback stopped by itself at the end of the data: moving the
            # cursor back into the data starts it again -- unless the user
            # paused it.
            if not _ps['playing'] and not self._user_paused \
                    and _ps['idx'] < len(self.X_idx) - 1:
                _do_play()

        def on_wheel_play(direction):
            idx = max(0, min(len(SPEED_STEPS) - 1,
                             _ps['speed_idx'] + (1 if direction > 0 else -1)))
            _ps['speed_idx'] = idx
            _ps['speed'] = SPEED_STEPS[idx]
            overlay.speed_lbl.setText(_speed_str(_ps['speed']))
            if _ps['playing']:
                _set_interval()

        self._play_timer = QTimer()
        self._play_timer.timeout.connect(on_play_tick)

        self._resume_timer = QTimer()
        self._resume_timer.setSingleShot(True)
        self._resume_timer.timeout.connect(
            lambda: _ps.update({'user_moving': False}))

        overlay.play_btn.clicked.connect(on_play_toggle)

        # Plays by default when the plot opens (it stops by itself at the
        # end of the data); a user Pause from before a Compress/Expand
        # Gaps rebuild is kept.
        self._user_paused = getattr(self, "_user_paused", False)
        if not self._user_paused and start_idx < len(self.X_idx) - 1:
            _do_play()

        self._play_filter = _WheelFilter(on_wheel_play)
        overlay.play_btn.installEventFilter(self._play_filter)
        overlay.speed_lbl.installEventFilter(self._play_filter)

        _xhair_drag = {'active': False}

        def on_mini_press(event):
            if event.inaxes is None:
                return
            if event.button == 1:
                _xhair_drag['active'] = True
                on_mini_move(event)
            elif event.button == 3:
                _mini_drag['active']    = True
                _mini_drag['press_px']  = event.x
                _mini_drag['orig_xlim'] = event.inaxes.get_xlim()

        def on_mini_release(event):
            if event.button == 1:
                _xhair_drag['active'] = False
            elif event.button == 3:
                _mini_drag['active'] = False
                # Recompute anchor so playback resumes from the panned position
                x0, x1 = ax_pace.get_xlim()
                if x1 > x0:
                    _ps['anchor_frac'] = float(np.clip(
                        (self.X_idx[_ps['idx']] - x0) / (x1 - x0), 0.05, 0.95))

        def on_mini_move(event):
            if _mini_drag['active']:
                # Right-click drag: pan
                if event.inaxes is None:
                    return
                dx_px = event.x - _mini_drag['press_px']
                x0, x1 = _mini_drag['orig_xlim']
                dpx = (x1 - x0) / event.inaxes.bbox.width
                new_xlim = (x0 - dx_px * dpx, x1 - dx_px * dpx)
                ax_pace.set_xlim(new_xlim)
                ax_mph.set_xlim(new_xlim)
                self._shared_xlim = new_xlim
                mini_canvas_pace.draw_idle()
                mini_canvas_mph.draw_idle()
                return

            if not _xhair_drag['active']:
                return   # hover: do nothing

            if not event.inaxes:
                return

            # Snap crosshair to nearest data point under cursor
            ax    = event.inaxes
            xdata = np.asarray(ax.lines[0].get_xdata(), float)
            idx   = np.searchsorted(xdata, event.xdata)
            idx   = np.clip(idx, 1, len(xdata) - 1)
            ni    = idx if abs(xdata[idx] - event.xdata) < abs(xdata[idx-1] - event.xdata) else idx - 1

            if ni != _ps['idx']:
                _ps['idx'] = ni
                if _ps['playing']:
                    _ps['user_moving'] = True
                    self._resume_timer.start(300)
                else:
                    _auto_resume()
                    if _ps['playing']:
                        _ps['user_moving'] = True       # don't run away mid-drag
                        self._resume_timer.start(300)
                x0, x1 = ax.get_xlim()
                if x1 > x0:
                    _ps['anchor_frac'] = float(np.clip(
                        (xdata[ni] - x0) / (x1 - x0), 0.05, 0.95))
                _update_crosshair(ni)

        def on_mini_scroll(event):
            if event.inaxes is None:
                return
            scale = 1.1 if event.button == "up" else 1 / 1.1
            x0, x1 = event.inaxes.get_xlim()
            xc = event.xdata
            new_xlim = (xc + (x0 - xc) * scale, xc + (x1 - xc) * scale)
            ax_pace.set_xlim(new_xlim)
            ax_mph.set_xlim(new_xlim)
            self._shared_xlim = new_xlim
            mini_canvas_pace.draw_idle()
            mini_canvas_mph.draw_idle()

        for mc in (mini_canvas_pace, mini_canvas_mph):
            mc.mpl_connect("button_press_event",   on_mini_press)
            mc.mpl_connect("motion_notify_event",  on_mini_move)
            mc.mpl_connect("button_release_event", on_mini_release)
            mc.mpl_connect("scroll_event",         on_mini_scroll)

        self.active_idx = start_idx
        self.video_overlay = overlay

    def _teardown_video_overlay(self):
        plt.close('all')
        if hasattr(self, '_play_timer') and self._play_timer is not None:
            self._play_timer.stop()
            self._play_timer = None
        if hasattr(self, '_resume_timer') and self._resume_timer is not None:
            self._resume_timer.stop()
            self._resume_timer = None
        self._play_filter = None
        if getattr(self, '_bar_filter', None) is not None:
            try:
                self.app.window.removeEventFilter(self._bar_filter)
            except Exception:
                pass
            self._bar_filter = None
        if hasattr(self, '_mini_cap') and self._mini_cap is not None:
            self._mini_cap.release()
            self._mini_cap     = None
            self._mini_cap_key = None
        if hasattr(self, 'video_overlay') and self.video_overlay is not None:
            self.video_overlay.close()
            self.video_overlay = None

    def on_close(self):
        self._teardown_video_overlay()
        self.accept()


class _LeftClickFilter(QObject):
    """
    Calls callback() on each left-button click on the replay video and
    swallows it (a quick double-click counts as two clicks).

    Installed on the MAIN WINDOW during swim plot replay: the video canvas
    is transparent to mouse events (DisplayCanvas), so clicks on the video
    arrive at the main window, never at the canvas. Clicks for which
    exclude(pos) is true -- inside the plot box -- are left alone. Swallowing
    the rest also keeps them from reaching the main screen's buttons (Hold,
    UP, ...) hidden under the replay video.
    """
    def __init__(self, callback, exclude=None, parent=None):
        super().__init__(parent)
        self._cb = callback
        self._exclude = exclude
    def eventFilter(self, obj, event):
        t = event.type()
        if t in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick, QEvent.MouseButtonRelease) \
                and event.button() == Qt.LeftButton:
            if self._exclude is not None and self._exclude(event.position().toPoint()):
                return False
            if t != QEvent.MouseButtonRelease:
                self._cb()
            return True
        return False

class _WheelFilter(QObject):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self._cb = callback
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            self._cb(1 if event.angleDelta().y() > 0 else -1)
            return True
        return False

class DraggableOverlay(QFrame):
    HANDLE_H = 24

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self._drag_active = False
        self._drag_offset = QPoint()

        # Handle bar with toggle button
        self.handle = QWidget(self)
        self.handle.setStyleSheet("background-color: rgba(255, 255, 255, 200);")

        handle_layout = QHBoxLayout(self.handle)
        handle_layout.setContentsMargins(4, 0, 4, 0)
        handle_layout.setSpacing(6)

        self.toggle_btn = QPushButton("MPH", self.handle)
        self.toggle_btn.setFixedSize(40, 18)
        self.toggle_btn.setStyleSheet("font-size: 10px; padding: 0px;")
        handle_layout.addWidget(self.toggle_btn)

        self.compress_btn = QPushButton("Compress Gaps", self.handle)
        self.compress_btn.setCheckable(True)
        self.compress_btn.setFixedSize(90, 18)
        self.compress_btn.setStyleSheet("font-size: 9px; padding: 0px;")
        handle_layout.addWidget(self.compress_btn)

        handle_layout.addStretch()

        self.play_btn = QPushButton("▶ Play", self.handle)
        self.play_btn.setFixedSize(60, 20)
        self.play_btn.setStyleSheet("font-size: 10px; padding: 0px;")
        handle_layout.addWidget(self.play_btn)

        self.speed_lbl = QLabel("1x", self.handle)
        self.speed_lbl.setFixedWidth(36)
        self.speed_lbl.setStyleSheet("font-size: 10px; color: #333; background-color: transparent;")
        self.speed_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        handle_layout.addWidget(self.speed_lbl)

        handle_layout.addStretch()

        # The pool's On/Off, also off the main screen (Bill, 2026-10-16)
        self.pump_btn = QPushButton("On/Off", self.handle)
        self.pump_btn.setFixedSize(50, 20)
        self.pump_btn.setStyleSheet(
            "QPushButton { font-size: 11px; padding: 0px; background-color: #e1b9b9;"
            " border: 1px solid #9c7c7c; border-radius: 3px; }"
            " QPushButton:pressed { background-color: #c99d9d; }")
        handle_layout.addWidget(self.pump_btn)

        self.plot_btn = QPushButton("Close", self.handle)   # closes SwimPlotWindow, back to the calendar
        self.plot_btn.setFixedSize(50, 20)
        self.plot_btn.setStyleSheet("font-size: 11px; padding: 0px;")
        handle_layout.addWidget(self.plot_btn)

        # Content area below handle
        self.content = QWidget(self)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.setMouseTracking(True)
        self.handle.setMouseTracking(True)

    def resizeEvent(self, event):
        h = self.HANDLE_H
        self.handle.setGeometry(0, 0, self.width(), h)
        self.content.setGeometry(0, h, self.width(), self.height() - h)
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().toPoint().y() <= 24:
            self._drag_active = True
            self._drag_offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            new_pos = self.mapToParent(event.position().toPoint() - self._drag_offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        self._drag_active = False


#########  MAIN PROGRAM INITIALIZATION  ###########

# --- Standard output redirection, choose one from below:
original_stdout = sys.stdout
#print_device = "billtest.txt"  # just define this here within the program.
print_device = ""   # set to filename for logging, leave "" for terminal

if print_device != "":
    f = open(print_device, "w")
    sys.stdout = f


# ---------------------------------------------------------
# PyQt-only startup
# ---------------------------------------------------------

if __name__ == "__main__":

    # 1. Create QApplication FIRST
    qt_app = QApplication(sys.argv)

    # 2. Create App (logic only, NO Qt widgets)
    app = App()

    # 4. Create QtMainWindow AFTER App is ready
    window = QtMainWindow(app)
    app.window = window       # allow App.shutdown() to close the window
    window.show()
    app.start_relay_watchdog()

    # 5. Ensure shutdown runs when Qt exits normally
    qt_app.aboutToQuit.connect(app.shutdown)
    
    # Start Qt event loop and exit Python when it finishes
    sys.exit(qt_app.exec())

"""
===============================================================
POOLWIND → PW_TRAINING ARCHITECTURE SUMMARY (CORRECTED)
===============================================================

GOAL:
PoolWind collects synchronized swim data + perspect video.
PW_training later loads both and provides frame-accurate,
distance-accurate playback and analysis.

---------------------------------------------------------------
PART 1 — POOLWIND (DATA COLLECTION)
---------------------------------------------------------------

PoolWind produces TWO synchronized data streams:

(1) A perspect video file (AVI recommended)
(2) A CSV file containing swim metrics AND the video frame index

These two files together form a complete, synchronized dataset.

-------------------------
A. VIDEO CREATION (AVI)
-------------------------
PoolWind writes perspect video frames at a fixed FPS (e.g., 5–10 FPS).
Frames are written ONLY when the perspect writer decides it is time
(now - last_write >= period). This means:

- No frames are written during gaps.
- No blank frames are written.
- The video file stays small.
- AVI tolerates large timestamp gaps safely.

AVI is preferred because:
- It does not require continuous timestamps.
- It supports frame-accurate seeking.
- It tolerates long gaps without corruption.
- It is ideal for PW_training’s “jump to frame” playback.

-------------------------
B. CSV CREATION
-------------------------
PoolWind writes a CSV row ONLY when swimmerFound is True AND the
system is not suspended. This means:

- CSV pauses during gaps.
- CSV resumes when swimming resumes.
- CSV and video naturally stay aligned.

Add a new column:
    frame_number

Rules:
- Before the perspect writer starts: frame_number = 0
- Each time a perspect frame is written: increment frame_number
- All CSV rows between video frames repeat the same frame_number
  (but only if CSV is writing at all)

Because CSV pauses during gaps, there are no CSV rows to fill during
gaps. This keeps the CSV timeline clean and effort-driven.

---------------------------------------------------------------
PART 2 — PW_TRAINING (ANALYSIS & PLAYBACK)
---------------------------------------------------------------

PW_training loads:
- The CSV file (master timeline)
- The perspect video (frame store)

PW_training does NOT “play” the video like VLC.
Instead, it displays a single frame at a time, indexed by CSV.

-------------------------
A. MASTER TIMELINE
-------------------------
PW_training uses the CSV as the authoritative timeline.
The CSV contains:
- time
- distance
- velocity
- pace
- segment (One swim session may have several AVI files)
- frame_number

PW_training uses frame_number to fetch the correct video frame.

-------------------------
B. VIDEO ACCESS
-------------------------
PW_training opens the AVI file with OpenCV:

    cap = cv2.VideoCapture("perspect.avi")

To show a frame:
    cap.set(POS_FRAMES, frame_number)
    ret, frame = cap.read()

This is frame-accurate, gap-proof, and timestamp-independent.

-------------------------
C. SYNC BETWEEN PLOT AND VIDEO
-------------------------
When the user moves the plot cursor:
- PW_training reads the CSV row under the cursor.
- It extracts frame_number.
- It jumps the video to that frame.

When the user moves the video position (“scrubs”):
- PW_training reads the current frame index.
- It moves the plot cursor to the CSV row with that frame_number.

Distance can also be used as a secondary sync key.

-------------------------
D. PRIVACY BENEFIT
-------------------------
Because the video contains large timestamp gaps and is not a
standard playable movie, it will not play correctly in VLC,
QuickTime, or Windows Media Player.

Only PW_training can interpret it correctly because only PW_training
knows how to map CSV frame_number → video frame.

This provides privacy by architecture.

---------------------------------------------------------------
SUMMARY
---------------------------------------------------------------

PoolWind:
- Writes perspect video frames at fixed FPS (AVI recommended).
- Writes CSV rows only when swimmerFound is True and not suspended.
- Adds frame_number to each CSV row.
- Increments frame_number only when a video frame is written.
- CSV naturally pauses during gaps, matching video behavior.

PW_training:
- Loads CSV as the master timeline.
- Loads AVI as a frame store.
- Displays frames by direct frame index.
- Syncs plot and video using frame_number.
- Ignores timestamps entirely.
- Works even with huge gaps in video.
- Provides privacy because the video is not normally playable.

This architecture is robust, simple, gap-tolerant, and ideal for
future expansion.
===============================================================



===============================================================
Copy and paste hotkey trick with an undo just in case:
===============================================================

 Yes, write the AutoHotkey script and another to undo it in case it doesn't work.

Here's an AutoHotkey v2 script (current default if you downloaded from ahk.net recently) with two hotkeys — one to clean, one to undo. I combined them into a single file rather than two separate scripts, because the "undo" needs to remember what the clipboard looked like before the clean, and that's only reliable if both hotkeys live in the same running script (two separate scripts running as separate processes can't share that state without extra file I/O, which is more fragile).

Save as ClipboardEOL.ahk:
#Requires AutoHotkey v2.0
#SingleInstance Force

; Ctrl+Alt+V -> clean clipboard: convert CRLF/CR line endings to LF
; Ctrl+Alt+Z -> undo: restore clipboard to what it was right before the last clean

global ClipBackup := ""

^!v:: {
    global ClipBackup
    if (A_Clipboard = "") {
        ToolTip("Clipboard is empty")
        SetTimer () => ToolTip(), -1500
        return
    }
    ClipBackup := A_Clipboard
    cleaned := StrReplace(A_Clipboard, "`r`n", "`n")
    cleaned := StrReplace(cleaned, "`r", "`n")
    A_Clipboard := cleaned
    ToolTip("Clipboard cleaned (CRLF -> LF)")
    SetTimer () => ToolTip(), -1000
}

^!z:: {
    global ClipBackup
    if (ClipBackup = "") {
        ToolTip("Nothing to restore")
        SetTimer () => ToolTip(), -1500
        return
    }
    A_Clipboard := ClipBackup
    ClipBackup := ""
    ToolTip("Clipboard restored to original")
    SetTimer () => ToolTip(), -1000
}

If you have AutoHotkey v1 instead (check by right-clicking a .ahk file → "Run script" fails vs works, or check Start Menu for "AutoHotkey" vs "AutoHotkey v2"), use this version instead:

#SingleInstance Force
ClipBackup := ""

^!v::
if (Clipboard = "") {
    ToolTip, Clipboard is empty
    SetTimer, RemoveToolTip, -1500
    return
}
ClipBackup := Clipboard
Clipboard := StrReplace(Clipboard, "`r`n", "`n")
Clipboard := StrReplace(Clipboard, "`r", "`n")
ToolTip, Clipboard cleaned (CRLF -> LF)
SetTimer, RemoveToolTip, -1000
return

^!z::
if (ClipBackup = "") {
    ToolTip, Nothing to restore
    SetTimer, RemoveToolTip, -1500
    return
}
Clipboard := ClipBackup
ClipBackup := ""
ToolTip, Clipboard restored to original
SetTimer, RemoveToolTip, -1000
return

RemoveToolTip:
ToolTip
return

How to use it:
1. Copy your code as usual (Ctrl+C).
2. Press Ctrl+Alt+V — cleans the clipboard in place, shows a brief tooltip confirmation.
3. Paste into the Windows Terminal SSH session as normal.
4. If it still comes out wrong, press Ctrl+Alt+Z to instantly get your original clipboard back, then fall back to the Notepad trick for that paste.

To install: save the file, double-click it to run (AutoHotkey needs to be installed already). To have it always running, put a shortcut to the .ahk file in shell:startup (paste that into File Explorer's address bar to open the Startup folder).

Try it on a small multi-line snippet first to confirm it actually fixes the blank-line problem before trusting it on something long.


"""