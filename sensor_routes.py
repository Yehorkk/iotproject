from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import (
    Sensor,
    UserIoTLink,
    SensorData,
    Setting,
    Alert,
    IoTSystem,
)
from auth_utils import get_db, get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/api/v1")


@router.post("/data")
def receive_data(
    iot_system_name: str,
    iot_system_password: str,
    timestamp: datetime,
    sensor_data: list[dict],
    db: Session = Depends(get_db),
):
    system = db.query(IoTSystem).filter(IoTSystem.name == iot_system_name).first()
    if not system or not verify_password(iot_system_password, system.password_hash):
        raise HTTPException(status_code=401, detail="Invalid IoT system")

    for entry in sensor_data:
        serial = entry["sensor_serial_number"]
        sensor = db.query(Sensor).filter(Sensor.serial_number == serial).first()
        if not sensor:
            sensor = Sensor(
                serial_number=serial,
                type=entry["type"],
                location=entry.get("location"),
                iot_system_id=system.id,
            )
            db.add(sensor)
            db.commit()
            db.refresh(sensor)
        data = SensorData(
            sensor_id=sensor.id,
            value=entry["value"],
            timestamp=timestamp,
        )
        db.add(data)
        # check settings
        setting = (
            db.query(Setting)
            .filter(
                Setting.iot_system_id == system.id,
                Setting.sensor_type == sensor.type,
            )
            .first()
        )
        if setting:
            if (
                (setting.min_value is not None and data.value < setting.min_value)
                or (
                    setting.max_value is not None
                    and data.value > setting.max_value
                )
            ):
                alert = Alert(
                    iot_system_id=system.id,
                    sensor_id=sensor.id,
                    message=f"{sensor.type} out of bounds: {data.value}",
                    timestamp=timestamp,
                )
                db.add(alert)
    db.commit()
    return {"message": "Data processed"}


@router.get("/alerts")
def get_alerts(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    alerts = (
        db.query(Alert)
        .join(IoTSystem, Alert.iot_system_id == IoTSystem.id)
        .join(UserIoTLink, UserIoTLink.iot_system_id == IoTSystem.id)
        .filter(UserIoTLink.user_id == current_user.id)
        .all()
    )
    return alerts


@router.post("/settings")
def set_setting(
    sensor_type: str,
    min_value: float | None = None,
    max_value: float | None = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    link = db.query(UserIoTLink).filter(UserIoTLink.user_id == current_user.id).first()
    if not link:
        raise HTTPException(status_code=400, detail="User has no system")
    setting = (
        db.query(Setting)
        .filter(
            Setting.iot_system_id == link.iot_system_id,
            Setting.sensor_type == sensor_type,
        )
        .first()
    )
    if not setting:
        setting = Setting(
            iot_system_id=link.iot_system_id,
            sensor_type=sensor_type,
            min_value=min_value,
            max_value=max_value,
        )
        db.add(setting)
    else:
        setting.min_value = min_value
        setting.max_value = max_value
    db.commit()
    db.refresh(setting)
    return setting


@router.get("/settings")
def get_settings(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    link = db.query(UserIoTLink).filter(UserIoTLink.user_id == current_user.id).first()
    if not link:
        raise HTTPException(status_code=400, detail="User has no system")
    settings = db.query(Setting).filter(Setting.iot_system_id == link.iot_system_id).all()
    return settings
