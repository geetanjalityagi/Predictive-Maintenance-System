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


def get_risk_level(confidence: float, failure: bool) -> str:
    if not failure:
        return "Low"
    elif confidence >= 0.95:
        return "Critical"

    elif confidence >= 0.80:
        return "High"

    elif confidence >= 0.60:
        return "Medium"

    else:
        return "Low"
    


def get_recommendation(failure_type: str) -> str:
    if failure_type == "No Failure":
        return "Machine is operating normally. Continue routine monitoring."

    recommendations = {
    "Tool Wear Failure (TWF)":
        "Replace or inspect the cutting tool.",

    "Heat Dissipation Failure (HDF)":
        "Inspect the cooling system and ventilation.",

    "Power Failure (PWF)":
        "Inspect motor, electrical supply and transmission system.",

    "Overstrain Failure (OSF)":
        "Reduce machine load and inspect mechanical components.",

    "Other Failure":
        "Perform comprehensive inspection to identify root cause."
    }

    return recommendations.get(
        failure_type,
        "Inspect the machine and monitor operating conditions."
    )

def predict_failure(request : PredictionRequest):
    input_df = build_feature(request)

    predicted_class = int(model.predict(input_df)[0])
    probability_array = model.predict_proba(input_df)[0]

    failure = predicted_class != 0
    failure_type = FAILURE_MAP[predicted_class]

    confidence = round(float(probability_array[predicted_class]), 4)

    risk_level = get_risk_level(confidence, failure)
    recommendation = get_recommendation(failure_type)

    probabilities = {
        FAILURE_MAP[i]: round(float(probability_array[i]), 4)
        for i in range(len(FAILURE_MAP))
    }

    return {
        "machine_status": "Failure Detected" if failure else "No Failure Detected",
        "failure_type": failure_type,
        "confidence": confidence,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "class_probabilities": probabilities
    }