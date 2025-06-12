import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/data"

payload = {
    "iot_system_name": "DemoSystem",
    "iot_system_password": "demo",
    "timestamp": datetime.utcnow().isoformat(),
    "sensor_data": [
        {
            "sensor_serial_number": "TEMP1",
            "type": "temperature",
            "location": "room1",
            "value": 25.3,
        }
    ],
}

response = requests.post(API_URL, json=payload)
print(response.status_code, response.json())
