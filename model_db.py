"""
    Instalar SQLAlquemy
    pip install sqlalchemy
"""
from datetime import datetime

from sqlalchemy import CHAR, Table, Column, Integer, String, insert, select, create_engine, DateTime, Float, JSON
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

class Devices(Base):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    device_id: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('name','device_id'))

    def __repr__(self) -> str:
        return (f"id={self.id}, name={self.name!r}, device_id={self.device_id!r}")

class Attributes(Base):
    __tablename__ = "attributes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_attribute: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)
    data_type: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('name_attribute'))

    def __repr__(self) -> str:
        return (f"id={self.id}, name_attribute={self.name_attribute!r}, unit={self.unit!r}, data_type={self.data_type!r}")

class Values(Base):
    __tablename__ = "values"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    attribute_id: Mapped[str] = mapped_column(ForeignKey("attributes.id"))
    value: Mapped[CHAR] = mapped_column(CHAR)
    timestamp: Mapped[DateTime] = mapped_column(DateTime)

    def __repr__(self):
        return (f"id={self.id}, device_id={self.device_id!r}, attribute_id={self.attribute_id!r}, value={self.value!r}, timestamp={self.timestamp!r}")

# class EventTable(Base):
#     __tablename__ = "event_table"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
#     date: Mapped[datetime] = mapped_column(DateTime)
#     event: Mapped[JSON] = mapped_column(JSON)

    def __repr__(self) -> str:
        return (f"Event (device_id={self.id!r}, date={self.date!r}, event={self.event!r})")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()