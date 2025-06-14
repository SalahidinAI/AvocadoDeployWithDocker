from mysite.db.schema import PredictSchema
from mysite.db.models import Avocado
from fastapi import APIRouter, Depends
from mysite.db.database import SessionLocal
from sqlalchemy.orm import Session
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


avocado_router = APIRouter(prefix='/avocado', tags=['Avocado'])

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

model_path = BASE_DIR / 'avocado_ripeness.pkl'
scaler_path = BASE_DIR / 'scaler_avocado.pkl'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@avocado_router.post('/predict/')
async def predict(avocado: PredictSchema):
    avocado_dict = avocado.dict()
    color = avocado_dict.pop('color_category')

    color_0_or_1 = [
        1 if color == 'dark green' else 0,
        1 if color == 'green' else 0,
        1 if color == 'purple' else 0,
    ]

    features = list(avocado_dict.values()) + color_0_or_1
    scaled = scaler.transform([features])

    probability_array = model.predict_proba(scaled)[0]

    labels = ["hard", "pre-conditioned", "breaking", "firm-ripe", "ripe"]
    prediction = labels[probability_array.argmax()]
    return {
        'predicted_ripeness': prediction,
        'probabilities': {labels[i]: round(float(probability_array[i]), 2) for i in range(5)}
    }


@avocado_router.post('/avocado_create/')
async def avocado_create(avocado: PredictSchema, db: Session = Depends(get_db)):
    avocado_dict = avocado.dict()

    avocado_color = avocado_dict.pop('color_category')

    color_0_or_1 = [
        1 if avocado_color == 'dark green' else 0,
        1 if avocado_color == 'green' else 0,
        1 if avocado_color == 'purple' else 0,
    ]

    features = list(avocado_dict.values()) + color_0_or_1
    scaled = scaler.transform([features])
    prediction = model.predict(scaled)[0]
    probability = float(model.predict_proba(scaled)[0][1]) * 100

    new_avocado = Avocado(
        firmness=avocado.firmness,
        hue=avocado.hue,
        saturation=avocado.saturation,
        brightness=avocado.brightness,
        color_category=avocado.color_category,
        sound_db=avocado.sound_db,
        weight_g=avocado.weight_g,
        size_cm3=avocado.size_cm3,
        ripeness=prediction,
        probability=probability,
    )

    db.add(new_avocado)
    db.commit()
    db.refresh(new_avocado)

    return {'prediction': prediction, 'probability': f'{probability:.1f}%'}

