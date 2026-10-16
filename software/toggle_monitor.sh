#!/bin/bash
# PoolWind Monitor Toggle: switches the pool monitor between portrait (for
# swimming) and landscape (for working on the Pi, for example over VNC).
# See the setup guide, section 9, "Working from home".
#
# Always switch back to portrait before anyone swims.
#
#   toggle_monitor.sh            switch between portrait and landscape
#   toggle_monitor.sh portrait   portrait (run at every start, set up by
#                                the install script)
#   toggle_monitor.sh landscape  landscape
#
# --- Settings for your monitor -------------------------------------------
# Set up for the author's Eyoyo 10-inch monitor. For another monitor, type
# `xrandr` in a terminal: it lists the output name (the line that says
# "connected") and the sizes the monitor offers.
OUTPUT="HDMI-1"            # the monitor's output name
PORTRAIT_SIZE="800x600"    # size used in portrait, before turning
LANDSCAPE_SIZE="1280x800"  # size used in landscape
# ---------------------------------------------------------------------------

export DISPLAY="${DISPLAY:-:0}"
line=$(xrandr --query | grep "^$OUTPUT connected")
if [ -z "$line" ]; then
    echo "Monitor Toggle: no monitor connected on $OUTPUT (see the settings at the top of $0)" >&2
    exit 1
fi
want="${1:-}"
if [ -z "$want" ]; then
    if echo "$line" | grep -q '+[0-9]* left ('; then
        want=landscape
    else
        want=portrait
    fi
fi
case "$want" in
    portrait)  xrandr --output "$OUTPUT" --mode "$PORTRAIT_SIZE" --rotate left ;;
    landscape) xrandr --output "$OUTPUT" --mode "$LANDSCAPE_SIZE" --rotate normal ;;
    *) echo "Monitor Toggle: use 'portrait', 'landscape' or nothing (to switch)" >&2
       exit 1 ;;
esac
