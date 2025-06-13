from pydantic import BaseModel


class PredictSchema(BaseModel):
    firmness: float
    hue: int
    saturation: int
    brightness: int
    color_category: str
    sound_db: int
    weight_g: int
    size_cm3: int

