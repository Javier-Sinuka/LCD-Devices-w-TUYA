"""
    Instalar SQLAlquemy
    pip install sqlalchemy
"""
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, insert, select, create_engine, DateTime, Float
from sqlalchemy import ForeignKey,UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///database.db")
# session = Session(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
class TemporalPowerData(Base):
    __tablename__ = "temporal_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    value_current: Mapped[float] = mapped_column(Float)
    value_voltage: Mapped[float] = mapped_column(Float)
    value_power: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return (f"TemporalPowerData (id={self.id!r}, date={self.date!r}, value_current={self.value_current!r},"
                f"value_voltage={self.value_voltage!r}, value_power={self.value_power!r})")

class Devices(Base):
    __tablename__ = "devices"
    device_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('name'),)

    def __repr__(self) -> str:
        return (f"Devices (device_id={self.device_id!r}, name={self.name!r}")

class MeasuringDevices(Base):
    __tablename__ = "measuring_devices"
    measuring_id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.device_id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    value_current: Mapped[float] = mapped_column(Float)
    value_voltage: Mapped[float] = mapped_column(Float)
    value_power: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return (f"Measuring Device (device_id={self.device_id!r}, date={self.date!r}, value_current={self.value_current!r},"
                f"value_voltage={self.value_voltage!r}, value_power={self.value_power!r})")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()