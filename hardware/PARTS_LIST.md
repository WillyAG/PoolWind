# PoolWind Parts List

**DRAFT.** The examples are the parts the author used. Any equivalent part
will do. Prices are approximate US prices checked in October 2026; they
change often, so check before buying. If an example is no longer sold,
Amazon usually shows a replacement: choose one that matches the
description and the notes. Comments like `<!-- Bill: ... -->` are notes
for the author.

License: see [LICENSE.md](../LICENSE.md).

| # | Part | Example | Price (2026, approx.) | Notes |
|---|---|---|---|---|
| 1 | Raspberry Pi 5 (8 GB) starter kit, with case, active cooler, 27 W power supply and microSD card | for example the 52Pi kit | $140 | The original build used a Raspberry Pi 4 |
| 2 | Wide-angle USB webcam: Spedal 920 Pro Conference Camera, 120° view | [amazon.com/dp/B07TDQ8NL3](https://www.amazon.com/dp/B07TDQ8NL3) | $44 | Mounted above the swim area. PoolWind uses it at 640×480. (On the Raspberry Pi it identifies itself as a "Vitade AF" USB camera.) |
| 3 | Waterproof keyboard: foldable silicone roll-up keyboard, USB | [amazon.com/dp/B06WWM5TC6](https://www.amazon.com/dp/B06WWM5TC6) | $15–20 | Has held up very well at the poolside and dries out easily |
| 4 | Waterproof mouse: Adesso iMouse W3, USB | [amazon.com/dp/B01LXR3R5J](https://www.amazon.com/dp/B01LXR3R5J) | $30 | |
| 5 | Waterproof case with a clear cover: LMioEtool IP65 box, 11.4 × 7.5 × 5.5 in | [amazon.com/dp/B07PDV2F2N](https://www.amazon.com/dp/B07PDV2F2N) | $45–115 | Holds the Raspberry Pi, the interface board and the monitor at the poolside. Similar boxes vary widely in price |
| 6 | Monitor: Eyoyo 10-inch IPS LCD, 1280×800 | [amazon.com/dp/B072N2YGXN](https://www.amazon.com/dp/B072N2YGXN) | $90–110 | Mounted in portrait. 245 × 166 × 33 mm: it only just fits the case, and its control buttons had to be removed. Check the fit against your case. Some Eyoyo 10-inch models are only 1024×768: check the resolution |
| 7 | USB extension cable, 10 ft: AINOPE USB 3.0 | [amazon.com/dp/B07ZV6FHWF](https://www.amazon.com/dp/B07ZV6FHWF) | $6 | For the camera. A longer run may need an active (repeater) USB extension |
| 8 | RJ45 jacks: Treedix RJ45 8-pin connector and breakout board kit (4 jacks, each with a small breakout board) | [amazon.com/dp/B08HGS5G8N](https://www.amazon.com/dp/B08HGS5G8N) | $11–15 | One kit covers all three jacks. Two are soldered straight onto the interface board (the Pace jack and the Remote jack), without their breakout boards. The third, on its breakout board, is mounted on the back of the modified remote (see the build guide, section 5) |
| 9 | INA260 voltage/current sensor breakout: Adafruit #4226 | [adafruit.com/product/4226](https://www.adafruit.com/product/4226) | $10 | Plugs into a header on the interface board. Reads the Pace Display port voltage over I2C. Must be an **INA260**: the program uses the INA260 library |
| 10 | Relay modules: 5 V 2-channel relay module with optocoupler (2), with 5 V relays such as JQC-3FF-S-Z or Songle SRD-05VDC-SL-C | [amazon.com/dp/B078478SZ9](https://www.amazon.com/dp/B078478SZ9) (4-pack) | $12–17 | Four relays: Up, Down, On/Off and one spare. Powered from the Raspberry Pi's 5 V. Switched by GPIO 17, 18 and 27, active low |
| 11 | Pool remote: Endless Pools EP1 water-resistant remote transmitter (inside: Martec BT-433M board) | myendlesspool.com | $45 | Wired to the relays, and powered from the Raspberry Pi instead of its batteries (see the build guide). Two come with the pool: modify one and keep the other unmodified for manual control. Buy a spare if you want to keep both |
| 12 | Interface board (PCB), two-layer, 117 × 88 mm | Upload [`gerbers/PoolWind_PCB_gerbers.zip`](gerbers/PoolWind_PCB_gerbers.zip) to any PCB maker | $10–30 for 5, plus shipping | Carries the INA260 breakout, the connections to the relays and both RJ45 jacks. Designed in [Fritzing](https://fritzing.org). Boards over 100 × 100 mm cost more than the makers' cheapest offers: upload the ZIP for an exact quote |
| 13 | Ribbon cable: 40-pin GPIO cable, female to female (2 × 20) | | $3–8 | Connects the Raspberry Pi to the interface board. It plugs onto all 40 of the Pi's GPIO pins; at the board end the plug fits over the board's 24-pin header, with the rest of the plug hanging past its end (there's plenty of room) |
| 14 | Resistors R6 = 100 kΩ and R3 = 7.5 kΩ, ¼ W (currently unused) | | | **Not needed now: leave them out.** They form a voltage divider meant for detecting whether the pool is on: the Pace Display port's power line (about 38 V) through R6, R3 to ground, the middle to GPIO 23, giving about 2.7 V. The program doesn't use it. Never fit lower values: the first design's 220 Ω pair would have put about 19 V on the GPIO pin and destroyed it |
| 15 | Header pins and sockets, wire, solder | | $5–10 | Male header pins: one 2 × 12 (ribbon cable) and four 1 × 12 (relay headers JP1-JP4), cut from breakaway strips. One 1 × 8 female socket strip for the INA260 |
| 16 | Cable glands, waterproof (IP68: dust-tight and sealed against water), sized for the cables | | $5–10 | Seal the cables where they leave the case. Nylon PG7/PG9 or M12/M16 glands are common and cost well under $1 each; mixed kits cost more. A split gland fits around a cable whose plug won't pass through. Let each cable sag in a drip loop below the case |
| 17 | USB extension cable for the swimmer's USB stick | | $6 | So the stick can be plugged in outside the closed case |
| 18 | Network cable, straight-through, Cat5e or Cat6 | | $5–12 | Remote to the interface board. Length to suit your pool |
| 19 | Phone cable(s), standard 6-wire (6P6C) | | $5–10 | From the pool controller's Pace Display port to the interface board's Pace jack (a phone plug fits the RJ45 jack). Length to suit your pool. **If a Pace Display is already installed:** a short cable from the port to the Y splitter, and a longer one from the splitter to the interface board |
| 20 | Y splitter for the Pace Display cable (only if you have a Pace Display) | | | Must connect every wire straight through to both outlets. Many phone splitters are "L1/L2" types that split the wires between the outlets: these won't work. A "6P6C (RJ12) straight-through" splitter carries all six wires. See the build guide, section 6 |
| 21 | Heatsink, about 3 × 4 in (only if the Raspberry Pi will run for hours at a time) | | | Mounted in a sealed hole in the case wall, fins outside. See the build guide, section 8 |
| 22 | For the remote's watertight box: a small clear plastic box, silicone putty, electrical tape, small desiccant packs | | $5–15 | Any spare box that fits the remote will do. See the build guide, section 5 |
| | **Total (without the remote)** | | **about $480** | Mostly depends on the case and the monitor |

<!-- Bill: open questions
- Bill has two spare interface PCBs (could be offered to early builders?).
- Anything missing: camera mount, monitor power supply, GFCI outlet.
- The heatsink you used (link or size), and the Y splitter once verified.
-->
