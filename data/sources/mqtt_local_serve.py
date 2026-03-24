import csv
import time
import json
import paho.mqtt.client as mqtt

# --- Configuration ---
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/mean_data"
FILE_PATH = "data.csv"  # Ensure this matches your filename
INTERVAL = 0.5  # Seconds between each publication


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully to Mosquitto broker.")
    else:
        print(f"Connection failed with code {rc}")


def run_publisher():
    # Initialize MQTT Client
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()

        with open(FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            # Using DictReader handles the "Time" and "mean" headers automatically
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Construct the payload (sending as JSON is best practice)
                payload = json.dumps({
                    "timestamp": row["Time"],
                    "value": int(row["mean"])
                })

                # Publish to topic
                client.publish(TOPIC, payload)
                print(f"Published: {payload}")

                time.sleep(INTERVAL)

    except FileNotFoundError:
        print(f"Error: {FILE_PATH} not found. Please check the path.")
    except KeyboardInterrupt:
        print("\nStopping the publisher...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run_publisher()