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
    "01-hook":         "Here. Eleven-month-old. Cough. Chest indrawing. Refusing to drink.\nThe model returns Pink, refer urgently. Ten seconds. Wi-Fi is off.",
    "02-context":      "PocketTriage is the WHO IMCI chart booklet, as a phone tool.\nGemma 4, locally, on Ollama. Same Pink-Yellow-Green tiers. Just faster.",
    "03-where":        "Why offline. Anambra State, hours without power, two G if you're lucky.\nThe chart booklet on the wall is still the only chart.",
    "04-evidence":     "Phase one gate. Four canonical IMCI scenarios. Wi-Fi off, tcpdump running.\nFour out of four match the WHO protocol. Zero non-localhost packets.",
    "05-architecture": "One path. Ollama runs Gemma 4 locally. Patient text never leaves the device.\nA keyword safety layer catches danger signs even when the model misses them.",
    "06-close":        "PocketTriage. Open source, Apache 2.0.\nBuilt by a Nigerian medical intern. Repo's on GitHub. Take it.",
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

    # Cleaner, less template-y subtitle: bold white text bottom-center
    # with a soft drop shadow + a thin accent rule above. No big black box.
    font = get_font(38)
    lines = text.split("\n")
    line_height = 50

    draw = ImageDraw.Draw(img)
    max_line_w = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        max_line_w = max(max_line_w, line_w)

    block_h = len(lines) * line_height
    block_y = TARGET_H - block_h - 70  # 70px from bottom edge

    # Soft scrim — narrow horizontal band, very faint, just under the text
    # block. Keeps text readable over busy frames without the "AI demo box".
    scrim = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    sd.rectangle(
        [(0, block_y - 24), (TARGET_W, TARGET_H)],
        fill=(0, 0, 0, 70),
    )
    img = Image.alpha_composite(img, scrim)

    # Thin accent rule above the text block — anchors it without a box
    rule = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rule)
    rule_w = 60
    rule_x = (TARGET_W - rule_w) // 2
    rd.rectangle(
        [(rule_x, block_y - 14), (rule_x + rule_w, block_y - 11)],
        fill=(0, 61, 114, 235),  # navy accent
    )
    img = Image.alpha_composite(img, rule)

    # Render text twice — once as a black shadow (offset 2 px) for legibility,
    # once as bold white. No background box.
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        lx = (TARGET_W - line_w) // 2
        ly = block_y + i * line_height
        # Multi-direction shadow stack for crisp legibility
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (2, 2), (-2, -2)]:
            draw.text((lx + dx, ly + dy), line, font=font, fill=(0, 0, 0, 220))
        draw.text((lx, ly), line, font=font, fill=(255, 255, 255, 255))

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
