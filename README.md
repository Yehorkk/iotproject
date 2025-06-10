# IoT Energy Monitoring Server

Simple FastAPI application for receiving sensor data, generating alerts and managing settings.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Features

- User registration and login with JWT authentication
- Receive sensor data from IoT systems
- Store data and generate alerts when values are out of bounds
- Manage threshold settings for sensors
