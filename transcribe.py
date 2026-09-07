
from faster_whisper import WhisperModel
import json
import os
import time
from datetime import datetime


def log(message):
    """Print a timestamped log message."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", flush=True)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AUDIO_PATH = "/Users/arnav/Desktop/highlight-validation/audio/podcast.mp3"
OUTPUT_PATH = "/Users/arnav/Desktop/highlight-validation/transcript/podcast.json"


# --------------------------------------------------
# Start
# --------------------------------------------------

start_time = time.time()

log("========================================")
log("Starting transcription")
log("========================================")

log(f"Audio file: {AUDIO_PATH}")
log(f"Output file: {OUTPUT_PATH}")


# --------------------------------------------------
# Check audio file
# --------------------------------------------------

if not os.path.exists(AUDIO_PATH):
    log("ERROR: Audio file not found!")
    log(f"Expected file at: {AUDIO_PATH}")
    exit(1)

audio_size = os.path.getsize(AUDIO_PATH) / (1024 * 1024)

log(f"Audio file found ({audio_size:.2f} MB)")


# --------------------------------------------------
# Create output directory
# --------------------------------------------------

output_directory = os.path.dirname(OUTPUT_PATH)

os.makedirs(output_directory, exist_ok=True)

log(f"Output directory ready: {output_directory}")


# --------------------------------------------------
# Load Whisper model
# --------------------------------------------------

log("Loading Whisper model...")
log("Model: small")
log("Device: CPU")
log("Compute type: int8")

model_start = time.time()

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

model_time = time.time() - model_start

log(f"Whisper model loaded successfully ({model_time:.2f}s)")


# --------------------------------------------------
# Start transcription
# --------------------------------------------------

log("Starting audio transcription...")
log("VAD filter: enabled")
log("This may take some time depending on audio length.")

transcription_start = time.time()

segments, info = model.transcribe(
    AUDIO_PATH,
    vad_filter=True
)


# --------------------------------------------------
# Process segments
# --------------------------------------------------

log("Transcription started. Processing segments...")

results = []
segment_count = 0

for segment in segments:
    segment_count += 1

    text = segment.text.strip()

    results.append({
        "start": segment.start,
        "end": segment.end,
        "text": text
    })

    log(
        f"Segment {segment_count}: "
        f"{segment.start:.2f}s → {segment.end:.2f}s | "
        f"{text}"
    )


transcription_time = time.time() - transcription_start

log(f"Transcription finished ({transcription_time:.2f}s)")
log(f"Total segments: {segment_count}")


# --------------------------------------------------
# Save JSON
# --------------------------------------------------

log("Saving transcription to JSON...")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False
    )

log("JSON file saved successfully.")


# --------------------------------------------------
# Finished
# --------------------------------------------------

total_time = time.time() - start_time

log("========================================")
log("Transcription complete!")
log(f"Segments: {segment_count}")
log(f"Output: {OUTPUT_PATH}")
log(f"Total time: {total_time:.2f}s")
log("========================================")

