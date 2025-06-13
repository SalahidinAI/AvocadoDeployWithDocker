from sqlalchemy import Integer, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column
from mysite.db.database import Base


class Avocado(Base):
    __tablename__ = 'avocado'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firmness: Mapped[float] = mapped_column(DECIMAL(6, 1))
    hue: Mapped[int] = mapped_column(Integer)
    saturation: Mapped[int] = mapped_column(Integer)
    brightness: Mapped[int] = mapped_column(Integer)
    color_category: Mapped[str] = mapped_column(String)
    sound_db: Mapped[int] = mapped_column(Integer)
    weight_g: Mapped[int] = mapped_column(Integer)
    size_cm3: Mapped[int] = mapped_column(Integer)
    ripeness: Mapped[str] = mapped_column(String)
    probability: Mapped[float] = mapped_column(DECIMAL(4, 1))
