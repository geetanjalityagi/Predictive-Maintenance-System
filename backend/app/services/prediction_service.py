import joblib
from pathlib import Path

from app.schemas import PredictionRequest
from app.services.feature_engineering import build_feature

MODEL_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "predictive_maintenance_model.pkl"

FAILURE_MAP = {
    0: "No Failure",
    1: "Tool Wear Failure (TWF)",
    2: "Heat Dissipation Failure (HDF)",
    3: "Power Failure (PWF)",
    4: "Overstrain Failure (OSF)",
    5: "Other Failure"
}

model = joblib.load(MODEL_PATH)

def predict_failure(request : PredictionRequest):
    input_df = build_feature(request)

    predicted_class = int(model.predict(input_df)[0])
    probability_array = model.predict_proba(input_df)[0]

    probabilities = {
        FAILURE_MAP[i]: round(float(probability_array[i]), 4)
        for i in range(len(FAILURE_MAP))
    }

    confidence = round(float(probability_array[predicted_class]), 4)

    return {
        "failure": predicted_class != 0,
        "failure_type": FAILURE_MAP[predicted_class],
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities
    }