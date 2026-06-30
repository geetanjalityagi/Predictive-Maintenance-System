from fastapi import APIRouter

from app.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import predict_failure


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    return predict_failure(request)

