#!/usr/bin/env zsh
# Assemble demo video from composites + audio
# Usage: zsh video/assemble.sh

set -e
setopt +o nomatch

SCRIPT_DIR="${0:a:h}"
COMPOSITES_DIR="$SCRIPT_DIR/composites"
AUDIO_DIR="$SCRIPT_DIR/audio"
SEGMENTS_DIR="$SCRIPT_DIR/segments"
OUTPUT="$SCRIPT_DIR/pockettriage-demo.mp4"

mkdir -p "$SEGMENTS_DIR"

# Timing constants (from pipeline spec)
VFADE_IN=0.2
AUDIO_DELAY=0.5
BREATH=0.3
VFADE_OUT=0.2
GAP=0.3

CLIP_ORDER=(01-intro 02-product 03-context 04-evidence 05-architecture 06-close)

echo "Building segments..."

for clip in "${CLIP_ORDER[@]}"; do
  COMPOSITE="$COMPOSITES_DIR/$clip.png"
  AUDIO="$AUDIO_DIR/$clip.mp3"
  SEG="$SEGMENTS_DIR/$clip.mp4"

  if [[ ! -f "$COMPOSITE" || ! -f "$AUDIO" ]]; then
    echo "  SKIP $clip (missing composite or audio)"
    continue
  fi

  # Get audio duration
  AUDIO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$AUDIO")

  # Calculate total segment duration
  # AUDIO_DELAY + audio + BREATH + VFADE_OUT
  TOTAL=$(python3 -c "print(round($AUDIO_DELAY + $AUDIO_DUR + $BREATH + $VFADE_OUT, 3))")
  FO_START=$(python3 -c "print(round($TOTAL - $VFADE_OUT, 3))")
  AFO_START=$(python3 -c "print(round($AUDIO_DELAY + $AUDIO_DUR - 0.25, 3))")

  echo "  SEG  $clip (audio=${AUDIO_DUR}s, total=${TOTAL}s)"

  ffmpeg -y \
    -loop 1 -i "$COMPOSITE" \
    -i "$AUDIO" \
    -filter_complex "
      anullsrc=r=44100:cl=stereo,atrim=0:${AUDIO_DELAY}[silence];
      [silence][1:a]concat=n=2:v=0:a=1[joined];
      [joined]afade=t=in:st=${AUDIO_DELAY}:d=0.15,afade=t=out:st=${AFO_START}:d=0.25,apad=whole_dur=${TOTAL}[a];
      [0:v]scale=1920:1080,fade=t=in:st=0:d=${VFADE_IN},fade=t=out:st=${FO_START}:d=${VFADE_OUT}[v]
    " \
    -map "[v]" -map "[a]" \
    -t "$TOTAL" \
    -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
    -c:a aac -b:a 128k \
    -r 30 "$SEG" 2>/dev/null

  if [[ ! -f "$SEG" ]]; then
    echo "  ERROR: Failed to create segment for $clip"
    exit 1
  fi
done

# Create black gap segment
GAP_SEG="$SEGMENTS_DIR/gap.mp4"
echo "  GAP  (${GAP}s black)"
ffmpeg -y \
  -f lavfi -i "color=c=black:s=1920x1080:d=${GAP}:r=30" \
  -f lavfi -i "anullsrc=r=44100:cl=stereo" \
  -t "$GAP" \
  -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  "$GAP_SEG" 2>/dev/null

# Build concat list (segment, gap, segment, gap, ..., segment)
CONCAT_LIST="$SEGMENTS_DIR/concat.txt"
> "$CONCAT_LIST"
for i in {1..${#CLIP_ORDER[@]}}; do
  clip="${CLIP_ORDER[$i]}"
  echo "file '${CLIP_ORDER[$i]}.mp4'" >> "$CONCAT_LIST"
  if (( i < ${#CLIP_ORDER[@]} )); then
    echo "file 'gap.mp4'" >> "$CONCAT_LIST"
  fi
done

echo "Assembling final video..."

# Re-encode during concat (never -c copy)
ffmpeg -y \
  -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -r 30 "$OUTPUT" 2>/dev/null

FINAL_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT")
echo ""
echo "Done: $OUTPUT (${FINAL_DUR}s)"
