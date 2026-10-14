#!/bin/bash
# PoolWind install script.
#
#   git clone https://github.com/<user>/PoolWind.git ~/PoolWind-download
#   bash ~/PoolWind-download/install.sh
#
# Sets up a Raspberry Pi 5 running Raspberry Pi OS (64-bit, with desktop)
# for PoolWind. See docs/SETUP_GUIDE.md, section 3. Safe to run again: it
# updates the program but never overwrites settings, calibration, swim logs
# or videos. Everything it does is written to ~/PoolWind/install.log.
#
# License: see LICENSE.md.

set -u

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOFTWARE="$SRC_DIR/software"
PW_DIR="$HOME/PoolWind"
LOG="$PW_DIR/install.log"

# Python packages from PyPI, at the versions PoolWind was tested with.
PIP_PACKAGES="opencv-python==4.13.0.92 scipy==1.17.1 adafruit-circuitpython-ina260==1.3.21"

# Debian packages.
APT_PACKAGES="python3-numpy python3-scipy python3-matplotlib python3-pyqt5 \
python3-lgpio python3-pip ffmpeg exfatprogs i2c-tools realvnc-vnc-server"

# --------------------------------------------------------------------------
# Helpers

say()  { echo "$*"; echo "$*" >> "$LOG"; }
step() { echo; echo "== $*"; printf '\n== %s  (%s)\n' "$*" "$(date '+%H:%M:%S')" >> "$LOG"; }

# Run a command, writing it and its output to the log. Stop on failure.
run() {
    echo "\$ $*" >> "$LOG"
    if ! "$@" >> "$LOG" 2>&1; then
        echo
        echo "FAILED: $*"
        echo "Nothing after this step was done. The details are in:"
        echo "    $LOG"
        echo "Fix the problem (often the internet connection) and run the script again."
        echo "FAILED: $*" >> "$LOG"
        exit 1
    fi
}

# Copy a file only if the destination doesn't exist yet.
copy_if_missing() {
    if [ -e "$2" ]; then
        say "   kept your existing $(basename "$2")"
    else
        run cp "$1" "$2"
        say "   installed $(basename "$2")"
    fi
}

# --------------------------------------------------------------------------
# Checks before changing anything

if [ "$(id -u)" -eq 0 ]; then
    echo "Run this script as your normal user, not with sudo:"
    echo "    bash $0"
    exit 1
fi

for f in poolwind.py poolwind_defaults.txt poolwind_calibration.txt toggle_monitor.sh; do
    if [ ! -f "$SOFTWARE/$f" ]; then
        echo "Missing $SOFTWARE/$f. Download PoolWind again (setup guide, section 3)."
        exit 1
    fi
done

mkdir -p "$PW_DIR"
{
    echo
    echo "################################################################"
    echo "PoolWind install  $(date '+%Y-%m-%d %H:%M:%S')"
    echo "From: $SRC_DIR"
    echo "User: $USER   Home: $HOME"
    uname -a
    grep PRETTY_NAME /etc/os-release
    cat /proc/device-tree/model 2>/dev/null; echo
} >> "$LOG"

echo "PoolWind install. Everything it does is logged in $LOG"

if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    say "WARNING: this doesn't look like a Raspberry Pi. PoolWind needs one."
fi
if ! command -v raspi-config > /dev/null; then
    echo "raspi-config not found: this needs Raspberry Pi OS (setup guide, section 2)."
    exit 1
fi

echo "Your password may be asked for once (for installing system packages)."
if ! sudo -v; then
    echo "Couldn't get administrator rights (sudo). Nothing was changed."
    exit 1
fi

# --------------------------------------------------------------------------
step "1/8  Installing system packages (this can take several minutes)"
run sudo apt-get update
run sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y $APT_PACKAGES

step "2/8  Installing Python packages"
run pip install --user --break-system-packages $PIP_PACKAGES

step "3/8  Turning on I2C (for the voltage sensor)"
run sudo raspi-config nonint do_i2c 0

step "4/8  Switching the desktop to X11"
# PoolWind is tested on X11, and the Monitor Toggle and RealVNC need it.
# Takes effect after the restart.
run sudo raspi-config nonint do_wayland W1

step "5/8  Turning on VNC (RealVNC), for working from another computer"
# raspi-config's own VNC option looks at the desktop running right now,
# which on a new card is still Wayland, so set up RealVNC directly.
# Turn off Wayland's VNC server (wayvnc), if it's there.
sudo systemctl disable wayvnc.service >> "$LOG" 2>&1 || true
run sudo systemctl enable vncserver-x11-serviced.service

step "6/8  Hardware access and USB sticks"
for g in gpio i2c video; do
    if getent group "$g" > /dev/null; then
        run sudo usermod -aG "$g" "$USER"
    fi
done
# PoolWind sets up new swimmer USB sticks with sudo (umount, mkfs.exfat,
# mkdir, mount). Raspberry Pi OS's first user may already use sudo without
# a password; if not, allow just these four commands.
sudo -k    # forget the password typed earlier, to test the real setting
if sudo -n true 2> /dev/null; then
    say "   sudo already works without a password: nothing to add"
else
    sudo -v
    tmp="$(mktemp)"
    printf '%s ALL=(root) NOPASSWD: %s, %s, %s, %s\n' "$USER" \
        "$(command -v umount)" "$(sudo sh -c 'command -v mkfs.exfat')" \
        "$(command -v mkdir)" "$(command -v mount)" > "$tmp"
    cat "$tmp" >> "$LOG"
    run sudo visudo -c -f "$tmp"
    run sudo install -m 0440 -o root -g root "$tmp" /etc/sudoers.d/poolwind
    rm -f "$tmp"
    say "   allowed setting up USB sticks without a password"
fi

step "7/8  Copying PoolWind to $PW_DIR"
if [ -f "$PW_DIR/poolwind.py" ]; then
    run cp "$PW_DIR/poolwind.py" "$PW_DIR/poolwind.py.previous"
    say "   the previous program is kept as poolwind.py.previous"
fi
run cp "$SOFTWARE/poolwind.py" "$PW_DIR/poolwind.py"
say "   installed poolwind.py"
copy_if_missing "$SOFTWARE/poolwind_defaults.txt"    "$PW_DIR/poolwind_defaults.txt"
copy_if_missing "$SOFTWARE/poolwind_calibration.txt" "$PW_DIR/poolwind_calibration.txt"
run mkdir -p "$HOME/.local/bin"
copy_if_missing "$SOFTWARE/toggle_monitor.sh" "$HOME/.local/bin/toggle_monitor.sh"
run chmod +x "$HOME/.local/bin/toggle_monitor.sh"

step "8/8  Desktop icons"
DESKTOP="$(xdg-user-dir DESKTOP 2> /dev/null || echo "$HOME/Desktop")"
run mkdir -p "$DESKTOP"
cat > "$DESKTOP/PoolWind.desktop" << EOF
[Desktop Entry]
Type=Application
Name=PoolWind
Comment=Start PoolWind
Exec=/usr/bin/python3 $PW_DIR/poolwind.py
Path=$PW_DIR
Icon=applications-games
Terminal=false
EOF
cat > "$DESKTOP/Monitor_Toggle.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Monitor Toggle
Comment=Turn the pool monitor between portrait (swimming) and landscape (working)
Exec=$HOME/.local/bin/toggle_monitor.sh
Icon=video-display
Terminal=false
EOF
run chmod +x "$DESKTOP/PoolWind.desktop" "$DESKTOP/Monitor_Toggle.desktop"
say "   added PoolWind and Monitor Toggle"

# --------------------------------------------------------------------------
step "Done"
say "PoolWind is installed in $PW_DIR."
say ""
say "Next:"
say "  1. Restart the Pi (Raspberry Pi menu -> Shutdown -> Reboot)."
say "  2. Check the voltage sensor: in a terminal, 'i2cdetect -y 1' shows 40."
say "  3. Continue with the setup guide, section 4, First start."
