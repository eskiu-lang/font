<p align="center">
  <img src="https://raw.githubusercontent.com/eskiu-lang/eskiu/main/assets/logo.png" alt="Eskiu, a kitten with a ball of yarn" width="140">
</p>

<h2 align="center">font</h2>
<p align="center">TrueType fonts for Eskiu: glyph outlines, antialiased rendering, text layout and atlases.</p>
<p align="center"><sub>Part of the <a href="https://github.com/eskiu-lang">Eskiu</a> project</sub></p>
<p align="center">
  <a href="https://eskiu-lang.org">eskiu-lang.org</a> &nbsp;&middot;&nbsp;
  <a href="#modules">Modules</a> &nbsp;&middot;&nbsp;
  <a href="examples/">Examples</a> &nbsp;&middot;&nbsp;
  <a href="https://github.com/eskiu-lang/eskiu">The language</a>
</p>

<p align="center">
  <a href="https://github.com/eskiu-lang/font/actions/workflows/ci.yml"><img src="https://github.com/eskiu-lang/font/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/version-0.1.0-6448d4" alt="Version 0.1.0">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"></a>
</p>

---

`font` draws text from TrueType fonts in Eskiu programs, with no library to install. It reads
`.ttf` files, turns glyphs into antialiased coverage bitmaps, lays out lines of UTF-8 text with
kerning, and packs a character set into one texture for text on the GPU.

- **TrueType outlines.** Character maps in formats 4 and 12 (the whole of Unicode), simple and
  composite glyphs with their transforms, horizontal metrics and `kern` pairs.
- **Exact coverage.** Each pixel gets the area of the glyph that covers it, the method of
  font-rs, so the total ink of a glyph matches its outline's area. Glyphs can be rendered at a
  subpixel pen position.
- **Text.** Layout with kerning and line breaks, measuring, and drawing into an RGBA image
  with alpha blending.
- **Atlases.** A set of characters at one size packed into an 8-bit texture with each glyph's
  rectangle and metrics, ready to upload with [gpu](https://github.com/eskiu-lang/gpu).

## Drawing text

```eskiu
import <font>;

Result<int, string> run(*uint8 rgba, int width, int height) {
    Font f = font_load("DejaVuSans.ttf")?;
    defer f.free();
    f.draw("Hola, Eskiu", 32.0, rgba, width, height, 10.0, 40.0, 0xFFFFFFFF);

    GlyphBitmap g = f.render(f.glyph('g'), 64.0)?;   // one glyph
    defer g.free();
    // g.pixels: g.width * g.height coverage values, 0 to 255, top row first;
    // g.left and g.top place it from the pen on the baseline.
    return Ok<int, string>(0);
}
```

Sizes are in pixels per em. `draw` takes the first baseline's position and a color as
`0xRRGGBBAA`; `layout` gives each character's pen position instead, and `measure` the size of
the text. For GPU text, `f.atlas(32.0, chars)` renders every character of `chars` once and
`atlas.find(cp)` gives where it is.

[`examples/render.esk`](examples/render.esk) prints a line of text to the terminal or writes it
to a PGM image:

```bash
eskiuc run examples/render.esk -- "Hola, Eskiu" 64 hola.pgm
```

## Install

In an Eskiu package (Eskiu 0.12 or newer):

```bash
eskiuc add font --git https://github.com/eskiu-lang/font --rev v0.1.0
```

## Modules

| Module | What it has |
|---|---|
| `<font>` | the three modules below |
| `<font/ttf>` | `Font`, `font_load`, `font_parse`, `glyph`, `advance`, `left_bearing`, `kerning`, `box`, `outline`, `scale` |
| `<font/raster>` | `GlyphBitmap`, `render`, `render_at`, `font_rasterize` |
| `<font/text>` | `layout`, `measure`, `draw`, `line_height`, `atlas`, `FontAtlas`, `font_utf8_next` |

Fonts with PostScript (CFF) outlines, OpenType shaping (`GPOS`/`GSUB`), hinting and
right-to-left text are not supported.

## Contributing

Bug reports are welcome; please include the program and the `eskiuc --version` output. The
tests run with `eskiuc test`. They compare glyph indices, metrics, boxes, kerning and outline
areas with [fontTools](https://github.com/fonttools/fonttools) (`tools/gen_reference.py`
regenerates `tests/data/reference.txt`), and parse cut and damaged copies of the font.

## License

MIT. See [LICENSE](LICENSE). The test font is a subset of DejaVu Sans, under its own license
([tests/data/DejaVu-LICENSE](tests/data/DejaVu-LICENSE)).
