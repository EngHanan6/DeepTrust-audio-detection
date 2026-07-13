from pathlib import Path

import torchaudio
from fastapi import FastAPI, File, UploadFile

from audio_processor import (
    delete_file,
    preprocess_audio,
    save_uploaded_file,
)

app = FastAPI(title="File Processing Test")


@app.post("/test-process")
def test_process(file: UploadFile = File(...)):
    original_path: Path | None = None
    processed_path: Path | None = None

    try:
        # Validate and temporarily save the uploaded file
        original_path, original_size = save_uploaded_file(file)

        # Convert to WAV, mono, 16 kHz, PCM 16-bit
        processed_path = preprocess_audio(original_path)

        # Verify the processed file
        waveform, sample_rate = torchaudio.load(str(processed_path))

        return {
            "message": "File processing completed successfully",
            "original_filename": file.filename,
            "original_size_bytes": original_size,
            "processed_format": processed_path.suffix,
            "sample_rate": sample_rate,
            "channels": waveform.shape[0],
            "processed_file_exists_during_test": processed_path.exists(),
        }

    finally:
        # Clean up both temporary files
        delete_file(original_path)
        delete_file(processed_path)