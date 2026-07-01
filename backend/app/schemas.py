from pydantic import BaseModel, Field
from typing import Annotated, Dict

class PredictionRequest(BaseModel):
    machine_type : Annotated[str, Field(..., examples=['L'])]
    air_temperature_k : Annotated[float, Field(..., gt=0, description='Enter air temperature [K] : ')]
    process_temperature_k : Annotated[float, Field(..., gt=0, description='Enter process temperature [K] : ')]
    rotational_speed_rpm : Annotated[float, Field(..., gt=0, description='Enter rotational speed [rpm] : ')]
    torque_nm : Annotated[float, Field(..., gt=0, description='Enter torque [Nm] : ')]
    tool_wear_min : Annotated[float, Field(..., gt=0, description='Enter tool wera [min] : ')]

class PredictionResponse(BaseModel):
    machine_status: str
    failure_type: str
    confidence: float
    risk_level: str
    recommendation: str
    class_probabilities: Dict[str, float]