#!/usr/bin/env python3
"""Groove Bank FX: clear the parts of the Stitch background that the FX layout puts live controls on.
    python3 design/fx_bg_edit.py images/stitch/bg_0.png
- top-left display: the 'SLOT // PRESET BANK' caption and the 'SOURCE / CLOCK / QUANTIZE' footer go (scanlines are
  copied from an empty band, period 2 px), so GENRE and GROOVE fit as two steppers;
- right panel: the 'SYNC MULTIPLIER' box is emptied for the MIDI IN CH stepper.
Run once on the original artwork (it is idempotent: running it again changes nothing)."""
import sys
from PIL import Image

path = sys.argv[1]
im = Image.open(path).convert("RGB")
band = im.crop((26, 140, 622, 160))          # 20 empty display rows
for y0 in (112, 132, 184):                     # even offsets keep the scanline phase
    im.paste(band, (26, y0))
im.paste((13, 14, 17), (976, 524, 1255, 563))  # SYNC MULTIPLIER box interior
im.save(path)

# v2 (chord source): the right-top panel's mock monitor (CHORD DETECT, NOTE/VEL, DYNAMICS, four small boxes) goes; each
# row is refilled from an empty strip just inside the panel's left edge (period 2 px), keeping the panel's gradient.
im = Image.open(path).convert("RGB")
for y in range(96, 307):
    a, b = im.getpixel((648, y)), im.getpixel((649, y))
    for x in range(648, 1261):
        im.putpixel((x, y), a if (x - 648) % 2 == 0 else b)
im.save(path)

# v3 (live step display): the mock data goes (STEP TICKS, IN/OUT ACTIVE, SERIAL, FIRMWARE line, STEP: 01 / 16 -- the
# last becomes a live readout); the bar's caption becomes "16-STEP PATTERN", built from the caption's own monospace
# glyphs (pitch 5.72 px from x 22.5); the 16 cells get live filmstrips (layout.conf meters), not drawn here.
im = Image.open(path).convert("RGB")


def clear_rows(x0, y0, x1, y1, lx=None, rx=None):
    """refill x0..x1 x y0..y1 row by row, blending from the two pixels left of the box to the two right of it (keeps
    the 2 px pattern and both gradients, so no edge shows)"""
    for y in range(y0, y1 + 1):
        lx_ = x0 - 2 if lx is None else lx   # sample columns: next to the box, or given (text right beside it)
        rx_ = x1 + 1 if rx is None else rx
        la, lb = im.getpixel((lx_, y)), im.getpixel((lx_ + 1, y))
        ra, rb = im.getpixel((rx_, y)), im.getpixel((rx_ + 1, y))
        if abs(sum(ra) - sum(la)) > 24 or abs(sum(rb) - sum(lb)) > 24:   # a panel screw or border there: no blend
            ra, rb = la, lb
        for x in range(x0, x1 + 1):
            t = (x - x0 + 1) / (x1 - x0 + 2)
            l, r = (la, ra) if (x - x0) % 2 == 0 else (lb, rb)
            im.putpixel((x, y), tuple(int(round(l[i] + (r[i] - l[i]) * t)) for i in range(3)))


P, X0, Y0, Y1 = 5.72, 22.5, 229, 244
cells = {k: im.crop((int(round(X0 + P * k)), Y0, int(round(X0 + P * (k + 1))), Y1)) for k in (4, 5, 6, 11, 17, 24)}
clear_rows(int(X0 + P * 7), Y0, 222, Y1, lx=300, rx=300)                   # " MICROTIMING DEVIATION (MS)"
for i, k in enumerate((6, 24, 4, 4, 5, 11, 17)):                 # P A T T E R N after "16-STEP "
    im.paste(cells[k], (int(round(X0 + P * (8 + i))), Y0))
clear_rows(548, 230, 625, 243)                              # STEP: 01 / 16
clear_rows(500, 69, 620, 80)                                # STEP TICKS: 960 PPQN
clear_rows(1110, 68, 1253, 79)                             # IN/OUT: 0.2 ms  ACTIVE
clear_rows(1172, 331, 1253, 340)                           # SERIAL: #0928
for y in range(472, 485):                                        # FIRMWARE 3.2.1 / 1280 x 628 TOUCH (scanlines)
    c = im.getpixel((980, y))
    for x in range(980, 1250):
        im.putpixel((x, y), c)
im.save(path)
