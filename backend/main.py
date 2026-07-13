from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import logging

from audio_processor import save_uploaded_file, delete_file

from database import (
    save_audio_file,
    save_result,
    get_all_results,
    get_result_by_id,
)

from predict import predict_audio
from schemas import UploadResponse, AnalysisResponse


# -----------------------------
# Logging Configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("deeptrust.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": "DeepTrust API"
    }


# -----------------------------
# Upload Audio
# -----------------------------

@app.post("/upload", response_model=UploadResponse)
def upload_file(file: UploadFile = File(...)):
    file_path = None

    logger.info(
        "Upload request received: original_filename=%s",
        file.filename,
    )

    try:
        # Validate the file and save it with a secure unique name
        file_path, file_size = save_uploaded_file(file)

        logger.info(
            "File validated and saved: original_filename=%s "
            "stored_filename=%s size_bytes=%s",
            file.filename,
            file_path.name,
            file_size,
        )

        save_audio_file(
            file_name=file_path.name,
            file_path=str(file_path),
            file_size=file_size,
            analysis_id=None,
        )

        logger.info(
            "File information saved to database: filename=%s",
            file_path.name,
        )

        return {
            "message": "File uploaded successfully",
            "filename": file_path.name,
        }

    except HTTPException as error:
        logger.warning(
            "Upload rejected: filename=%s status_code=%s reason=%s",
            file.filename,
            error.status_code,
            error.detail,
        )

        raise

    except Exception as error:
        delete_file(file_path)

        logger.exception(
            "Unexpected upload error: filename=%s",
            file.filename,
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading the file.",
        ) from error


# -----------------------------
# Get Results
# -----------------------------

@app.get("/results", response_model=list[AnalysisResponse])
def get_results():
    logger.info("All analysis results requested")

    try:
        results = get_all_results()

        logger.info(
            "Analysis results returned successfully: count=%s",
            len(results),
        )

        return results

    except Exception as error:
        logger.exception("Could not retrieve analysis results")

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve analysis results.",
        ) from error


@app.get("/results/{id}", response_model=AnalysisResponse)
def get_result(id: int):
    logger.info("Analysis result requested: id=%s", id)

    try:
        result = get_result_by_id(id)

        if result is None:
            logger.warning(
                "Analysis result not found: id=%s",
                id,
            )

            raise HTTPException(
                status_code=404,
                detail="Result not found.",
            )

        logger.info(
            "Analysis result returned successfully: id=%s",
            id,
        )

        return result

    except HTTPException:
        raise

    except Exception as error:
        logger.exception(
            "Could not retrieve analysis result: id=%s",
            id,
        )

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve the requested result.",
        ) from error


# -----------------------------
# Analyze Audio
# -----------------------------

@app.post("/analyze")
async def analyze_audio(file_name: str):
    logger.info(
        "Analysis request received: filename=%s",
        file_name,
    )

    audio_path = os.path.join("uploads", file_name)

    if not os.path.exists(audio_path):
        logger.warning(
            "Analysis rejected because file was not found: filename=%s",
            file_name,
        )

        raise HTTPException(
            status_code=404,
            detail="Audio file not found.",
        )

    allowed_extensions = {
        ".wav",
        ".flac",
        ".mp3",
        ".m4a",
        ".ogg",
        ".webm",
    }

    extension = os.path.splitext(file_name)[1].lower()

    if extension not in allowed_extensions:
        logger.warning(
            "Analysis rejected because extension is unsupported: "
            "filename=%s extension=%s",
            file_name,
            extension,
        )

        raise HTTPException(
            status_code=400,
            detail="Only valid audio files can be analyzed.",
        )

    try:
        logger.info(
            "Audio analysis started: filename=%s",
            file_name,
        )

        result = predict_audio(audio_path)

        save_result(
            file_name=file_name,
            result=result["prediction"],
            confidence=result["confidence"],
        )

        logger.info(
            "Audio analysis completed: filename=%s "
            "prediction=%s confidence=%s",
            file_name,
            result["prediction"],
            result["confidence"],
        )

        return {
            "file_name": file_name,
            "result": result["prediction"],
            "confidence": result["confidence"],
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception(
            "Audio analysis failed: filename=%s",
            file_name,
        )

        raise HTTPException(
            status_code=400,
            detail="The file could not be analyzed as valid audio.",
        ) from error
