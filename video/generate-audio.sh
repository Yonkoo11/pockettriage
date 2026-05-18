#!/usr/bin/env zsh
# PocketTriage voiceover via ElevenLabs Brian voice.
# Reads API key from ~/.config/pockettriage/eleven.key (0600). Never echoes the key.

set -e
setopt +o nomatch

SCRIPT_DIR="${0:a:h}"
AUDIO_DIR="$SCRIPT_DIR/audio"
mkdir -p "$AUDIO_DIR"

KEY_FILE="$HOME/.config/pockettriage/eleven.key"
if [[ ! -r "$KEY_FILE" ]]; then
  echo "ERROR: keyfile $KEY_FILE missing or unreadable"
  exit 1
fi
ELEVENLABS_API_KEY="$(cat "$KEY_FILE")"

VOICE_ID="nPczCjzI2devNBz1zQrb"  # Brian
MODEL="eleven_multilingual_v2"

typeset -A CLIPS
CLIPS=(
  [01-hook]="Severe pneumonia. WHO IMCI protocol. Pink. Refer urgently. The model is Gemma 4 on this laptop. Wi-Fi off."
  [02-context]="PocketTriage is the WHO IMCI chart booklet as a phone tool. Gemma 4 runs on the device. Same protocol. Same action. Faster."
  [03-where]="Anambra State, Nigeria. Patchy two-G. Hours without power. This is where the chart booklet still rules."
  [04-evidence]="Four canonical scenarios from the chart booklet. Wi-Fi off. Tcpdump running. Four out of four agree with the WHO protocol. Zero packets."
  [05-architecture]="One narrow path. The model runs locally. The patient text never leaves the device. No server. No analytics. No fallback to anyone's cloud."
  [06-close]="PocketTriage. Built by a Nigerian medical intern. Open source. On GitHub now."
)

CLIP_ORDER=(01-hook 02-context 03-where 04-evidence 05-architecture 06-close)

for clip in "${CLIP_ORDER[@]}"; do
  OUT="$AUDIO_DIR/$clip.mp3"
  if [[ -f "$OUT" && -s "$OUT" ]]; then
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT")
    echo "  SKIP $clip (${DUR}s)"
    continue
  fi

  TEXT="${CLIPS[$clip]}"
  echo "  GEN  $clip"

  HTTP_CODE=$(curl -s -o "$OUT" -w "%{http_code}" \
    -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"$TEXT\",\"model_id\":\"$MODEL\",\"voice_settings\":{\"stability\":0.82,\"similarity_boost\":0.65,\"style\":0.03}}")

  SIZE=$(wc -c < "$OUT" | tr -d ' ')
  if [[ "$HTTP_CODE" != "200" ]] || [[ "$SIZE" -lt 5000 ]]; then
    echo "  ERROR $clip (http=$HTTP_CODE size=$SIZE):"
    head -c 200 "$OUT"; echo
    rm -f "$OUT"
    exit 1
  fi

  DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT")
  echo "  OK   $clip (${DUR}s)"
done

echo "Done. Audio in $AUDIO_DIR"
