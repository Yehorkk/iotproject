from sqlalchemy import (Column, Integer, String, Float, ForeignKey, DateTime)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

DATABASE_URL = "sqlite:///./iot_system.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")

    systems = relationship("UserIoTLink", back_populates="user")

class IoTSystem(Base):
    __tablename__ = "iot_systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password_hash = Column(String)

    sensors = relationship("Sensor", back_populates="iot_system")
    settings = relationship("Setting", back_populates="iot_system")

class UserIoTLink(Base):
    __tablename__ = "user_iot_link"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    iot_system_id = Column(Integer, ForeignKey("iot_systems.id"))

    user = relationship("User", back_populates="systems")
    iot_system = relationship("IoTSystem")

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    type = Column(String)
    location = Column(String)
    iot_system_id = Column(Integer, ForeignKey("iot_systems.id"))

    iot_system = relationship("IoTSystem", back_populates="sensors")
    data = relationship("SensorData", back_populates="sensor")

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="data")

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    iot_system_id = Column(Integer, ForeignKey("iot_systems.id"))
    sensor_type = Column(String)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)

    iot_system = relationship("IoTSystem", back_populates="settings")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    iot_system_id = Column(Integer, ForeignKey("iot_systems.id"))
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)
