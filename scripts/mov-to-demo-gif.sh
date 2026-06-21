#!/usr/bin/env bash
# macOS screen recording → docs/demo.gif.
# Two-pass palette: sample one mid-clip frame so collapsed-rail frames don't grey the GIF.
# SDR (bt709) — use as-is. HDR captures: re-record in SDR if colors look wrong.
set -euo pipefail

src="${1:?usage: mov-to-demo-gif.sh <recording.mov> [out.gif]}"
dest="${2:-$(dirname "$0")/../docs/demo.gif}"
palette="${TMPDIR:-/tmp}/gvr-demo-palette-$$.png"
trap 'rm -f "$palette"' EXIT

eq="eq=saturation=1.08:contrast=1.03"
scale="scale=600:-1:flags=lanczos,format=rgb24"
speed=2.75  # 26s clip → ~10s GIF (was 5.5 → ~5s)

# Frame ~3s in — usually expanded sidebar / bright page
ffmpeg -y -loglevel error -i "$src" \
  -vf "select=eq(n\\,180),${scale},${eq},palettegen=stats_mode=diff" \
  -frames:v 1 "$palette"

ffmpeg -y -loglevel error -i "$src" -i "$palette" \
  -lavfi "[0:v]setpts=PTS/${speed},fps=12,${scale},${eq}[v];[v][1:v]paletteuse=dither=bayer:bayer_scale=5" \
  -loop 0 "$dest"

echo "Wrote $dest ($(du -h "$dest" | cut -f1))"
