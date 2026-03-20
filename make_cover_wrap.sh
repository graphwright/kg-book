#!/bin/bash
# make_cover_wrap.sh -- build a full cover wrap for a 6x9 book
#
# Usage: ./make_cover_wrap.sh <spine_width_inches> [output_file]
#
# Example:
#   ./make_cover_wrap.sh 0.85
#   ./make_cover_wrap.sh 0.85 wrap.jpg
#
# Requirements: ImageMagick (convert), bc

set -e

SPINE_INCHES="${1:?Usage: $0 <spine_width_inches> [output_file]}"
OUTPUT="${2:-cover_wrap.jpg}"

BACK_TEXT="Large language models are fluent, confident, and wrong in ways that are hard to anticipate. The fix is not better prompting — it is grounding: giving the model a structured, inspectable, provenance-tracked representation of what is actually known in your domain. That is a knowledge graph.

This book covers the full arc: why knowledge graphs are necessary for reliable machine reasoning, how fifty years of attempts to build them stalled at the same extraction bottleneck, and why that bottleneck is finally tractable. It then walks through the engineering — schema design, LLM-based extraction, identity resolution, provenance tracking, and graph serving — with a working implementation in medical literature as the concrete example throughout.

If you have a corpus and a domain, you have what you need to start."

FRONT="Cover6x9.jpg"
DPI=300
HEIGHT=2700          # 9 inches * 300 DPI
COVER_W=1800         # 6 inches * 300 DPI
SPINE_W=$(echo "$SPINE_INCHES * $DPI" | bc | xargs printf "%.0f")
TOTAL_W=$(( COVER_W + SPINE_W + COVER_W ))

DARK_BLUE="#1a2a4a"
WHITE="#ffffff"
FONT="DejaVu-Sans-Bold"

# --- Back cover ---
BACK_FONT_SIZE=72
BACK_TEXT_W=$(( COVER_W - 200 ))   # 100px margin each side
BACK_X=$(( COVER_W / 2 ))
BACK_Y=$(( HEIGHT * 2 / 5 ))       # slightly above center

convert \
    -size "${COVER_W}x${HEIGHT}" \
    xc:"${DARK_BLUE}" \
    -font "${FONT}" \
    -pointsize "${BACK_FONT_SIZE}" \
    -fill "${WHITE}" \
    -gravity None \
    -size "${BACK_TEXT_W}x" \
    caption:"${BACK_TEXT}" \
    -geometry "+100+0" \
    -gravity North \
    -geometry "+0+${BACK_Y}" \
    -composite \
    /tmp/back_cover.png

# --- Spine ---
SPINE_FONT_SIZE=60
SPINE_TEXT="Knowledge Graphs from Unstructured Text    Will Ware"

# Build spine as a wide image, then rotate 90 degrees clockwise
# so text reads top-to-bottom
SPINE_TEXT_W=$(( HEIGHT - 100 ))   # leave 50px margin each end

convert \
    -size "${HEIGHT}x${SPINE_W}" \
    xc:"${DARK_BLUE}" \
    -font "${FONT}" \
    -pointsize "${SPINE_FONT_SIZE}" \
    -fill "${WHITE}" \
    -gravity Center \
    -annotate 0 "${SPINE_TEXT}" \
    -rotate 90 \
    /tmp/spine.png

# --- Assemble wrap ---
convert \
    /tmp/back_cover.png \
    /tmp/spine.png \
    "${FRONT}" \
    +append \
    -density "${DPI}" \
    "${OUTPUT}"

echo "Written: ${OUTPUT}  (${TOTAL_W}x${HEIGHT} px, spine ${SPINE_W}px / ${SPINE_INCHES}\")"
