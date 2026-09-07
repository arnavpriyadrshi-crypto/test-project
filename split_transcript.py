
import json
import os
from datetime import datetime


# --------------------------------------------------
# Configuration
# --------------------------------------------------

TRANSCRIPT_PATH = "/Users/arnav/Desktop/highlight-validation/transcript/podcast.json"

OUTPUT_DIR = "/Users/arnav/Desktop/highlight-validation/chunks"

CHUNK_DURATION = 8 * 60  # 8 minutes in seconds


# --------------------------------------------------
# Logging
# --------------------------------------------------

def log(message):
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] {message}",
        flush=True
    )


# --------------------------------------------------
# Time formatting
# --------------------------------------------------

def format_timestamp(seconds):
    """
    Convert seconds into HH:MM:SS format.
    Example:
        0       -> 00:00:00
        494     -> 00:08:14
        3614    -> 01:00:14
    """

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# --------------------------------------------------
# Start
# --------------------------------------------------

log("========================================")
log("Starting transcript chunking")
log("========================================")

log(f"Transcript: {TRANSCRIPT_PATH}")
log(f"Output directory: {OUTPUT_DIR}")
log(f"Chunk duration: {CHUNK_DURATION // 60} minutes")


# --------------------------------------------------
# Check transcript
# --------------------------------------------------

if not os.path.exists(TRANSCRIPT_PATH):
    log("ERROR: Transcript file not found!")
    log(f"Expected: {TRANSCRIPT_PATH}")
    exit(1)

log("Transcript file found.")


# --------------------------------------------------
# Load transcript
# --------------------------------------------------

log("Loading transcript...")

with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
    transcript = json.load(f)

log(f"Loaded {len(transcript)} transcript segments.")


# --------------------------------------------------
# Create output directory
# --------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

log(f"Output directory ready: {OUTPUT_DIR}")


# --------------------------------------------------
# Group transcript segments into chunks
# --------------------------------------------------

chunks = {}

for segment in transcript:

    start = segment["start"]
    end = segment["end"]
    text = segment["text"].strip()

    # Determine which 8-minute chunk this segment belongs to
    chunk_number = int(start // CHUNK_DURATION) + 1

    if chunk_number not in chunks:
        chunks[chunk_number] = []

    chunks[chunk_number].append({
        "start": start,
        "end": end,
        "text": text
    })


# --------------------------------------------------
# Write chunks
# --------------------------------------------------

log(f"Creating {len(chunks)} chunks...")

for chunk_number in sorted(chunks.keys()):

    chunk_segments = chunks[chunk_number]

    chunk_start = (chunk_number - 1) * CHUNK_DURATION
    chunk_end = chunk_number * CHUNK_DURATION

    output_path = os.path.join(
        OUTPUT_DIR,
        f"chunk-{chunk_number:02d}.txt"
    )

    log(
        f"Creating chunk {chunk_number:02d}: "
        f"{format_timestamp(chunk_start)} - "
        f"{format_timestamp(chunk_end)}"
    )

    with open(output_path, "w", encoding="utf-8") as f:

        for segment in chunk_segments:

            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])

            f.write(
                f"[{start_time} - {end_time}]\n"
            )

            f.write(
                f"{segment['text']}\n\n"
            )

    log(
        f"Saved: {output_path} "
        f"({len(chunk_segments)} segments)"
    )


# --------------------------------------------------
# Complete
# --------------------------------------------------

log("========================================")
log("Chunking complete!")
log(f"Total chunks: {len(chunks)}")
log(f"Output: {OUTPUT_DIR}")
log("========================================")

