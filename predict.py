import torch
import torchaudio
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

model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

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

    waveform, sample_rate = torchaudio.load(audio_path)

    # Convert to Mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(
            sample_rate,
            16000
        )
        waveform = resampler(waveform)

    inputs = feature_extractor(
        waveform.squeeze().numpy(),
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )

    inputs = {
        k: v.to(device)
        for k, v in inputs.items()
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

result = predict_audio("test.wav") #change the path to your audio file

print(result)