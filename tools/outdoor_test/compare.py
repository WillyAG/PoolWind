"""
PoolWind's swimmer detection against the tracker prototype, on recorded
swims. Nothing here moves the jet: it only reads video files.

    python3 compare.py RECORDING.mp4 [MORE.mp4 ...]
        [--program PATH]     poolwind.py to take the detection from
                             (default: ../../software/poolwind.py)
        [--corners "x,y x,y x,y x,y"]   the swim area's corners in the
                             recording (default: swimAreaPoints from the
                             calibration file next to the program)
        [--start S] [--seconds S]   which part of each recording (default:
                             from 0 s, 60 s of it)
        [--step N]           every Nth frame (default 2: 15 of the camera's
                             30 frames a second, about PoolWind's own rate)
        [--paint LIST]       distractors painted in, comma separated:
                             clean, shadow, glare, dapple, leaves, clumps
                             (default: clean)
        [--sheet FILE.jpg]   pictures of frames where the two disagree,
                             current detection red, tracker green

A recording is the camera's own picture, 640 x 480, as PoolWind writes it
with 'recordRawVideo': True ('developerMode': True). "Wrong place" counts
frames more than a tenth of the pool from PoolWind's own detection on the
unpainted frame: on a pool where PoolWind works, that's the swimmer. On a
recording where PoolWind itself goes wrong there is no such reference:
look at the --sheet pictures to see which of the two is right.
"""
import argparse
import ast
import importlib.util
import os
import sys
import types

sys.dont_write_bytecode = True
import cv2
import numpy as np

from tracker import SwimmerTracker, W, H

HERE = os.path.dirname(os.path.abspath(__file__))


def load_program(path):
    spec = importlib.util.spec_from_file_location("poolwind", path)
    pw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pw)
    return pw


def current_detection(pw):
    """PoolWind's own F_mask and get_auto_CoM, outside the program."""
    win = pw.QtMainWindow

    class Current:
        DROPOUT_HOLD_FRAMES = win.DROPOUT_HOLD_FRAMES
        F_mask = win.F_mask
        get_auto_CoM = win.get_auto_CoM
        _dropout_hold = win._dropout_hold

        def __init__(self):
            self.app = types.SimpleNamespace(REPdefaults={"Sensitivity": 5000},
                                             CoM_size_h=1000.0, CoM_size_w=750.0)

        def update(self, picture):
            w, h, _ = self.get_auto_CoM(self.F_mask(picture))
            return None if w is None else (w, h)

    return Current


def corners_from_calibration(program):
    path = os.path.splitext(program)[0] + "_calibration.txt"
    text = open(path).read()
    return ast.literal_eval(text[text.index("{"):])["swimAreaPoints"]


def pictures(path, corners, start, seconds, step):
    """The recording's frames as PoolWind sees them: resized to 640 x 480,
    turned upright, straightened with the swim area's corners to 480 x 640
    (MyVideoCapture.getImages)."""
    M = cv2.getPerspectiveTransform(np.float32(corners), np.float32([[0, 0], [W, 0], [W, H], [0, H]]))
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    for i in range(int(seconds * fps)):
        ok, frame = cap.read()
        if not ok:
            break
        if i % step == 0:
            frame = cv2.rotate(cv2.resize(frame, (640, 480)), cv2.ROTATE_90_CLOCKWISE)
            yield cv2.warpPerspective(frame, M, (W, H))
    cap.release()


# ---- painted distractors: t counts camera frames (30 a second) ----
rng = np.random.default_rng(1)
LEAVES = [(rng.uniform(140, 340), rng.uniform(0, H), rng.uniform(5, 9), rng.uniform(0, 180),
           tuple(int(c) for c in rng.choice([(30, 70, 110), (40, 110, 120), (20, 50, 80)]))) for _ in range(25)]
CLUMPS = [(rng.uniform(150, 330), rng.uniform(0, H), rng.uniform(25, 45)) for _ in range(10)]


def shadow(img, t):
    """A still, swimmer-sized dark patch in the swim zone, from 3 s on."""
    if t < 90:
        return img
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (W // 2 + 20, int(H * 0.30)), (55, 95), 10, 0, 360, 1, -1)
    m = cv2.GaussianBlur(m, (31, 31), 0)
    return (img * (1 - 0.55 * m[..., None])).astype(np.uint8)


def glare(img, t):
    """Two bright patches, in new places every 6 frames."""
    out, r = img.copy(), np.random.default_rng(t // 6)
    for _ in range(2):
        x, y = int(r.integers(80, W - 80)), int(r.integers(80, H - 80))
        cv2.ellipse(out, (x, y), (int(r.integers(40, 70)), int(r.integers(30, 60))), 0, 0, 360, (250, 250, 250), -1)
    return out


def dapple(img, t):
    """Light through trees: a soft bright and dark pattern drifting across."""
    g = cv2.resize(np.random.default_rng(7).random((9, 7)).astype(np.float32), (W + 200, H + 200),
                   interpolation=cv2.INTER_CUBIC)
    o = int(t * 1.5) % 200
    return np.clip(img * (0.45 + 0.9 * g[o:o + H, o:o + W][..., None]), 0, 255).astype(np.uint8)


def leaves(img, t):
    """25 single leaves, about 4 x 2 inches, drifting back with the current."""
    out = img.copy()
    for x, y, r, ang, col in LEAVES:
        cv2.ellipse(out, (int(x + 6 * np.sin(t / 20 + y)), int((y + 2.0 * t) % (H + 40) - 20)),
                    (int(r * 1.8), int(r)), ang + t, 0, 360, col, -1)
    return out


def clumps(img, t):
    """Swimmer-sized clumps (leaves, a toy) drifting back with the current."""
    out = img.copy()
    for i, (x, y, r) in enumerate(CLUMPS):
        cv2.ellipse(out, (int(x), int((y + 2.0 * t) % (H + 100) - 50)), (int(r * 1.6), int(r)),
                    30 * i, 0, 360, (30, 70, 110), -1)
    return out


PAINT = {"clean": None, "shadow": shadow, "glare": glare, "dapple": dapple, "leaves": leaves, "clumps": clumps}


def line(img, com, colour):
    if com is not None:
        y = int(H - com[1] * H / 1000.0)
        cv2.line(img, (0, y), (W - 1, y), colour, 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("recordings", nargs="+")
    ap.add_argument("--program", default=os.path.join(HERE, "..", "..", "software", "poolwind.py"))
    ap.add_argument("--corners")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--seconds", type=float, default=60)
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--paint", default="clean")
    ap.add_argument("--sheet")
    a = ap.parse_args()

    program = os.path.abspath(a.program)
    Current = current_detection(load_program(program))
    corners = ([tuple(int(v) for v in p.split(",")) for p in a.corners.split()] if a.corners
               else corners_from_calibration(program))
    paints = [p.strip() for p in a.paint.split(",")]
    totals, disagree = {}, []

    for rec in a.recordings:
        clean = list(pictures(rec, corners, a.start, a.seconds, a.step))
        if not clean:
            print(f"{rec}: no frames read")
            continue
        ref_det = Current()
        reference = [ref_det.update(p) for p in clean]
        for paint in paints:
            fx = PAINT[paint]
            imgs = clean if fx is None else [fx(p, i * a.step) for i, p in enumerate(clean)]
            cur, trk = Current(), SwimmerTracker()
            for i, (img, ref) in enumerate(zip(imgs, reference)):
                c = cur.update(img)
                t = trk.update(img)[0]
                for label, out in (("current", c), ("tracker", t)):
                    n = totals.setdefault((paint, label), [0, 0, 0, 0])
                    n[0] += 1
                    if ref is None:
                        n[3] += out is not None
                    elif out is None:
                        n[2] += 1
                    elif abs(out[1] - ref[1]) > 100:
                        n[1] += 1
                if a.sheet and ((c is None) != (t is None) or (c and t and abs(c[1] - t[1]) > 100)):
                    disagree.append((img, c, t, f"{os.path.basename(rec)} {paint} "
                                                f"{a.start + i * a.step / 30:.1f}s"))
        print(f"{os.path.basename(rec)}: {len(clean)} frames", flush=True)

    print(f"\n{'painted':8s} {'method':8s} {'frames':>7s} {'wrong place':>12s} {'not found':>10s} {'phantom':>8s}")
    for (paint, label), (n, bad, lost, phantom) in totals.items():
        print(f"{paint:8s} {label:8s} {n:7d} {100*bad/n:11.1f}% {100*lost/n:9.1f}% {100*phantom/n:7.1f}%")
    print("(phantom: a swimmer reported where PoolWind's own detection found none on the unpainted frame)")

    if a.sheet:
        if not disagree:
            print("No frames where the two disagree.")
            return
        picks = [disagree[i] for i in np.linspace(0, len(disagree) - 1, min(12, len(disagree))).astype(int)]
        tiles = []
        for img, c, t, label in picks:
            im = img.copy()
            line(im, c, (0, 0, 255))
            line(im, t, (0, 255, 0))
            cv2.putText(im, label, (6, 24), 0, 0.6, (0, 255, 255), 2)
            tiles.append(cv2.resize(im, (240, 320)))
        while len(tiles) % 4:
            tiles.append(np.zeros_like(tiles[0]))
        cv2.imwrite(a.sheet, np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]))
        print(f"{len(disagree)} frames disagree; {len(picks)} of them in {a.sheet}")


if __name__ == "__main__":
    main()
