#!/usr/bin/env python3
"""Composite subtitle captions onto video frames.

Reads frames from video/frames/, renders verbatim subtitle text
in a semi-transparent box at bottom center, outputs to video/composites/.
"""

import os
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).parent
FRAMES_DIR = SCRIPT_DIR / "frames"
COMPOSITES_DIR = SCRIPT_DIR / "composites"
COMPOSITES_DIR.mkdir(exist_ok=True)

TARGET_W, TARGET_H = 1920, 1080

# Subtitle text — MUST match VOICEOVER_CLIPS.md and generate-audio.sh verbatim
CLIPS = {
    "01-hook":         "Severe pneumonia. WHO IMCI protocol.\nPink. Refer urgently.\nThe model is Gemma 4 on this laptop. Wi-Fi off.",
    "02-context":      "PocketTriage is the WHO IMCI chart booklet\nas a phone tool. Gemma 4 runs on the device.\nSame protocol. Same action. Faster.",
    "03-where":        "Anambra State, Nigeria.\nPatchy two-G. Hours without power.\nThis is where the chart booklet still rules.",
    "04-evidence":     "Four canonical scenarios from the chart booklet.\nWi-Fi off. Tcpdump running.\nFour out of four agree with the WHO protocol. Zero packets.",
    "05-architecture": "One narrow path. The model runs locally.\nThe patient text never leaves the device.\nNo server. No analytics. No fallback to anyone's cloud.",
    "06-close":        "PocketTriage.\nBuilt by a Nigerian medical intern.\nOpen source. On GitHub now.",
}

# Font selection (sans-serif, never monospace)
FONT_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/Library/Fonts/Arial.ttf",
]

def get_font(size=32):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def composite_caption(frame_path, text, out_path):
    img = Image.open(frame_path).convert("RGBA")

    # Resize to target if needed
    if img.size != (TARGET_W, TARGET_H):
        # Center the frame on a black 1920x1080 canvas
        canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 255))
        # Scale frame to fit
        ratio = min(TARGET_W / img.width, TARGET_H / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        x = (TARGET_W - new_w) // 2
        y = (TARGET_H - new_h) // 2
        canvas.paste(img, (x, y))
        img = canvas

    font = get_font(32)
    lines = text.split("\n")
    line_height = 42
    padding = 20
    margin_x = 160

    # Calculate text block size
    draw = ImageDraw.Draw(img)
    max_line_w = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        max_line_w = max(max_line_w, line_w)

    block_h = len(lines) * line_height
    box_w = max_line_w + padding * 2
    box_h = block_h + padding * 2

    # Position at bottom center
    box_x = (TARGET_W - box_w) // 2
    box_y = TARGET_H - box_h - 60  # 60px from bottom

    # Draw semi-transparent box
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [(box_x, box_y), (box_x + box_w, box_y + box_h)],
        radius=12,
        fill=(0, 0, 0, 120),
    )
    img = Image.alpha_composite(img, overlay)

    # Draw text
    draw = ImageDraw.Draw(img)
    text_x = box_x + padding
    text_y = box_y + padding
    for i, line in enumerate(lines):
        # Center each line within the box
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        lx = box_x + (box_w - line_w) // 2
        draw.text((lx, text_y + i * line_height), line, font=font, fill=(255, 255, 255, 240))

    # Save as RGB PNG
    img.convert("RGB").save(out_path, "PNG")
    print(f"  {out_path.name}")

def main():
    for clip_name, text in CLIPS.items():
        frame = FRAMES_DIR / f"{clip_name}.png"
        out = COMPOSITES_DIR / f"{clip_name}.png"
        if not frame.exists():
            print(f"  SKIP {clip_name} (no frame)")
            continue
        composite_caption(frame, text, out)
    print(f"Done. Composites in {COMPOSITES_DIR}")

if __name__ == "__main__":
    main()
