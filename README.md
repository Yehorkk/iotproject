# IoT Energy Monitoring Server

Simple FastAPI application for receiving sensor data, generating alerts and managing settings.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Usage

1. Register a user via `/api/v1/register`.
2. Login at `/api/v1/login` to obtain a JWT token.
3. Create an IoT system using `/api/v1/iot_systems` with the token.
4. Run `python iot_sensor_simulator.py` to post demo sensor data.

## Features

- User registration and login with JWT authentication
- Receive sensor data from IoT systems
- Store data and generate alerts when values are out of bounds
- Manage threshold settings for sensors
