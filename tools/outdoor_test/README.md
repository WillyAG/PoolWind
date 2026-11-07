# Outdoor test tools

For a builder whose pool is outdoors, or anyone whose swimmer detection
goes wrong in their light. These scripts only read recorded video: nothing
here moves the jet.

PoolWind was developed under a tent roof. Before anyone had swum with it
outdoors, Claude tested its swimmer detection on the author's recordings
with shade, dappled light, glare and leaves painted in. It held up well as
it is. The results, what's still unknown, and where to go from there are in
[CLAUDE.md](../../CLAUDE.md), "Outdoor pools". Claude Code reads that
section, so it can help you carry on.

| File | What it is |
|---|---|
| `compare.py` | Runs PoolWind's own swimmer detection (imported from `poolwind.py`) and the tracker side by side on recordings, with or without painted distractors, and counts how often each loses the swimmer |
| `tracker.py` | A swimmer tracker, a prototype: it finds the swimmer once, then follows them, looking only near where they should be and checking the blob still looks like them. Not part of PoolWind |

## Using them

1. **Record your pool** in the light that gives trouble. In
   `poolwind_defaults.txt`, set `'developerMode': True` and
   `'recordRawVideo': True`, then swim. PoolWind saves the camera's own
   picture as `Raw_<date>_<time>.mp4` in the `PoolWind` folder, next to
   the program (when it closes, it also makes a smaller copy ending in
   `.mp4.mp4`). The files are large: set it back to `False` afterwards.
2. **Compare**, in a terminal in this folder:
   ```
   python3 compare.py ~/path/to/Raw_recording.mp4 --sheet disagree.jpg
   ```
   It uses the swim area's corners from your calibration file. If the
   camera has moved since the recording, give them with
   `--corners "x,y x,y x,y x,y"`. `--start` and `--seconds` choose the
   part of the recording, `--paint clean,shadow,glare,dapple,leaves,clumps`
   adds painted distractors. `python3 compare.py --help` lists everything.
3. **Look at `disagree.jpg`**: frames where the two disagree, PoolWind's
   detection as a red line, the tracker's green. On a recording where
   PoolWind goes wrong, these pictures show which one is right.

Change the tracker (or PoolWind's `F_mask` and `get_auto_CoM` in your own
copy) and compare again. Test any change at a desk first, then at the pool
with nobody in it, watching the jet (CLAUDE.md, safety rules).

If you get PoolWind working outdoors, please share how in
[Discussions](https://github.com/WillyAG/PoolWind/discussions).
