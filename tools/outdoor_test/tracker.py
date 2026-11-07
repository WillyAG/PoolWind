"""
A swimmer tracker: a prototype, not part of PoolWind.

PoolWind (QtMainWindow.F_mask and get_auto_CoM in poolwind.py) judges each
frame almost on its own. This tracker uses the swimmer's behaviour instead:
it finds the swimmer once, then follows them. It predicts where they'll be,
looks only near there, and checks that the blob still looks and moves like
them (size, colour). It uses the same segmentation as F_mask (each pixel's
HSV distance from the frame's average colour, the same threshold), so the
only difference is how the blob is chosen.

Tested only on painted distractors (see README.md and CLAUDE.md, "Outdoor
pools"). Tune it on real recordings of the pool that gives trouble.
"""
import cv2
import numpy as np

W, H = 480, 640                   # PoolWind's straightened picture (work_size_w, work_size_h)
SENSITIVITY = 5000                # PoolWind's 'Sensitivity': the smallest swimmer blob, in pixels
THRESH = 110                      # F_mask's threshold (60 + thresholdTune 50)


def segment(perspect):
    """F_mask's first steps: HSV distance from the frame's average colour,
    then the threshold. Returns (mask, hsv)."""
    hsv = cv2.cvtColor(perspect, cv2.COLOR_BGR2HSV)
    mean = hsv.reshape(-1, 3).mean(0).astype(np.int16)
    dist = np.abs(hsv.astype(np.int16) - mean).sum(2)
    _, mask = cv2.threshold(np.clip(dist, 0, 255).astype(np.uint8), THRESH, 255, cv2.THRESH_BINARY)
    return mask, hsv


def find_blobs(mask, hsv, gray, prev_gray, min_area=SENSITIVITY):
    """The blobs big enough to be a swimmer (and not more than 20 % of the
    picture), each with its centre, area, mean colour, box and churn: the
    share of its pixels that changed since the last frame (a swimmer
    stirs the water; a shadow or glare doesn't)."""
    out = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diff = cv2.absdiff(gray, prev_gray) if prev_gray is not None else None
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area or area > 0.2 * W * H:
            continue
        m = np.zeros(mask.shape, np.uint8)
        cv2.drawContours(m, [c], -1, 255, -1)
        M = cv2.moments(c)
        churn = float((diff[m > 0] > 12).mean()) if diff is not None else 0.0
        out.append(dict(centre=(M["m10"] / M["m00"], M["m01"] / M["m00"]), area=area,
                        colour=np.array(cv2.mean(hsv, mask=m)[:3]), churn=churn,
                        mask=m, box=cv2.boundingRect(c)))
    return out


def com_from_mask(m):
    """get_auto_CoM's last step: the blob's thin centre strip (1 % of the
    width) -> (CoM_w, CoM_h) in PoolWind's units (0-750 across, 0-1000
    from the back of the pool to the front)."""
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    half = W * 0.01 / 2
    strip = (xs >= xs.mean() - half) & (xs < xs.mean() + half)
    if strip.sum() >= 50:
        xs, ys = xs[strip], ys[strip]
    return ((W - xs.mean()) * (750.0 / W), (H - ys.mean()) * (1000.0 / H))


class SwimmerTracker:
    """update(picture) -> (CoM or None, the swimmer's mask or None).

    pick-up: the blob nearest the centre line, the same blob ACQUIRE_FRAMES
             running, churning the water (ACQUIRE_CHURN);
    follow:  predict from the last movement, look only in a window around
             the prediction, and take the blob nearest it whose area and
             colour are close to the swimmer's (learned slowly);
    lose:    after LOSE_FRAMES without a match, back to pick-up; the last
             position is reported for HOLD_FRAMES misses, as PoolWind does.
    """
    ACQUIRE_FRAMES = 8
    ACQUIRE_CHURN = 0.10
    GATE_PX = 45              # how far from the prediction a blob may be
    GATE_GROW = 12            # ...more for each missed frame
    MAX_AREA_LOG = 0.9        # area within a factor of e**0.9 (about 2.5) of the swimmer's
    LOSE_FRAMES = 20
    HOLD_FRAMES = 3

    def __init__(self):
        self.state = "pick-up"
        self.prev_gray = None
        self.candidate = None         # pick-up: (centre, area, frames seen)
        self.misses = 0
        self.last = None

    def update(self, perspect):
        gray = cv2.cvtColor(perspect, cv2.COLOR_BGR2GRAY)
        mask, hsv = segment(perspect)
        try:
            if self.state == "follow":
                return self._follow(mask, hsv, gray)
            return self._pick_up(mask, hsv, gray)
        finally:
            self.prev_gray = gray

    def _follow(self, mask, hsv, gray):
        px, py = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        gate = self.GATE_PX + self.GATE_GROW * self.misses
        _, _, bw, bh = self.box
        hw, hh = max(bw, 60) * 0.75 + gate, max(bh, 80) * 0.75 + gate
        window = np.zeros_like(mask)
        window[int(max(0, py - hh)):int(min(H, py + hh)), int(max(0, px - hw)):int(min(W, px + hw))] = 255
        best, best_cost = None, None
        for b in find_blobs(cv2.bitwise_and(mask, window), hsv, gray, self.prev_gray, SENSITIVITY * 0.5):
            d = np.hypot(b["centre"][0] - px, b["centre"][1] - py) / gate
            da = abs(np.log(b["area"] / self.area))
            dc = np.abs(b["colour"] - self.colour).sum() / 120.0
            if d <= 1.0 and da <= self.MAX_AREA_LOG and (best is None or d + da + dc < best_cost):
                best, best_cost = b, d + da + dc
        if best is None:
            self.misses += 1
            self.vel = (self.vel[0] * 0.8, self.vel[1] * 0.8)
            if self.misses > self.LOSE_FRAMES:
                self.state, self.candidate = "pick-up", None
            return (self.last if self.misses <= self.HOLD_FRAMES else None), None
        nx, ny = best["centre"]
        self.vel = (0.6 * self.vel[0] + 0.4 * (nx - self.pos[0]), 0.6 * self.vel[1] + 0.4 * (ny - self.pos[1]))
        self.pos, self.box, self.misses = (nx, ny), best["box"], 0
        self.area = 0.9 * self.area + 0.1 * best["area"]
        self.colour = 0.95 * self.colour + 0.05 * best["colour"]
        self.last = com_from_mask(best["mask"])
        return self.last, best["mask"]

    def _pick_up(self, mask, hsv, gray):
        found = find_blobs(mask, hsv, gray, self.prev_gray)
        if not found:
            self.candidate = None
            return None, None
        if self.candidate is not None:
            (cx, cy), area, n = self.candidate
            near = [b for b in found if np.hypot(b["centre"][0] - cx, b["centre"][1] - cy) < 60
                    and abs(np.log(b["area"] / area)) < 0.7]
            if near:
                b = min(near, key=lambda b: np.hypot(b["centre"][0] - cx, b["centre"][1] - cy))
                n += b["churn"] >= self.ACQUIRE_CHURN
                self.candidate = (b["centre"], b["area"], n)
                if n >= self.ACQUIRE_FRAMES:
                    self.state, self.misses = "follow", 0
                    self.pos, self.vel, self.box = b["centre"], (0.0, 0.0), b["box"]
                    self.area, self.colour = b["area"], b["colour"]
                    self.last = com_from_mask(b["mask"])
                    return self.last, b["mask"]
                return None, None
        b = min(found, key=lambda b: abs(b["centre"][0] - W / 2))
        self.candidate = (b["centre"], b["area"], 0)
        return None, None
