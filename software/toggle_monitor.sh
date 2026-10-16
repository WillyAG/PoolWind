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
# Set up for the author's Eyoyo 10-inch monitor. Another monitor usually
# works without changes: if the output below isn't connected, the first
# connected monitor is used, and a size the monitor doesn't offer (or
# "auto") uses the monitor's own preferred size. PoolWind adapts to
# whatever size the screen has. To choose sizes yourself, type `xrandr` in
# a terminal: it lists the output name (the line that says "connected")
# and the sizes the monitor offers.
OUTPUT="HDMI-1"            # the monitor's output name
PORTRAIT_SIZE="800x600"    # size used in portrait, before turning, or "auto"
LANDSCAPE_SIZE="1280x800"  # size used in landscape, or "auto"
# ---------------------------------------------------------------------------

export DISPLAY="${DISPLAY:-:0}"
query=$(xrandr --query)
line=$(echo "$query" | grep -m1 "^$OUTPUT connected")
if [ -z "$line" ]; then
    line=$(echo "$query" | grep -m1 "^[^ ]* connected")
    if [ -z "$line" ]; then
        echo "Monitor Toggle: no monitor found" >&2
        exit 1
    fi
    OUTPUT="${line%% *}"
fi

# The sizes this monitor offers (the indented lines under its output).
modes=$(echo "$query" | awk -v o="$OUTPUT" '
    $1 == o { inside = 1; next }
    /^[^ ]/ { inside = 0 }
    inside  { print $1 }')

# xrandr arguments for a size: the size itself if the monitor offers it,
# otherwise the monitor's preferred size.
size_args() {
    if [ "$1" != "auto" ] && echo "$modes" | grep -qx "$1"; then
        echo "--mode $1"
    else
        echo "--auto"
    fi
}

want="${1:-}"
if [ -z "$want" ]; then
    if echo "$line" | grep -q '+[0-9]* left ('; then
        want=landscape
    else
        want=portrait
    fi
fi
case "$want" in
    portrait)  xrandr --output "$OUTPUT" $(size_args "$PORTRAIT_SIZE") --rotate left ;;
    landscape) xrandr --output "$OUTPUT" $(size_args "$LANDSCAPE_SIZE") --rotate normal ;;
    *) echo "Monitor Toggle: use 'portrait', 'landscape' or nothing (to switch)" >&2
       exit 1 ;;
esac
