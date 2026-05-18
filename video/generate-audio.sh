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
MODEL="eleven_turbo_v2_5"

typeset -A CLIPS
CLIPS=(
  [01-intro]="Let me walk you through PocketTriage. It's a paediatric triage assistant built on Gemma 4 that runs entirely on the device. The problem we're solving is real: community health workers in rural Nigeria, where the internet drops out for days at a time, and the only clinical reference is the chart booklet hanging on the wall."
  [02-product]="Here's how it works in practice. The worker types in a patient's symptoms, and the model returns one of three tiers — Pink for refer urgently, Yellow for facility care, Green for home care — together with the matching pathway from the WHO IMCI protocol. Same protocol the worker already follows, just considerably faster."
  [03-context]="And it works completely offline by design. The patient text never leaves the device. There's no server, no analytics, and no fallback to anyone else's cloud."
  [04-evidence]="For our gate, I ran four canonical scenarios from the IMCI chart booklet, with the Wi-Fi disabled and tcpdump capturing anything that left the machine. All four cases matched the WHO protocol exactly, and tcpdump recorded zero packets going anywhere other than localhost. The whole thing is reproducible from the repository."
  [05-architecture]="Architecturally it's one narrow path. Ollama runs Gemma 4 locally, the JSON output is validated and coerced, and then a keyword safety layer enforces four invariants — including forcing a Pink classification whenever a general danger sign appears, even when the model has missed it."
  [06-close]="PocketTriage is open source under Apache 2.0, built by a Nigerian medical intern. The repository is on GitHub. Take a look."
)

CLIP_ORDER=(01-intro 02-product 03-context 04-evidence 05-architecture 06-close)

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
    -d "{\"text\":\"$TEXT\",\"model_id\":\"$MODEL\",\"voice_settings\":{\"stability\":0.42,\"similarity_boost\":0.70,\"style\":0.28,\"use_speaker_boost\":true}}")

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
