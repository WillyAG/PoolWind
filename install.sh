#!/bin/bash
# PoolWind install script.
#
#   git clone https://github.com/WillyAG/PoolWind.git PoolWind-download || git -C PoolWind-download pull
#   cd PoolWind-download
#   bash install.sh
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
# The GitHub repository this copy was cloned from (its Release holds the
# sample video): a copy of the project, or a private test repository,
# downloads from itself. Not a clone: the author's.
REPO_URL="$(git -C "$SRC_DIR" remote get-url origin 2>/dev/null)"
REPO_URL="${REPO_URL%.git}"
case "$REPO_URL" in
    https://github.com/*/*) ;;
    git@github.com:*) REPO_URL="https://github.com/${REPO_URL#git@github.com:}" ;;
    *) REPO_URL="https://github.com/WillyAG/PoolWind" ;;
esac
PW_DIR="$HOME/PoolWind"
LOG="$PW_DIR/install.log"

# Python packages from PyPI, at the versions PoolWind was tested with.
PIP_PACKAGES="opencv-python==4.13.0.92 scipy==1.17.1 adafruit-circuitpython-ina260==1.3.21"

# Debian packages.
APT_PACKAGES="python3-numpy python3-scipy python3-matplotlib python3-pyside6.qtwidgets \
python3-lgpio python3-pip ffmpeg exfatprogs i2c-tools realvnc-vnc-server tmux"

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

# Since v15.8 PoolWind needs R6 and R3 on the interface board (it sees
# whether the pump is running). An update from a version without that asks
# first; nothing is changed if they aren't fitted (Bill, 2026-11-02: "let
# user decide if they want to upgrade to the version that requires the
# hardware change").
if [ -f "$PW_DIR/poolwind.py" ] && ! grep -q "PUMP_SENSE_PIN" "$PW_DIR/poolwind.py" \
        && grep -q "PUMP_SENSE_PIN" "$SOFTWARE/poolwind.py"; then
    echo
    say "This version of PoolWind needs two resistors, R6 and R3, fitted on the"
    say "interface board: they let PoolWind see whether the pool's pump is running"
    say "(build guide, section 4). Without them the new version won't start."
    read -r -p "Are R6 and R3 fitted on your interface board? (y/n) " answer
    echo "Answer: $answer" >> "$LOG"
    case "$answer" in
        [yY]*) ;;
        *)  say "Nothing was changed: your PoolWind stays as it is."
            say "Fit R6 and R3 first, then run this again."
            read -r -p "Press Enter to close."
            exit 0 ;;
    esac
fi

echo "Type your password when asked: the one you chose in Raspberry Pi Imager."
echo "(Nothing shows on the screen while you type it. Press Enter at the end.)"
if ! sudo -v; then
    echo "Couldn't get administrator rights (sudo). Nothing was changed."
    exit 1
fi
# Keep sudo's permission fresh until the script ends, so the password is
# asked for only once, however long the downloads take.
( while sleep 50; do sudo -n true 2> /dev/null || exit; done ) &
SUDO_KEEPALIVE=$!
trap 'kill $SUDO_KEEPALIVE 2> /dev/null' EXIT

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
# mkdir, mount): allow just these four commands without a password.
# (Harmless if this user's sudo needs no password anyway.)
tmp="$(mktemp)"
printf '%s ALL=(root) NOPASSWD: %s, %s, %s, %s\n' "$USER" \
    "$(command -v umount)" "$(sudo sh -c 'command -v mkfs.exfat')" \
    "$(command -v mkdir)" "$(command -v mount)" > "$tmp"
cat "$tmp" >> "$LOG"
run sudo visudo -c -f "$tmp"
run sudo install -m 0440 -o root -g root "$tmp" /etc/sudoers.d/poolwind
rm -f "$tmp"
say "   allowed setting up USB sticks without a password"

step "7/8  Copying PoolWind to $PW_DIR"
# An update: which version it was (the program's first line names it)
OLD_VER=""
NEW_VER="$(grep -m1 -o 'poolwindAI_v[0-9.]*[0-9]' "$SOFTWARE/poolwind.py" | sed 's/poolwindAI_//')"
if [ -f "$PW_DIR/poolwind.py" ]; then
    OLD_VER="$(grep -m1 -o 'poolwindAI_v[0-9.]*[0-9]' "$PW_DIR/poolwind.py" | sed 's/poolwindAI_//')"
    OLD_VER="${OLD_VER:-an earlier version}"
    run cp "$PW_DIR/poolwind.py" "$PW_DIR/poolwind.py.previous"
    say "   the previous program is kept as poolwind.py.previous"
fi
run cp "$SOFTWARE/poolwind.py" "$PW_DIR/poolwind.py"
say "   installed poolwind.py"
copy_if_missing "$SOFTWARE/poolwind_defaults.txt"    "$PW_DIR/poolwind_defaults.txt"
copy_if_missing "$SOFTWARE/poolwind_calibration.txt" "$PW_DIR/poolwind_calibration.txt"
# The sample swim (desk tests, and a 'Demo': True developer run), from the latest GitHub Release.
# Not needed at the pool, so a failed download doesn't stop the install.
if [ -f "$PW_DIR/PoolWind_demo.mp4" ]; then
    say "   kept PoolWind_demo.mp4"
elif curl -L -f -o "$PW_DIR/PoolWind_demo.mp4" \
        "$REPO_URL/releases/latest/download/PoolWind_demo.mp4" >> "$LOG" 2>&1; then
    say "   installed PoolWind_demo.mp4 (the demo's recorded swim)"
elif command -v gh >/dev/null 2>&1 && \
        gh release download --repo "${REPO_URL#https://github.com/}" --pattern PoolWind_demo.mp4 \
           --dir "$PW_DIR" --clobber >> "$LOG" 2>&1; then
    # (a private repository: only with GitHub's gh tool, signed in)
    say "   installed PoolWind_demo.mp4 (the demo's recorded swim)"
else
    rm -f "$PW_DIR/PoolWind_demo.mp4"
    say "   the sample video couldn't be downloaded: PoolWind says so if it's needed"
fi
run mkdir -p "$HOME/.local/bin"
# The Monitor Toggle script: always the new version, but keeping the monitor
# settings at its top (OUTPUT, PORTRAIT_SIZE, LANDSCAPE_SIZE) if already set.
TOGGLE="$HOME/.local/bin/toggle_monitor.sh"
if [ -f "$TOGGLE" ]; then
    run cp "$TOGGLE" "$TOGGLE.previous"
    new="$(mktemp)"
    cp "$SOFTWARE/toggle_monitor.sh" "$new"
    for v in OUTPUT PORTRAIT_SIZE LANDSCAPE_SIZE; do
        old_line="$(grep -m1 "^$v=" "$TOGGLE.previous")"
        if [ -n "$old_line" ]; then
            awk -v v="$v" -v l="$old_line" \
                'index($0, v "=") == 1 && !done { print l; done = 1; next } { print }' \
                "$new" > "$new.tmp" && mv "$new.tmp" "$new"
        fi
    done
    run cp "$new" "$TOGGLE"
    rm -f "$new"
    say "   updated toggle_monitor.sh (your monitor settings kept)"
else
    run cp "$SOFTWARE/toggle_monitor.sh" "$TOGGLE"
    say "   installed toggle_monitor.sh"
fi
run chmod +x "$TOGGLE"

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

# The Claude icon: Claude Code (an AI assistant, setup guide section 12)
# in this downloaded folder, which holds CLAUDE.md. Bill, 2026-11-03: the
# first click installs it and signs in, with nothing to type or paste; it
# runs in a tmux session, so the PC (over SSH) and the Pi share one live
# Claude.
CLAUDE_SH="$HOME/.local/bin/poolwind_claude.sh"
cat > "$CLAUDE_SH" << 'EOF'
#!/bin/bash
# PoolWind's Claude icon (written by install.sh): Claude Code in the
# PoolWind download folder, where CLAUDE.md gives it PoolWind's background.
# It runs in a tmux session, poolwind-claude: the icon on the Pi and this
# script from a PC over SSH both show that one session, so you can go from
# one to the other mid-conversation:
#     ssh -t yourname@poolwind.local .local/bin/poolwind_claude.sh
# Closing a window leaves Claude running; /exit in Claude ends it.
SRC_DIR="__SRC_DIR__"
SESSION=poolwind-claude
export PATH="$HOME/.local/bin:$PATH"

if [ "${1:-}" != "--inside" ] && command -v tmux > /dev/null; then
    if ! tmux has-session -t "$SESSION" 2> /dev/null; then
        tmux new-session -d -s "$SESSION" -x 120 -y 40 "$(readlink -f "$0") --inside"
        tmux set-option -t "$SESSION" window-size latest > /dev/null
        tmux set-option -t "$SESSION" status off > /dev/null
    fi
    exec tmux attach-session -t "$SESSION"
fi

done_key() { echo; read -r -p "Press Enter to close." _; exit "$1"; }
cd "$SRC_DIR" || { echo "The folder $SRC_DIR is missing."; done_key 1; }

if ! command -v claude > /dev/null; then
    echo "Installing Claude Code, an AI assistant that can help you set up, fix"
    echo "or change PoolWind (setup guide, section 12). It needs a paid Claude"
    echo "account; you can create one when you sign in."
    echo
    if ! curl -fsSL https://claude.ai/install.sh | bash; then
        echo "The install didn't work. Check the internet connection and try again."
        done_key 1
    fi
    # The installer may print a note about PATH with a line to copy: this
    # does it, so typing claude in any new terminal works too
    if ! grep -q '\.local/bin' "$HOME/.bashrc" 2> /dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"  # added by PoolWind for Claude Code' >> "$HOME/.bashrc"
    fi
    clear
    echo "Claude Code is installed."
    echo
fi

if ! claude auth status 2> /dev/null | grep -q '"loggedIn": *true'; then
    echo "Signing in to Claude."
    echo
    echo "The web browser opens on the Claude sign-in page:"
    echo "  - sign in with your email (Claude emails you a code to type in) or"
    echo "    with Google, or create an account (a paid plan is needed);"
    echo "  - then click Authorize. Claude Code finishes by itself."
    echo
    echo "From a PC over SSH, open the link it shows in the PC's browser, and"
    echo "paste the code that page gives you back here."
    echo
    if ! claude auth login --claudeai; then
        echo
        echo "Not signed in. Click the Claude icon to try again."
        done_key 1
    fi
    clear
    echo "Signed in."
    echo
fi

echo "Starting Claude. It has read CLAUDE.md, PoolWind's background."
sleep 2
# Carry on the last conversation in this folder, if there is one
if ls "$HOME/.claude/projects/$(pwd | sed 's/[^A-Za-z0-9]/-/g')"/*.jsonl > /dev/null 2>&1; then
    claude -c
else
    claude
fi
EOF
sed -i "s|__SRC_DIR__|$SRC_DIR|" "$CLAUDE_SH"
run chmod +x "$CLAUDE_SH"
# Written beside the desktop and moved in, so the file manager shows its name
tmp="$(mktemp)"
cat > "$tmp" << EOF
[Desktop Entry]
Type=Application
Name=Claude
Comment=Claude Code, an AI assistant for PoolWind (setup guide, section 12)
Exec=x-terminal-emulator -e $CLAUDE_SH
Path=$SRC_DIR
Icon=utilities-terminal
Terminal=false
EOF
chmod +x "$tmp"
run mv "$tmp" "$DESKTOP/Claude.desktop"
say "   added Claude (Claude Code, offered the first time it's opened)"

# The Copy Claude to USB icon: Claude Code's conversations and memory notes
# (~/.claude/projects) to a PoolWind_Claude folder on a USB stick, so they
# can go on with a new SD card. This script brings them back from the stick
# (--restore, below). Bill, 2026-11-03.
CLAUDE_USB_SH="$HOME/.local/bin/poolwind_claude_usb.sh"
cat > "$CLAUDE_USB_SH" << 'EOF'
#!/bin/bash
# PoolWind's Copy Claude to USB icon (written by install.sh).
#   poolwind_claude_usb.sh             copy Claude Code's conversations and
#                                      memory notes (~/.claude/projects) to
#                                      PoolWind_Claude on a USB stick
#   poolwind_claude_usb.sh --restore   copy them back from a stick, if one
#                                      has them (install.sh does this)
# Files already on the Pi are only replaced by newer ones. Sign-in isn't
# copied: Claude Code asks for it again on a new card.
PROJECTS="$HOME/.claude/projects"

# Mounted USB sticks: removable disks only (never the SD card), mounting
# one left unmounted (PoolWind unmounts its stick when it closes). Not a
# disk with a Linux partition or one mounted outside /media: a Raspberry
# Pi system card in a card reader, perhaps being written by SD Card Copier.
usb_sticks() {
    local r disk dev fs mp parts
    for r in /sys/block/sd*/removable; do
        [ "$(cat "$r" 2> /dev/null)" = 1 ] || continue
        disk="/dev/$(basename "$(dirname "$r")")"
        parts="$(lsblk -rpno PATH,FSTYPE,MOUNTPOINT "$disk" 2> /dev/null)"
        awk '$2 ~ /^ext/ || ($3 != "" && $3 !~ /^\/media\//) {bad = 1} END {exit !bad}' \
            <<< "$parts" && continue
        while read -r dev fs mp; do
            case "$fs" in exfat|vfat|ntfs|ntfs3) ;; *) continue ;; esac
            if [ -z "$mp" ]; then
                udisksctl mount -b "$dev" --no-user-interaction > /dev/null 2>&1
                mp="$(lsblk -rno MOUNTPOINT "$dev")"
            fi
            mp="$(printf '%b' "$mp")"          # lsblk writes a space as \x20
            [ -n "$mp" ] && [ -d "$mp" ] || continue
            echo "$mp"
        done <<< "$parts"
    done
}

copy_newer() {    # copy_newer FROM TO [progress]: newer files only
    mkdir -p "$2" || return 1
    if [ -n "${3:-}" ] && command -v rsync > /dev/null; then
        # the percentage as it goes; a USB stick keeps file times to the
        # 1/100 s, hence the window
        rsync -rt --update --modify-window=1 --info=progress2 --no-inc-recursive "$1/" "$2/"
    else
        cp -r --update --preserve=timestamps "$1/." "$2/"
    fi
}

# Claude Code keeps each conversation under the folder it was started in,
# and the Claude icon starts in the download folder. Conversations (and
# memory notes) from a folder this card doesn't have, such as one on the
# old card, go there, so the icon carries them on. Newer files win.
# Bill, 2026-11-03.
move_to_icon_folder() {
    local here d f cwd
    here="$PROJECTS/$(printf '%s' "__SRC_DIR__" | sed 's/[^A-Za-z0-9]/-/g')"
    for d in "$PROJECTS"/*/; do
        d="${d%/}"
        [ "$d" = "$here" ] && continue
        f="$(ls -t "$d"/*.jsonl 2> /dev/null | head -1)"
        [ -n "$f" ] || continue
        cwd="$(grep -m1 -o '"cwd":"[^"]*"' "$f" | cut -d'"' -f4)"
        [ -n "$cwd" ] && [ ! -d "$cwd" ] || continue
        if copy_newer "$d" "$here"; then
            rm -rf "$d"
            echo "   Claude's conversations from $cwd (not on this card) moved so the Claude icon goes on with them"
        fi
    done
}

if [ "${1:-}" = "--restore" ]; then
    while read -r stick; do
        [ -d "$stick/PoolWind_Claude/projects" ] || continue
        if copy_newer "$stick/PoolWind_Claude/projects" "$PROJECTS"; then
            echo "   Claude's conversations copied from the USB stick $(basename "$stick")"
        else
            echo "   Claude's conversations on the USB stick $(basename "$stick") couldn't all be copied"
        fi
        break
    done < <(usb_sticks)
    [ -d "$PROJECTS" ] && move_to_icon_folder
    exit 0
fi

finish() { echo; read -r -p "Press Enter to close."; exit "$1"; }

echo "Copy Claude to USB"
echo
echo "Copies Claude Code's conversations and memory notes to a USB stick,"
echo "so they can go on with a new SD card: plug the stick in before running"
echo "the install script there, and it copies them back."
echo
if [ ! -d "$PROJECTS" ]; then
    echo "There are no Claude conversations on this Pi yet."
    finish 0
fi
mapfile -t sticks < <(usb_sticks)
if [ "${#sticks[@]}" -eq 0 ]; then
    echo "No USB stick found. Plug one in and try again."
    finish 1
fi
stick=""
for s in "${sticks[@]}"; do        # the stick that has them already
    [ -d "$s/PoolWind_Claude" ] && { stick="$s"; break; }
done
if [ -z "$stick" ] && [ "${#sticks[@]}" -eq 1 ]; then
    stick="${sticks[0]}"
fi
if [ -z "$stick" ]; then
    echo "Which USB stick?"
    for i in "${!sticks[@]}"; do echo "  $((i + 1))  $(basename "${sticks[$i]}")"; done
    read -r -p "Number: " n
    case "$n" in ''|*[!0-9]*) n=0 ;; esac
    if [ "$n" -lt 1 ] || [ "$n" -gt "${#sticks[@]}" ]; then
        echo "Nothing was copied."
        finish 1
    fi
    stick="${sticks[$((n - 1))]}"
fi
echo "Copying to the USB stick $(basename "$stick")."
echo "(Close Claude first, so the copy has the whole conversation.)"
echo "A long conversation can take a few minutes; the line below shows how"
echo "far it has got (the percentage)."
echo
if copy_newer "$PROJECTS" "$stick/PoolWind_Claude/projects" progress && echo &&
        echo "Finishing writing to the stick..." && sync; then
    echo
    echo "Done: $(du -sh "$stick/PoolWind_Claude" | cut -f1) in PoolWind_Claude on $(basename "$stick")."
    echo "The stick holds everything said and read in those conversations:"
    echo "keep it to yourself."
    finish 0
fi
echo
echo "The copy didn't finish (is the stick full?). Nothing on the Pi was changed."
finish 1
EOF
sed -i "s|__SRC_DIR__|$SRC_DIR|" "$CLAUDE_USB_SH"
run chmod +x "$CLAUDE_USB_SH"
tmp="$(mktemp)"
cat > "$tmp" << EOF
[Desktop Entry]
Type=Application
Name=Copy Claude to USB
Comment=Copy Claude Code's conversations to a USB stick, for a new SD card (setup guide, section 12)
Exec=x-terminal-emulator -e $CLAUDE_USB_SH
Icon=drive-removable-media
Terminal=false
EOF
chmod +x "$tmp"
# Its icon only for whoever keeps Claude's conversations on a stick: a stick
# with them plugged in now (copied back here), or the icon there already
restored="$("$CLAUDE_USB_SH" --restore 2>> "$LOG")"
if [ -n "$restored" ] || [ -e "$DESKTOP/Copy_Claude_to_USB.desktop" ]; then
    run mv "$tmp" "$DESKTOP/Copy_Claude_to_USB.desktop"
    say "   added Copy Claude to USB"
else
    rm -f "$tmp"
fi
[ -n "$restored" ] && say "$restored"

# Turn the monitor to portrait every time the desktop starts, so it's
# always ready for swimming. (The Monitor Toggle icon still switches to
# landscape for working.)
run mkdir -p "$HOME/.config/autostart"
cat > "$HOME/.config/autostart/poolwind-portrait.desktop" << EOF
[Desktop Entry]
Type=Application
Name=PoolWind portrait monitor
Comment=Turn the pool monitor to portrait when the desktop starts
Exec=sh -c 'sleep 3; $TOGGLE portrait'
Terminal=false
EOF
say "   the monitor turns to portrait each time the Pi starts"

# --------------------------------------------------------------------------
step "Done"
if [ -n "$OLD_VER" ]; then
    # An update: what was kept, and what's new (software/WHATS_NEW.txt)
    if [ "$OLD_VER" = "$NEW_VER" ]; then
        say "PoolWind $NEW_VER was already installed: the program was copied again."
    else
        say "PoolWind is updated from $OLD_VER to $NEW_VER."
    fi
    say "Kept as they were: your settings (poolwind_defaults.txt), your pool's"
    say "calibration (poolwind_calibration.txt), swim logs, videos and USB sticks."
    say "The previous program is kept as poolwind.py.previous."
    if [ "$OLD_VER" != "$NEW_VER" ] && [ -f "$SOFTWARE/WHATS_NEW.txt" ]; then
        say ""
        while IFS= read -r line; do say "$line"; done < "$SOFTWARE/WHATS_NEW.txt"
    fi
    say ""
    say "Next: restart the Pi, then start PoolWind as usual."
    exit 0
fi
say "PoolWind is installed in $PW_DIR."
say ""
say "Next:"
say "  1. Restart the Pi (Raspberry Pi menu -> Shutdown -> Reboot)."
say "  2. Check the voltage sensor: in a terminal, 'i2cdetect -y 1' shows 40."
say "  3. Continue with the setup guide, section 4, First start."
