#!/usr/bin/env zsh
# v3 silent cut — no voice, no music, no subtitles.
# Uses raw scene frames (not caption composites) so frames render clean.
# Tighter pacing — each clip held just long enough to read the on-frame text.

set -e
setopt +o nomatch

SCRIPT_DIR="${0:a:h}"
FRAMES_DIR="$SCRIPT_DIR/frames"
SEGMENTS_DIR="$SCRIPT_DIR/segments-silent"
OUTPUT="$SCRIPT_DIR/pockettriage-demo-silent.mp4"

mkdir -p "$SEGMENTS_DIR"
rm -f "$SEGMENTS_DIR"/*.mp4 2>/dev/null

# Per-clip hold time (seconds visible after fade-in, before fade-out)
typeset -A HOLDS
HOLDS=(
  [01-hook]=6.0
  [02-context]=5.5
  [03-where]=4.0
  [04-evidence]=7.0
  [05-architecture]=6.0
  [06-close]=4.5
)
CLIP_ORDER=(01-hook 02-context 03-where 04-evidence 05-architecture 06-close)

VFADE=0.25

for clip in "${CLIP_ORDER[@]}"; do
  IMG="$FRAMES_DIR/$clip.png"
  SEG="$SEGMENTS_DIR/$clip.mp4"
  HOLD="${HOLDS[$clip]}"
  TOTAL=$(python3 -c "print(round($VFADE + $HOLD + $VFADE, 3))")
  FO_START=$(python3 -c "print(round($TOTAL - $VFADE, 3))")

  echo "  SEG  $clip  hold=${HOLD}s  total=${TOTAL}s"

  ffmpeg -y -loop 1 -i "$IMG" \
    -f lavfi -i "anullsrc=r=44100:cl=stereo" \
    -filter_complex "
      [0:v]scale=1920:1080,fade=t=in:st=0:d=${VFADE},fade=t=out:st=${FO_START}:d=${VFADE}[v]
    " \
    -map "[v]" -map "1:a" \
    -t "$TOTAL" \
    -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
    -c:a aac -b:a 96k \
    -r 30 "$SEG" 2>/dev/null
done

# Black gap between clips
GAP=0.25
GAP_SEG="$SEGMENTS_DIR/gap.mp4"
ffmpeg -y \
  -f lavfi -i "color=c=black:s=1920x1080:d=${GAP}:r=30" \
  -f lavfi -i "anullsrc=r=44100:cl=stereo" \
  -t "$GAP" \
  -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
  -c:a aac -b:a 96k \
  "$GAP_SEG" 2>/dev/null

# Concat list
CONCAT_LIST="$SEGMENTS_DIR/concat.txt"
> "$CONCAT_LIST"
for i in {1..${#CLIP_ORDER[@]}}; do
  echo "file '${CLIP_ORDER[$i]}.mp4'" >> "$CONCAT_LIST"
  if (( i < ${#CLIP_ORDER[@]} )); then
    echo "file 'gap.mp4'" >> "$CONCAT_LIST"
  fi
done

echo "  CONCAT…"
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" \
  -vf "eq=contrast=1.06:saturation=1.06:brightness=0.015:gamma=1.02" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 96k \
  -r 30 "$OUTPUT" 2>/dev/null

DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT")
SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
echo ""
echo "Done: $OUTPUT  (${DUR}s, ${SIZE} bytes)"
