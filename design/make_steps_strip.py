#!/usr/bin/env python3
"""Groove Bank FX: the filmstrip for one step cell of the 16-STEP PATTERN bar (33 x 42 px, 10 frames stacked down).
    python3 design/make_steps_strip.py images/steps.png
Frame = state + 5 * playing; state 0 rest, 1 ghost, 2 hit, 3 accent, 4 tie (the note held on from the step before).
Colours and geometry are the Stitch bar's own (cell 33 x 42, bars 4 px in from the sides, bottom at 38)."""
import sys
from PIL import Image, ImageDraw

W, H = 33, 42
BORDER, INNER = (51, 46, 42), (31, 31, 35)
BARS = {1: (9, (99, 82, 54)), 2: (26, (196, 154, 84)), 3: (32, (243, 189, 98))}
TIE = (26, (121, 98, 61))


def lift(c, k):
    return tuple(min(255, int(v * k)) for v in c)


def frame(state, playing):
    im = Image.new("RGB", (W, H), INNER)
    d = ImageDraw.Draw(im)
    if playing:
        d.rectangle((1, 1, W - 2, H - 2), fill=(58, 50, 40))
    d.rectangle((0, 0, W - 1, H - 1), outline=(255, 194, 102) if playing else BORDER, width=2 if playing else 1)
    k = 1.15 if playing else 1.0
    if state in BARS:
        h, c = BARS[state]
        d.rectangle((4, 38 - h, W - 5, 37), fill=lift(c, k))
    elif state == 4:   # tie: a lower band running out of both sides, so it reads as one held note
        h, c = TIE
        d.rectangle((0, 38 - h, W - 1, 37), fill=lift(c, k))
        d.line((0, 38 - h, W - 1, 38 - h), fill=lift((160, 128, 76), k))
    return im


strip = Image.new("RGB", (W, H * 10))
for f in range(10):
    strip.paste(frame(f % 5, f >= 5), (0, H * f))
strip.save(sys.argv[1])
