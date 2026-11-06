#!/usr/bin/env python3
# Petunia - Draw the home-screen pictures: the background and the launch picture.
# Copyright (C) 2026 Oliv3rmoon
# SPDX-License-Identifier: GPL-3.0-or-later
"""Draw Petunia's home-screen pictures in Nightshade's style, in Petunia's chartreuse.

usage: python3 tools/render-home-art.py              (needs Pillow and NumPy)
       python3 tools/render-home-art.py --preview DIR  (small copies in DIR; the repository is left alone)

Datura's tools/render-home-art.py (after Physalis's and Nightshade's, Oliv3rmoon/Nightshade), with
Petunia's logo in place of the drawn flower: near black with a low chartreuse glow, faint stars and
dark leaves lit chartreuse along one edge, and Nightshade's palette with chartreuse where it has its
red. The petunia is the logo itself (assets/branding/petunia-logo-1024.png), cut out of its black
ground, with its sound going out of the bell's mouth in wide arcs of light, as its own arcs do.

Writes, in sce_sys/ (icon0.png is never drawn here: it is Petunia's logo, resized from
assets/branding/petunia-logo-1024.png):
  background-source.png         3840x2160: the petunia at the right, its sound going out to the
                                upper right, leaves along the edges
  launch-background-source.png  3840x2160: the petunia in the middle, in a ring of chartreuse light
  pic0.dds, pic1.dds            those two as BC7 (the format, size and header the console's
                                pictures were in, tools/validate-assets.sh), opaque, as
                                ProsperoRadio's were
Everything else is procedural; the same logo and seed give the same files.
"""
import math
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
targets = [root / 'sce_sys']
LOGO = root / 'assets/branding/petunia-logo-1024.png'

# Nightshade's base, with Petunia's chartreuse for its red: accent_deep, accent, accent_pale; the
# leaves' near black.
BASE = (0x09, 0x09, 0x0b)
DEEP = (0x2a, 0x3a, 0x08)
ACCENT = (0xae, 0xea, 0x00)
PALE = (0xe4, 0xf5, 0xc0)
LEAF = (0x0c, 0x0f, 0x06)
# The logo's own ground, which the cut-out takes away.
LOGO_GROUND = (0x0b, 0x0b, 0x0d)
# Where the bell's mouth is in the logo (fractions of its side): the centre its own three sound
# arcs are drawn round (fitted to them).
MOUTH = (0.69, 0.32)


def rgb(color):
    return np.array(color, np.float32) / 255.0


def canvas(width, height):
    image = np.empty((height, width, 3), np.float32)
    image[:] = rgb(BASE)
    return image


def glow(image, cx, cy, radius, color, strength, ring=None, width=None):
    """Adds a soft round light; with ring, a ring of light of that radius instead."""
    height, width_px = image.shape[:2]
    y, x = np.ogrid[:height, :width_px]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2, dtype=np.float32)
    if ring is None:
        falloff = np.exp(-(d / radius) ** 2)
    else:
        falloff = np.exp(-((d - ring) / width) ** 2)
    image += falloff[..., None] * rgb(color) * strength


def vignette(image, amount):
    height, width = image.shape[:2]
    y, x = np.ogrid[:height, :width]
    d = np.sqrt(((x - width / 2) / (width / 2)) ** 2 + ((y - height / 2) / (height / 2)) ** 2)
    image *= (1.0 - amount * np.clip(d - 0.55, 0, None) ** 1.5)[..., None]


def stars(image, count, seed, avoid=None):
    rng = np.random.default_rng(seed)
    height, width = image.shape[:2]
    for _ in range(count):
        x, y = rng.uniform(0, width), rng.uniform(0, height * 0.8)
        if avoid and math.hypot(x - avoid[0], y - avoid[1]) < avoid[2]:
            continue
        size = rng.uniform(0.6, 1.6) * width / 3840
        light = rng.uniform(0.15, 0.6) ** 2
        tint = PALE if rng.random() < 0.3 else (0xf6, 0xff, 0xf0)
        r = int(size * 4) + 2
        x0, y0 = int(x) - r, int(y) - r
        if x0 < 0 or y0 < 0 or x0 + 2 * r >= width or y0 + 2 * r >= height:
            continue
        yy, xx = np.mgrid[y0:y0 + 2 * r, x0:x0 + 2 * r]
        dot = np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (size * size)))
        image[y0:y0 + 2 * r, x0:x0 + 2 * r] += dot[..., None].astype(np.float32) * rgb(tint) * light


def leaf_points(cx, cy, length, wide, angle, steps=64, bend=0.0):
    """A pointed leaf or petal from (cx, cy) along angle (radians): its outline."""
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        w = wide * (math.sin(math.pi * t) ** 0.85) * (1 - t) ** 0.25
        off = bend * length * t * t
        left.append((t * length, w + off))
        right.append((t * length, -w + off))
    outline = left + right[::-1]
    c, s = math.cos(angle), math.sin(angle)
    return [(cx + px * c - py * s, cy + px * s + py * c) for px, py in outline]


def shape_mask(points, box, scale=4):
    """The anti-aliased coverage of a polygon inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    big = Image.new('L', (w * scale, h * scale), 0)
    ImageDraw.Draw(big).polygon([((px - x0) * scale, (py - y0) * scale) for px, py in points], fill=255)
    return np.asarray(big.resize((w, h), Image.LANCZOS), np.float32) / 255.0


def stroke_mask(points, thickness, box, scale=4):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    big = Image.new('L', (w * scale, h * scale), 0)
    ImageDraw.Draw(big).line([((px - x0) * scale, (py - y0) * scale) for px, py in points], fill=255,
                             width=max(1, int(thickness * scale)), joint='curve')
    return np.asarray(big.resize((w, h), Image.LANCZOS), np.float32) / 255.0


def bounds(image, points, pad=4):
    height, width = image.shape[:2]
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return (max(0, int(min(xs)) - pad), max(0, int(min(ys)) - pad),
            min(width, int(max(xs)) + pad), min(height, int(max(ys)) + pad))


def put(image, box, mask, color):
    """Covers box with color (an RGB triple or an array the size of box) by mask."""
    x0, y0, x1, y1 = box
    region = image[y0:y1, x0:x1]
    fill = color if isinstance(color, np.ndarray) and color.ndim == 3 else rgb(color)
    region[:] = region * (1 - mask[..., None]) + fill * mask[..., None]


def leaf(image, cx, cy, length, wide, angle, bend=0.0, rim=0.35):
    points = leaf_points(cx, cy, length, wide, angle, bend=bend)
    box = bounds(image, points, pad=int(length * 0.05) + 4)
    mask = shape_mask(points, box)
    # Chartreuse light along one edge: the leaf less a copy shifted away from the light.
    shift = max(2, int(length * 0.012))
    moved = np.zeros_like(mask)
    moved[shift:, shift:] = mask[:-shift, :-shift]
    edge = np.clip(mask - moved, 0, 1)
    put(image, box, mask, LEAF)
    image[box[1]:box[3], box[0]:box[2]] += edge[..., None] * rgb(ACCENT) * rim
    rib = [(cx + math.cos(angle) * length * t, cy + math.sin(angle) * length * t + bend * length * t * t * math.cos(angle))
           for t in np.linspace(0.02, 0.85, 24)]
    put(image, box, stroke_mask(rib, max(1.0, length * 0.006), box) * 0.5, DEEP)


def stem(image, points, thickness):
    box = bounds(image, points, pad=int(thickness) + 4)
    put(image, box, stroke_mask(points, thickness, box), (0x14, 0x1c, 0x06))


def curve(a, b, c, steps=40):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * b[0] + t * t * c[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * b[1] + t * t * c[1]) for t in np.linspace(0, 1, steps)]



def sound_arcs(image, cx, cy, radii, toward, sweep, width, strength):
    """The sound: arcs of chartreuse light round (cx, cy), each centred on the direction `toward`
    (radians, 0 up, clockwise) and `sweep` wide, each fainter than the one inside it. Soft ends, a
    bright core and a glow, as Nightshade's ring of light."""
    height, width_px = image.shape[:2]
    reach = max(radii) + width * 6
    x0, y0 = max(0, int(cx - reach)), max(0, int(cy - reach))
    x1, y1 = min(width_px, int(cx + reach) + 1), min(height, int(cy + reach) + 1)
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d = np.hypot(xx - cx, yy - cy)
    a = np.arctan2(xx - cx, -(yy - cy))  # 0 up, clockwise
    off = np.abs((a - toward + math.pi) % (2 * math.pi) - math.pi)
    region = image[y0:y1, x0:x1]
    for k, r in enumerate(radii):
        half = sweep * (1 - 0.13 * k) / 2
        ends = np.clip((half - off) / (half * 0.35), 0, 1) ** 1.5
        light = (np.exp(-((d - r) / width) ** 2) * 0.9 + np.exp(-((d - r) / (width * 4)) ** 2) * 0.25) * ends
        region += light[..., None] * rgb(ACCENT) * strength * (1 - 0.27 * k)


def eclipse(image, cx, cy, radius, strength=1.0, crescent=None):
    """Nightshade's eclipse: a dark disc in a ring of light, chartreuse here. With crescent (a
    direction, as sound_arcs takes it), the ring is a crescent, bright on that side and gone on the
    other."""
    height, width = image.shape[:2]
    y, x = np.ogrid[:height, :width]
    d = np.hypot(x - cx, y - cy).astype(np.float32)
    side = 1.0
    if crescent is not None:
        a = np.arctan2(x - cx, -(y - cy))
        side = (0.5 + 0.5 * np.cos(a - crescent)).astype(np.float32) ** 2.2
    ring = np.exp(-((d - radius) / (radius * 0.06)) ** 2) * 0.75 + np.exp(-((d - radius) / (radius * 0.27)) ** 2) * 0.25
    image += (ring * side)[..., None] * rgb(ACCENT) * strength
    disc = np.clip((radius - d) / 3, 0, 1)[..., None]
    image[:] = image * (1 - disc * 0.92) + rgb(BASE) * disc * 0.92



def mark(image, cx, cy, size):
    """Petunia's logo, `size` pixels square, centred on (cx, cy), cut out of its black ground: how
    far each pixel is from that ground is how much of the logo it is, so the glows show round it."""
    logo = Image.open(LOGO).convert('RGB').resize((int(size), int(size)), Image.LANCZOS)
    pixels = np.asarray(logo, np.float32) / 255.0
    ground = rgb(LOGO_GROUND)
    alpha = np.clip((np.abs(pixels - ground).max(2) * 255.0 - 6.0) / 34.0, 0, 1)[..., None]
    x0, y0 = int(cx - size / 2), int(cy - size / 2)
    region = image[y0:y0 + pixels.shape[0], x0:x0 + pixels.shape[1]]
    # The logo over the picture: its own colours where it is, the picture where its ground was.
    region[:] = pixels + (region - ground) * (1 - alpha)
    return x0 + MOUTH[0] * size, y0 + MOUTH[1] * size


def background(w=3840, h=2160):
    image = canvas(w, h)
    # The glows are lower than Nightshade's red ones: green looks brighter at the same strength.
    glow(image, w * 0.72, h * 0.47, w * 0.3, DEEP, 0.62)
    glow(image, w * 0.05, h * 1.05, w * 0.3, DEEP, 0.35)
    stars(image, 900, 1011, avoid=(w * 0.72, h * 0.47, w * 0.2))
    for x, y, length, angle, bend in ((w * 1.03, h * 0.0, w * 0.22, 2.45, 0.10), (w * 1.03, h * 0.66, w * 0.2, 3.35, -0.12),
                                      (w * 0.94, h * 1.06, w * 0.22, 3.9, 0.08), (w * 0.6, h * 1.08, w * 0.17, 4.5, -0.1),
                                      (-w * 0.02, h * 1.04, w * 0.2, 5.6, 0.1)):
        leaf(image, x, y, length, length * 0.24, angle, bend=bend)
    # The petunia at the right, its sound going out of the bell to the upper right, beyond its
    # own three arcs: wide and faint, into the room the title takes.
    size = h * 0.62
    mx, my = w * 0.72, h * 0.5
    glow(image, mx + size * 0.1, my - size * 0.1, size * 0.32, ACCENT, 0.10)
    ax, ay = mx - size / 2 + MOUTH[0] * size, my - size / 2 + MOUTH[1] * size
    sound_arcs(image, ax, ay, (size * 0.3, size * 0.4, size * 0.5), 0.7854, 1.1, h * 0.0042, 0.55)
    mark(image, mx, my, size)
    vignette(image, 0.55)
    return image


def launch(w=3840, h=2160):
    image = canvas(w, h)
    cx, cy = w * 0.5, h * 0.5
    glow(image, cx, cy, h * 0.55, DEEP, 0.55)
    stars(image, 1100, 1012, avoid=(cx, cy, h * 0.46))
    # Nightshade's eclipse round the petunia, and its sound going out to the upper right.
    eclipse(image, cx, cy, h * 0.33, 0.8)
    for x, y, length, angle, bend in ((-w * 0.02, h * 0.02, w * 0.26, 0.55, 0.08), (-w * 0.03, h * 0.7, w * 0.23, -0.2, -0.1),
                                      (w * 0.1, h * 1.08, w * 0.2, -1.0, 0.1), (w * 1.02, h * 0.04, w * 0.26, 2.6, -0.08),
                                      (w * 1.03, h * 0.72, w * 0.23, 3.35, 0.1), (w * 0.9, h * 1.08, w * 0.2, 4.15, -0.1)):
        leaf(image, x, y, length, length * 0.24, angle, bend=bend)
    size = h * 0.52
    ax, ay = cx - size / 2 + MOUTH[0] * size, cy - size / 2 + MOUTH[1] * size
    sound_arcs(image, ax, ay, (h * 0.25, h * 0.3, h * 0.35), 0.7854, 0.95, h * 0.0045, 0.75)
    mark(image, cx, cy, size)
    vignette(image, 0.6)
    return image


def to_image(image, mode='RGB'):
    # A little noise keeps the dark glows from showing steps (the same noise every time).
    noise = np.random.default_rng(7).uniform(-0.75, 0.75, image.shape[:2])[..., None]
    data = np.clip(np.clip(image, 0, 1) * 255 + 0.5 + noise, 0, 255).astype(np.uint8)
    picture = Image.fromarray(data)
    return picture.convert(mode)


def bc7(picture):
    """BC7 blocks of an RGBA picture, every block in mode 6 (one pair of endpoints, 16 steps)."""
    pixels = np.asarray(picture.convert('RGBA'), np.float32)
    h, w = pixels.shape[:2]
    blocks = pixels.reshape(h // 4, 4, w // 4, 4, 4).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 4)
    weights = np.array([0, 4, 9, 13, 17, 21, 26, 30, 34, 38, 43, 47, 51, 55, 60, 64], np.int32)
    out = np.empty((blocks.shape[0], 16), np.uint8)
    for start in range(0, blocks.shape[0], 32768):
        b = blocks[start:start + 32768]
        mean = b.mean(1, keepdims=True)
        centred = b - mean
        cov = np.einsum('npi,npj->nij', centred, centred)
        axis = np.ones((b.shape[0], 4), np.float32)
        for _ in range(8):
            axis = np.einsum('nij,nj->ni', cov, axis)
            axis /= np.maximum(np.linalg.norm(axis, axis=1, keepdims=True), 1e-9)
        proj = np.einsum('npi,ni->np', centred, axis)
        e0 = np.clip(mean[:, 0] + proj.min(1, keepdims=True) * axis, 0, 255)
        e1 = np.clip(mean[:, 0] + proj.max(1, keepdims=True) * axis, 0, 255)
        # 7 bits and a p-bit of 1 per endpoint: an endpoint is 2q + 1, so opaque stays 255.
        q0 = np.clip(np.round((e0 - 1) / 2), 0, 127).astype(np.int32)
        q1 = np.clip(np.round((e1 - 1) / 2), 0, 127).astype(np.int32)
        v0, v1 = q0 * 2 + 1, q1 * 2 + 1
        palette = ((64 - weights)[None, :, None] * v0[:, None, :] + weights[None, :, None] * v1[:, None, :] + 32) >> 6
        dist = ((b[:, :, None, :] - palette[:, None, :, :].astype(np.float32)) ** 2).sum(-1)
        index = dist.argmin(-1).astype(np.int32)
        # The first pixel's index has 3 bits: when it would need 4, the endpoints change places.
        flip = index[:, 0] >= 8
        q0[flip], q1[flip] = q1[flip].copy(), q0[flip].copy()
        index[flip] = 15 - index[flip]
        lo = np.zeros(b.shape[0], np.uint64)
        hi = np.zeros(b.shape[0], np.uint64)
        position = 0

        def field(value, bits):
            nonlocal position
            value = value.astype(np.uint64) & np.uint64((1 << bits) - 1)
            if position >= 64:
                hi[:] |= value << np.uint64(position - 64)
            elif position + bits <= 64:
                lo[:] |= value << np.uint64(position)
            else:
                low = 64 - position
                lo[:] |= (value & np.uint64((1 << low) - 1)) << np.uint64(position)
                hi[:] |= value >> np.uint64(low)
            position += bits

        field(np.full(b.shape[0], 1 << 6), 7)
        for channel in range(4):
            field(q0[:, channel], 7)
            field(q1[:, channel], 7)
        field(np.ones(b.shape[0]), 1)
        field(np.ones(b.shape[0]), 1)
        field(index[:, 0], 3)
        for pixel in range(1, 16):
            field(index[:, pixel], 4)
        assert position == 128
        out[start:start + 32768, :8] = lo.view(np.uint8).reshape(-1, 8)
        out[start:start + 32768, 8:] = hi.view(np.uint8).reshape(-1, 8)
    return out.tobytes()


def dds(picture, alpha_mode):
    """A DDS file with a DX10 header: BC7_UNORM, one level, as the console's pictures were."""
    w, h = picture.size
    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x20000 | 0x80000  # caps, size, format, levels, linear size
    header = struct.pack('<4s7I44x', b'DDS ', 124, flags, h, w, w * h, 1, 1)
    header += struct.pack('<2I4s5I', 32, 0x4, b'DX10', 0, 0, 0, 0, 0)  # pixel format: FourCC
    header += struct.pack('<5I', 0x1000, 0, 0, 0, 0)  # caps: texture
    header += struct.pack('<5I', 98, 3, 0, 1, alpha_mode)  # BC7_UNORM, 2D, one, alpha mode
    assert len(header) == 148
    return header + bc7(picture)


def main():
    preview = len(sys.argv) > 1 and sys.argv[1] == '--preview'
    if preview:
        # Small copies to look at, in the folder given (nothing in the repository changes).
        out = Path(sys.argv[2])
        out.mkdir(parents=True, exist_ok=True)
        to_image(background(960, 540)).save(out / 'background.png')
        to_image(launch(960, 540)).save(out / 'launch.png')
        return
    pictures = {}  # icon0.png is the logo (assets/branding/petunia-logo-1024.png), not drawn here
    for source, target, draw in (('background-source.png', 'pic0.dds', background),
                                 ('launch-background-source.png', 'pic1.dds', launch)):
        picture = to_image(draw(), 'RGBA')
        pictures[source] = picture
        # The alpha mode ProsperoRadio's pictures had (DX10: 3, opaque).
        pictures[target] = dds(picture, 3)
        decoded = np.asarray(Image.open(__import__('io').BytesIO(pictures[target])).convert('RGB'), np.float32)
        error = ((decoded - np.asarray(picture.convert('RGB'), np.float32)) ** 2).mean()
        psnr = 10 * math.log10(255 * 255 / max(error, 1e-9))
        print(f'{target}: {psnr:.1f} dB against {source}')
        if psnr < 38:
            sys.exit(f'{target}: the BC7 blocks are too far from the picture')
    for folder in targets:
        for name, picture in pictures.items():
            if isinstance(picture, bytes):
                (folder / name).write_bytes(picture)
            else:
                picture.save(folder / name, optimize=True)
        print(folder.relative_to(root), ', '.join(pictures))


if __name__ == '__main__':
    main()
