import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

CTRL, FEED, VIS, GRAY = '#d9480f', '#2b8a3e', '#1c7ed6', '#555555'
fig, ax = plt.subplots(figsize=(13, 8.2))
ax.set_xlim(0, 134); ax.set_ylim(-9, 82); ax.axis('off')

def zone(x0, y0, x1, y1, label, fc, ec):
    ax.add_patch(FancyBboxPatch((x0, y0), x1-x0, y1-y0, boxstyle='round,pad=0,rounding_size=2',
                                fc=fc, ec=ec, lw=1.5, ls='--'))
    ax.text(x0+2, y1-2.2, label, fontsize=12, weight='bold', color=ec, va='top')

def box(x0, y0, x1, y1, title, sub=None, ec=GRAY, fc='white'):
    ax.add_patch(FancyBboxPatch((x0, y0), x1-x0, y1-y0, boxstyle='round,pad=0,rounding_size=1.2',
                                fc=fc, ec=ec, lw=2))
    cx, cy = (x0+x1)/2, (y0+y1)/2
    if sub:
        ax.text(cx, cy+1.6, title, ha='center', va='center', fontsize=12.5, weight='bold')
        ax.text(cx, cy-2.0, sub, ha='center', va='center', fontsize=10, color='#333')
    else:
        ax.text(cx, cy, title, ha='center', va='center', fontsize=12.5, weight='bold')

def arrow(p0, p1, color, label=None, lpos=None, ls='-', both=False, lha='center'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='<|-|>' if both else '-|>', color=color, lw=2.4,
                                ls=ls, mutation_scale=18, shrinkA=0, shrinkB=0))
    if label:
        x, y = lpos if lpos else ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2 + 1.6)
        ax.text(x, y, label, ha=lha, va='center', fontsize=10, color=color, style='italic',
                bbox=dict(fc='white', ec='none', pad=0.6))

# zones
zone(4, 4, 58, 80, 'Waterproof case at the poolside', '#f1f5fb', '#5c7cab')
zone(100, 4, 131, 48, "Pool equipment\n(not modified)", '#f3f8f3', '#4f7a4f')

# case contents
box(12, 64, 50, 72, 'Monitor', 'portrait, 10 in')
box(12, 42, 50, 53, 'Raspberry Pi 5', 'runs PoolWind')
ax.add_patch(FancyBboxPatch((8, 8), 46, 26, boxstyle='round,pad=0,rounding_size=1.2', fc='#fffbe6', ec=GRAY, lw=2))
ax.text(31, 31.3, 'Interface board', ha='center', va='center', fontsize=12.5, weight='bold')
box(12, 20, 50, 28, 'Relays', 'Up · Down · On/Off', ec=CTRL)
box(12, 10, 50, 18, 'INA260 voltage sensor', None, ec=FEED)

# outside the case
box(64, 67, 94, 75, 'Keyboard and mouse', 'waterproof')
box(64, 55, 94, 63, "Swimmer's USB stick", 'on a USB extension')
box(64, 40, 94, 50, 'Camera', 'above the swim area', ec=VIS)
box(64, 21, 94, 33, 'Modified remote', 'in a watertight box', ec=CTRL)

# pool equipment
box(103, 28, 127, 38, 'Pool controller', 'and jet pump')
box(103, 10, 127, 19, 'Pace Display port', None)

# connections
arrow((31, 53), (31, 64), GRAY, 'HDMI', (35, 58.5), both=True)
arrow((31, 34), (31, 42), GRAY, 'ribbon cable', (39, 38), both=True)
arrow((64, 71), (50, 51.5), GRAY, 'USB', (58.5, 63.5))
arrow((64, 59), (50, 49.5), GRAY, 'USB', (57, 56))
arrow((64, 45), (50, 45), VIS, 'USB, 10 ft', (57, 46.8))
arrow((50, 25), (64, 25), CTRL, 'network\ncable', (57.5, 29.4))
arrow((94, 29), (103, 33), CTRL, 'radio', (97.5, 34.2), ls=(0, (4, 3)))
arrow((103, 14.5), (50, 14.5), FEED, 'phone cable', (76, 16.6))
ax.text(76, 11.6, '(through a Y splitter if you\nhave a Pace Display)', ha='center', va='center', fontsize=9.5, color=FEED, style='italic')

# legend
ly = -2
for i, (c, t) in enumerate([(CTRL, 'Control: presses the remote’s buttons'),
                            (FEED, 'Feedback: the jet speed, as a voltage'),
                            (VIS, 'Vision: the camera sees the swimmer')]):
    x = [6, 50, 94][i]
    y = ly
    ax.plot([x, x+4], [y, y], color=c, lw=3)
    ax.text(x+5.5, y, t, va='center', fontsize=10.5, color='#222')

plt.savefig(sys.argv[1], dpi=130, bbox_inches='tight', pad_inches=0.15, facecolor='white')
