from fastapi import FastAPI
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point, WriteOptions
import os

app = FastAPI()

# InfluxDB configuration from environment variables
influxdb_host = os.environ.get("INFLUXDB_HOST", "http://localhost:8086")
influxdb_token = os.environ.get("INFLUXDB_TOKEN", "your_influxdb_token")
influxdb_org = os.environ.get("INFLUXDB_ORG", "your_organization_name")
influxdb_bucket = os.environ.get("INFLUXDB_BUCKET", "temperature_metrics")

client = InfluxDBClient(url=influxdb_host, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(
    write_options=WriteOptions(batch_size=1000, flush_interval=1000)
)


# Pydantic model for incoming data, expecting a "temperature" field
class TemperatureData(BaseModel):
    temperature: float


@app.post("/metrics/temperature")
async def receive_temperature(data: TemperatureData):
    """
    Receives temperature data from the ESP32 and writes it to InfluxDB.
    """
    # Create a data point with the measurement name and field
    point = Point("temperature_reading").field("value", data.temperature)

    # Write the data point to the database
    write_api.write(bucket=influxdb_bucket, record=point)

    return {"status": "success", "message": "Temperature data recorded."}


@app.get("/")
def home():
    return {"message": "Welcome to the temperature metrics backend!"}
