from fastapi import APIRouter

from app.schemas import PredictionRequest, PredictionResponse
from app.services.prediction_service import predict_failure

router = APIRouter()

@router.post('\preedict', response=PredictionResponse)
def predict(request : PredictionRequest):
    return predict_failure(request)

