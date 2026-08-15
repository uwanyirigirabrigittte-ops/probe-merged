import json
import logging
import os
import sys
import time

from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from probe.services.sensor_reading import SensorReadingService
from probe.schemas.sensor_reading import SensorReadingCreate

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("mqtt-subscriber")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "probe/telemetry/+")
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker %s:%d (rc=%d)", MQTT_BROKER, MQTT_PORT, rc)
        client.subscribe(MQTT_TOPIC, qos=1)
        logger.info("Subscribed to topic: %s", MQTT_TOPIC)
    else:
        logger.error("MQTT connection failed with code %d", rc)


def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT broker (rc=%d). Reconnecting in 5s...", rc)
    time.sleep(5)
    try:
        client.reconnect()
    except Exception as e:
        logger.error("Reconnect failed: %s", e)


def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        logger.debug("Received on %s: %s", msg.topic, payload_str)

        data = json.loads(payload_str)
        device_id = data.get("device_id")
        battery_id = data.get("battery_id")
        temp = float(data.get("temp", 0.0))
        current = float(data.get("current", 0.0))
        v_rest = float(data.get("v_rest", 0.0))
        v_load = float(data.get("v_load", 0.0))

        if not device_id or not battery_id:
            logger.warning("Missing device_id or battery_id in payload from topic %s", msg.topic)
            return

        db: Session = SessionLocal()
        try:
            reading_data = SensorReadingCreate(
                device_id=device_id,
                battery_id=battery_id,
                temp=temp,
                current=current,
                v_rest=v_rest,
                v_load=v_load,
            )
            reading = SensorReadingService.create_sensor_reading(db, reading_data)
            logger.info(
                "Created reading %s | slot=%s | SoH=%.1f%% | category=%s | status=%s",
                reading.sensor_reading_id,
                msg.topic,
                reading.state_of_health,
                reading.category,
                reading.status,
            )
        except Exception as e:
            logger.error("Failed to create sensor reading from topic %s: %s", msg.topic, e)
        finally:
            db.close()

    except json.JSONDecodeError:
        logger.error("Invalid JSON payload on %s: %s", msg.topic, msg.payload.decode("utf-8", errors="replace"))
    except Exception as e:
        logger.error("Unexpected error processing message on %s: %s", msg.topic, e)


def main():
    client = mqtt.Client(client_id="probe-backend-subscriber", clean_session=False)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    logger.info("Connecting to HiveMQ broker %s:%d", MQTT_BROKER, MQTT_PORT)
    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

    logger.info("Starting MQTT subscriber loop...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("MQTT subscriber stopped by user")
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        logger.error("MQTT subscriber crashed: %s", e)
        client.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    main()
