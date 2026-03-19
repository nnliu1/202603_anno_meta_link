import json
import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from linkml_runtime.loaders import json_loader
# Note: You must generate 'datamodel.py' first using:
# uv run gen-python schema.yaml > datamodel.py
from datamodel import SensorPayload

# --- Configuration ---
MQTT_BROKER = "elab-cmvc001.server.elab2.kit.edu"  # Change to your broker IP if not local
MQTT_PORT = 10883
MQTT_TOPIC = "testing/fenecon/mea/130"
COLLECTION_DURATION = 200  # How long to listen (seconds)

# Global list to store incoming data
received_data = []


def on_message(client, userdata, msg):
    """Callback triggered when a message arrives."""
    try:
        payload = msg.payload.decode()
        # Expecting a simple numeric value or JSON string
        value = float(payload)

        reading = {
            "timestamp": datetime.now(),
            "value": value
        }
        received_data.append(reading)
        print(f"Received: {value} on {msg.topic}")
    except ValueError:
        print(f"Payload '{payload}' is not a number. Skipping.")


# --- Main Execution ---
def main():
    client = mqtt.Client()
    client.on_message = on_message

    print(f"Connecting to {MQTT_BROKER}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)

    # Start the network loop in a non-blocking background thread
    client.loop_start()

    print(f"Collecting data for {COLLECTION_DURATION} seconds...")
    time.sleep(COLLECTION_DURATION)

    # Stop the network loop
    client.loop_stop()
    client.disconnect()

    # --- Processing & Plotting ---
    if not received_data:
        print("No data received. Check your broker and topic.")
        return

    # Convert list to DataFrame
    df = pd.DataFrame(received_data)

    print("\nData Summary:")
    print(df.describe())

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['value'], marker='o', color='tab:blue', linestyle='-')

    plt.title(f"MQTT Data from {MQTT_TOPIC}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()