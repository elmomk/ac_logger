import os
import time
import random
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration from environment variables with defaults
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/metrics/temperature")
SEND_INTERVAL = int(os.getenv("SEND_INTERVAL", "5"))  # seconds

# Temperature simulation parameters
MIN_TEMP = 18.0
MAX_TEMP = 25.0
TEMP_VARIATION = 0.5  # Maximum variation between readings


class TemperatureSimulator:
    def __init__(self, min_temp=MIN_TEMP, max_temp=MAX_TEMP):
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.current_temp = random.uniform(min_temp, max_temp)

    def get_next_reading(self):
        # Slightly vary the temperature
        variation = random.uniform(-TEMP_VARIATION, TEMP_VARIATION)
        self.current_temp = max(
            self.min_temp, min(self.max_temp, self.current_temp + variation)
        )
        return round(self.current_temp, 2)


def send_temperature_reading(temperature):
    """Send temperature reading to the backend."""
    payload = {"temperature": temperature}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"[{timestamp}] Sending temperature: {temperature}°C")

    try:
        response = requests.post(
            BACKEND_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        response.raise_for_status()
        logger.info(
            f"Successfully sent temperature data. Status: {response.status_code}"
        )
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send temperature data: {str(e)}")
        return False


def main():
    logger.info("Starting fake temperature sensor...")
    logger.info(f"Backend URL: {BACKEND_URL}")
    logger.info(f"Send interval: {SEND_INTERVAL} seconds")

    simulator = TemperatureSimulator()

    try:
        while True:
            temperature = simulator.get_next_reading()
            send_temperature_reading(temperature)
            time.sleep(SEND_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping fake temperature sensor...")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
