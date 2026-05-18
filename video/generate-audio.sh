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
  [01-hook]="Here. Eleven-month-old. Cough. Chest indrawing. Refusing to drink. The model returns Pink, refer urgently. Ten seconds. Wi-Fi is off."
  [02-context]="PocketTriage is the WHO IMCI chart booklet, as a phone tool. Gemma 4, locally, on Ollama. Same protocol, same Pink-Yellow-Green tiers. Just faster."
  [03-where]="Why offline. Anambra State, hours without power, two G if you're lucky. The chart booklet on the wall is still the only chart."
  [04-evidence]="Phase one gate. Four canonical IMCI scenarios. Wi-Fi off, tcpdump running. Four out of four match the WHO protocol. Zero non-localhost packets. Reproducible from the repo."
  [05-architecture]="One path. Ollama runs Gemma 4 locally. Patient text never leaves the device. No server, no analytics. A keyword safety layer catches danger signs even when the model misses them."
  [06-close]="PocketTriage. Open source, Apache 2.0. Built by a Nigerian medical intern. Repo's on GitHub. Take it."
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
    -d "{\"text\":\"$TEXT\",\"model_id\":\"$MODEL\",\"voice_settings\":{\"stability\":0.55,\"similarity_boost\":0.65,\"style\":0.15,\"use_speaker_boost\":true}}")

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
