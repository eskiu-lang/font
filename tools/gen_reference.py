#!/usr/bin/env python3
"""Writes tests/data/reference.txt from tests/data/DejaVuSans-Latin1.ttf with
fontTools (run with python3 -I).

One line per character: code point, glyph index, advance, left side bearing,
bounding box and the outline's exact area (fontTools' AreaPen, in font units
squared); then "kern A B value" lines for every kerning pair of the 'kern'
table between characters of the set.
"""
import os

from fontTools.pens.areaPen import AreaPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "tests", "data")
font = TTFont(os.path.join(DATA, "DejaVuSans-Latin1.ttf"))
cmap = font.getBestCmap()
glyphs = font.getGlyphSet()
order = font.getGlyphOrder()
hmtx = font["hmtx"]
glyf = font["glyf"]
lines = []
for cp in sorted(cmap):
    name = cmap[cp]
    gid = order.index(name)
    adv, lsb = hmtx[name]
    g = glyf[name]
    g.recalcBounds(glyf)
    box = (g.xMin, g.yMin, g.xMax, g.yMax) if hasattr(g, "xMin") and g.numberOfContours != 0 else (0, 0, 0, 0)
    pen = AreaPen(glyphs)
    glyphs[name].draw(pen)
    lines.append("%d %d %d %d %d %d %d %d %.3f" % (cp, gid, adv, lsb, box[0], box[1], box[2], box[3], abs(pen.value)))
kern = font["kern"].kernTables[0].kernTable
names = {cmap[cp]: cp for cp in cmap}
for (a, b), v in sorted(kern.items()):
    if a in names and b in names:
        lines.append("kern %d %d %d" % (names[a], names[b], v))
with open(os.path.join(DATA, "reference.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print(len(lines), "lines")
