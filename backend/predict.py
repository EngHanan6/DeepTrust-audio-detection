import torch
import librosa

from transformers import (
    AutoFeatureExtractor,
    HubertForSequenceClassification
)

# -----------------------------
# Load Model
# -----------------------------

MODEL_PATH = "DeepTrust_Model"

feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_PATH)

model = HubertForSequenceClassification.from_pretrained(MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)
model.eval()

# -----------------------------
# Labels
# -----------------------------

id2label = {
    0: "Real",
    1: "Fake"
}

# -----------------------------
# Prediction Function
# -----------------------------

def predict_audio(audio_path):

    waveform, sample_rate = librosa.load(
        audio_path,
        sr=16000,
        mono=True
    )

    waveform = torch.tensor(waveform)

    inputs = feature_extractor(
        waveform.numpy(),
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    return {
        "prediction": id2label[prediction.item()],
        "confidence": round(
            confidence.item() * 100,
            2
        )
    }