from datetime import datetime

from sqlalchemy import CHAR, String, create_engine, DateTime
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine("sqlite:///database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Devices(Base):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    unique_device_id: Mapped[str] = mapped_column(String)
    manufacturer: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('name'),)

    def __repr__(self) -> str:
        return (f"id={self.id}, name={self.name!r}, device_id={self.unique_device_id!r}, manufacturer={self.manufacturer!r}")

class Attributes(Base):
    __tablename__ = "attributes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)
    data_type: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('name'),)

    def __repr__(self) -> str:
        return (f"id={self.id}, name={self.name!r}, unit={self.unit!r}, data_type={self.data_type!r}")

class Values(Base):
    __tablename__ = "values"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"))
    value: Mapped[CHAR] = mapped_column(CHAR)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return (f"id={self.id}, device_id={self.device_id!r}, attribute_id={self.attribute_id!r}, value={self.value!r}, timestamp={self.timestamp!r}")

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

