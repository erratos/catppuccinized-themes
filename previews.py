#!/usr/bin/env python3
"""Build the README previews from themes/ and wallpapers/ (run ./build.sh first).

    python3 previews.py      # -> ksplash/assets, limine/assets, wallpapers/assets

Each preview puts the original next to the recoloured versions. The originals
are read from the installed packages (same sources as build.sh).
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
THEMES = ROOT / "themes"
LNF = [Path("/usr/share/plasma/look-and-feel"), Path.home() / ".local/share/plasma/look-and-feel"]
CACHY_WALLS = Path("/usr/share/wallpapers/cachyos-wallpapers")
CACHY_HELLO = Path("/usr/share/icons/hicolor/scalable/apps/org.cachyos.hello.svg")
BASE, TEXT, SUB = (30, 30, 46), (205, 214, 244), (166, 173, 200)
TILE = (320, 180)
GAP, LABEL = 6, 26


def font(size, bold=False):
    try:
        name = "DejaVu Sans:bold" if bold else "DejaVu Sans"
        path = subprocess.run(["fc-match", "-f", "%{file}", name],
                              capture_output=True, text=True).stdout
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default(size)


def fit(im, size=TILE):
    """Letterbox an image into a tile on the Mocha base colour."""
    im = im.convert("RGBA")
    im.thumbnail(size, Image.LANCZOS)
    tile = Image.new("RGBA", size, BASE + (255,))
    tile.alpha_composite(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return tile.convert("RGB")


def frame(path, n=None):
    """A representative frame of an image (middle of an animation)."""
    im = Image.open(path)
    frames = getattr(im, "n_frames", 1)
    if frames > 1:
        im.seek(n if n is not None else frames // 2)
    return im.convert("RGBA")


def strip(tiles, out, size=TILE):
    """[(label, image)] side by side, labels above (shrunk to fit their tile)."""
    w = len(tiles) * (size[0] + GAP) + GAP
    sheet = Image.new("RGB", (w, LABEL + size[1] + GAP), BASE)
    d = ImageDraw.Draw(sheet)
    f = font(13, bold=True)
    for i, (label, im) in enumerate(tiles):
        x = GAP + i * (size[0] + GAP)
        lf = f
        for sz in (13, 12, 11, 10):
            lf = font(sz, bold=True)
            if d.textlength(label, font=lf) <= size[0] - 4:
                break
        d.text((x + 2, 6), label, font=lf, fill=SUB if label == "original" else TEXT)
        sheet.paste(fit(im, size), (x, LABEL))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)
    print(out.relative_to(ROOT), sheet.size, f"{out.stat().st_size // 1024} KB")


def source_pkg(pid):
    for d in LNF:
        if (d / pid).is_dir():
            return d / pid
    raise SystemExit(f"source splash '{pid}' is not installed")


# ------------------------------------------------------------------ ksplash
KSPLASH = [  # (source id, image inside the package, output slug, accents)
    ("org.kde.breeze.desktop", "contents/previews/splash.png", "breeze", ["mauve"]),
    ("CachyOS-Nord", "contents/previews/splash.png", "cachyos-nord", ["mauve"]),
    ("a2n.kuro", "contents/previews/splash.png", "kuro", ["mauve"]),
    ("MatrixKDEGlow", "contents/splash/images/splash.webp",
     "matrix-code-welcome-to-kde-glowing", ["green", "lavender"]),
    ("Weaving-Helix-Ring-Dark", "contents/splash/images/Helix-Ring-Dark.gif",
     "weaving-helix-ring-dark", ["mauve", "lavender"]),
]


def ksplash():
    for pid, rel, slug, accents in KSPLASH:
        tiles = [("original", frame(source_pkg(pid) / rel))]
        for acc in accents:
            tiles.append((acc, frame(THEMES / f"ksplash/catppuccin-mocha-{slug}-{acc}" / rel)))
        strip(tiles, ROOT / f"ksplash/assets/{slug}.png")


# ------------------------------------------------------------------- limine
def limine():
    wall = THEMES / "limine/limine-catppuccin-mocha-mauve/wallpaper-mocha-mauve.png"
    strip([("original", frame(CACHY_WALLS / "limine-splash.png")),
           ("Mocha", frame(wall))], ROOT / "limine/assets/wallpaper.png", (480, 270))
    # the menu colours of each accent, as swatches
    rows = []
    for acc in ("mauve", "lavender"):
        c = (THEMES / f"limine/limine-catppuccin-mocha-{acc}/limine-theme.conf").read_text()
        kv = dict(l.split(": ", 1) for l in c.splitlines() if ": " in l and not l.startswith("#"))
        rows.append((acc, kv))
    sw, pad = 34, 8
    keys = ["backdrop", "term_foreground", "interface_help_colour", "interface_branding_colour"]
    names = ["background", "text", "help", "branding (accent)"]
    pal = rows[0][1]["term_palette"].split(";")
    w = 980
    sheet = Image.new("RGB", (w, LABEL + len(rows) * (sw + pad) + pad + 40), BASE)
    d = ImageDraw.Draw(sheet)
    f, fs = font(13, bold=True), font(11)
    for j, (acc, kv) in enumerate(rows):
        y = LABEL + j * (sw + pad)
        d.text((pad, y + 10), acc, font=f, fill=TEXT)
        x = 100
        for k, label in zip(keys, names):
            hexv = kv[k][-6:]
            d.rectangle([x, y, x + sw, y + sw], fill="#" + hexv, outline=SUB)
            if j == 0:
                d.text((x, 6), label, font=fs, fill=SUB)
            x += 170
    y = LABEL + len(rows) * (sw + pad) + pad
    d.text((pad, y + 8), "terminal", font=f, fill=TEXT)
    for i, hexv in enumerate(pal):
        d.rectangle([100 + i * 40, y, 100 + i * 40 + 32, y + 32], fill="#" + hexv)
    out = ROOT / "limine/assets/colours.png"
    sheet.save(out, optimize=True)
    print(out.relative_to(ROOT), sheet.size, f"{out.stat().st_size // 1024} KB")


# --------------------------------------------------------------- wallpapers
def svg_png(path, size=160):
    tmp = ROOT / "themes" / f".{path.stem}.png"
    tmp.parent.mkdir(exist_ok=True)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", str(tmp), str(path)],
                   check=True)
    im = Image.open(tmp).convert("RGBA")
    tmp.unlink()
    return im


def wallpapers():
    w = ROOT / "wallpapers"
    strip([("original", frame(CACHY_WALLS / "Cachy_Topography.jpg")),
           ("Macchiato", frame(w / "Cachy_Topography-catppuccin-macchiato-mauve.png"))],
          w / "assets/cachy-topography.png", (480, 270))
    variants = ["mauve-lavender-mauve", "lavender-mauve-lavender", "blue-sapphire-blue",
                "teal-sky-teal"]
    tiles = [("original", svg_png(CACHY_HELLO))]
    tiles += [(v, svg_png(w / f"org.cachyos.hello-catppuccin-mocha-{v}.svg")) for v in variants]
    strip(tiles, w / "assets/cachyos-hello.png", (200, 186))


if __name__ == "__main__":
    steps = {"ksplash": ksplash, "limine": limine, "wallpapers": wallpapers}
    for name in sys.argv[1:] or steps:
        steps[name]()
