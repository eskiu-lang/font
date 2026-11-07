# font documentation

Guides and reference for font. The [README](../README.md) has the overview.

<!-- pages -->
- [API reference](api.md): every public function and type
<!-- /pages -->

## Platforms

The package is plain Eskiu with no native library, so it builds for every target Eskiu has:
macOS, Linux and Windows, iOS and Android, WebAssembly, and freestanding builds. Its tests
pass on macOS, Linux and Windows in CI, under node as WebAssembly (emscripten) and on an
Android arm64 emulator.

## Modules

| Module | What it has |
|---|---|
| `<font>` | the three modules below |
| `<font/ttf>` | `Font`, `font_load`, `font_parse`, `glyph`, `advance`, `left_bearing`, `kerning`, `box`, `outline`, `scale` |
| `<font/raster>` | `GlyphBitmap`, `render`, `render_at`, `font_rasterize` |
| `<font/text>` | `layout`, `measure`, `draw`, `line_height`, `atlas`, `FontAtlas`, `font_utf8_next` |

Fonts with PostScript (CFF) outlines, OpenType shaping (`GPOS`/`GSUB`), hinting and
right-to-left text are not supported.

Every public function and type, with its documentation, is in the [API reference](api.md).

## Contributing

Bug reports are welcome; please include the program and the `eskiuc --version` output. The
tests run with `eskiuc test`. They compare glyph indices, metrics, boxes, kerning and outline
areas with [fontTools](https://github.com/fonttools/fonttools) (`tools/gen_reference.py`
regenerates `tests/data/reference.txt`), and parse cut and damaged copies of the font.
