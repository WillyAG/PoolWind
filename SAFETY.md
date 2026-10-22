# Safety: read this first

PoolWind controls the speed of a swimming current. You build it, install it
and use it **entirely at your own risk**. It is provided "as is", with no
warranty of any kind, and the author accepts no liability for injury, damage
or loss arising from building or using it. See the licenses in [LICENSE.md](LICENSE.md)
for the full disclaimer.

## Electrical

- **Keep all electronics low-voltage and dry.** The Raspberry Pi, relay board,
  sensor and monitor must be powered from a proper low-voltage power supply,
  mounted away from splashing water. The keyboard and mouse must be waterproof.
- **Use certified power supplies only** (for example UL-listed), and never
  bring mains wiring into the station's case beyond the supplies' own plugs.
  Their low-voltage outputs are isolated from the mains, which is what makes
  touching the keyboard or mouse safe while standing in the pool.
- **Plug the power supplies into a GFCI-protected outlet,** placed as your
  local electrical code requires for outlets near a pool. In the US that is
  NEC Article 680: outlets at least 6 ft (1.8 m) from the water, and
  GFCI-protected within 20 ft (6 m). Rules vary by place and code edition,
  so follow your local code. The GFCI is the main protection: if a power
  supply ever fails and mains current leaks out through a person, it cuts
  the power in a fraction of a second.
- **The Pace Display cable's ground is not a safety ground.** It is one thin
  phone wire that gives the sensor a reference for its reading. It is not
  meant to carry fault current. Without it, PoolWind's low-voltage side
  simply floats, like a laptop on its charger: the jet speed reading stops
  working, but that adds no electrical risk.
- **Do not modify the pool's own control box, pump or wiring.**
  PoolWind only connects to a handheld remote and to the Pace Display port.
  If the port is inside the control box, turn the pool's power off before
  opening it to plug in the cable.
- **Connecting PoolWind may affect your pool's warranty.** Check your
  warranty before you build. That decision, and its risk, are yours.
- **If you are not confident with electronics near water, have a qualified
  electrician check your installation.**

## Using the pool

- **To control the pool by hand, close PoolWind.** While PoolWind is running
  it keeps setting the jet speed itself: if you change the speed with the
  pool's own remote, PoolWind changes it back. Hold and Suspend don't stop
  this either. The pool also can't receive two remotes at the same time.
  When PoolWind is closed, it releases all its relays and the pool works
  exactly as manufactured with its own remote. **Closing PoolWind doesn't
  slow the jet:** it stays at the speed it had. PoolWind winds the jet down
  to its lowest setting when its **OnOff** button is pressed, before it
  turns the pump on or off.
- **Before relying on PoolWind, confirm the pool's own remote works** to slow
  down and stop the jet after PoolWind is closed.
- **Never swim alone** while testing a new build or new settings.
- **Test with the pool empty of swimmers first.** Watch the jet respond to the
  program before you get in, make sure it goes to the lowest flow.
- **Set sensible limits** for each swimmer's ability: their slowest and
  fastest zone on their USB stick (Swimmer limits), and the pace limits in
  the defaults file for anyone without a stick. The **safety voltage
  limits** in the calibration file are fitted to your pool by the
  calibration's scan. The program will not command speeds outside them.
  The calibration file is for technician changes only.
- **The calibration moves the jet to fast speeds.** Nobody in the pool
  while it runs. During the scan, when the pool sounds too fast or
  strained, press **Stop**, then **Use as top**: PoolWind then never drives
  the jet faster than that.
- **Each swimmer's USB stick is personal.** Its zone limits decide how fast
  the jet can go for that swimmer. A child or weak swimmer using a strong
  swimmer's stick could be faced with a current they can't handle. Give
  every swimmer their own stick with a fastest zone that suits them, and never
  swap sticks.
- **Children and weak swimmers:** use a low fastest zone on their stick, and do
  not let PoolWind control the current for anyone who couldn't handle the
  jet at the fastest pace their stick allows. Supervise them.
- **Without a USB stick, the defaults file's pace limits apply.** The shipped
  defaults file uses a moderate top pace (3:00 per 100 yards) as a safe
  starting point. If you raise it for yourself, remember it then applies to
  anyone who swims without their own stick.

## The remote

- Soldering to a remote will probably **void that remote's warranty**. Buy a
  spare remote to modify and keep your original untouched.
- The modified remote (used by PoolWind) and the pool's normal remote both
  work, but **not at the same time**: the pool can only receive one remote
  at a time. Close PoolWind before using the normal remote.

## Not affiliated

PoolWind is an independent project, not affiliated with or endorsed by the
pool manufacturer. Contact the manufacturer about your pool itself, not about
PoolWind.
