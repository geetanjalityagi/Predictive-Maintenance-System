import numpy as np
import pandas as pd
from app.schemas import PredictionRequest

def build_feature(request : PredictionRequest) -> pd.DataFrame:
    temperature_difference = (
        request.process_temperature_k - request.air_temperature_k
    )

    power = (
        request.torque_nm * request.rotational_speed_rpm * (2 * np.pi / 60.0)
    )

    torque_wear_stress = (
        request.torque_nm * request.tool_wear_min
    )

    temperature_ratio = (
        request.process_temperature_k / request.air_temperature_k
    )

    torque_speed_ratio = (
        request.torque_nm / request.rotational_speed_rpm
    )

    wear_power_interaction = (
        request.tool_wear_min * power
    )

    return pd.DataFrame({
        "Type": [request.machine_type],
        "Air temperature [K]": [request.air_temperature_k],
        "Process temperature [K]": [request.process_temperature_k],
        "Rotational speed [rpm]": [request.rotational_speed_rpm],
        "Torque [Nm]": [request.torque_nm],
        "Tool wear [min]": [request.tool_wear_min],
        "temperature_difference": [temperature_difference],
        "Power": [power],
        "torque_wear_stress": [torque_wear_stress],
        "temperature_ratio": [temperature_ratio],
        "torque_speed_ratio": [torque_speed_ratio],
        "wear_power_interaction": [wear_power_interaction]
    })