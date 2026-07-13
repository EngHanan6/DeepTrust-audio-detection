from fastapi import FastAPI, UploadFile, File
import os
import shutil
import traceback

from huggingface_hub import delete_file

from database import (
    save_audio_file,
    save_result,
    get_all_results,
    get_result_by_id
)

from predict import predict_audio
from schemas import UploadResponse, AnalysisResponse

app = FastAPI()


@app.get("/")
def home():
    print("HOME ENDPOINT WORKS")
    return {
        "message": "DeepTrust API"
    }


# -----------------------------
# Upload Audio
# -----------------------------

@app.post("/upload", response_model=UploadResponse)
def upload_file(file: UploadFile = File(...)):
    try:
        print("1- Request received")

        # إنشاء مجلد uploads إذا لم يكن موجودًا
        os.makedirs("uploads", exist_ok=True)

        file_path = os.path.join("uploads", file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("2- File saved")

        file_size = os.path.getsize(file_path)

        print("3- File size calculated")

        save_audio_file(
            file_name=file.filename,
            file_path=file_path,
            file_size=file_size,
            analysis_id=None
        )

        print("4- Saved to database")

        return {
            "message": "File uploaded successfully",
            "filename": file.filename
        }

    except Exception as error:
       delete_file(file_path)

    print("\n========== ERROR ==========")
    print(error)
    traceback.print_exc()
    print("===========================\n")

    raise


# -----------------------------
# Get Results
# -----------------------------
@app.get("/results", response_model=list[AnalysisResponse])
def get_results():
    return get_all_results()


@app.get("/results/{id}", response_model=AnalysisResponse)
def get_result(id: int):
    return get_result_by_id(id)


# -----------------------------
# Analyze Audio
# -----------------------------

@app.post("/analyze")
async def analyze_audio(file_name: str):

    audio_path = os.path.join("uploads", file_name)

    result = predict_audio(audio_path)

    save_result(
        file_name=file_name,
        result=result["prediction"],
        confidence=result["confidence"]
    )

    return {
        "file_name": file_name,
        "result": result["prediction"],
        "confidence": result["confidence"]
    }