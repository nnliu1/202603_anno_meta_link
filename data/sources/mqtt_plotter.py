import json
import os

import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from linkml_runtime.loaders import json_loader
# Note: You must generate 'datamodel.py' first using:
# uv run gen-python schema.yaml > datamodel.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2])) # needed for some operating systems

from models.fenecon_mea.datamodel import SensorPayload

# --- Configuration ---
MQTT_BROKER = "elab-cmvc001.server.elab2.kit.edu"  # Change to your broker IP if not local
MQTT_PORT = 10883
MQTT_TOPIC = "testing/fenecon/mea/130"
COLLECTION_DURATION = 640  # How long to listen (seconds)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ACQUISITION_PATH = "acquisitions"

# Global list to store incoming data
received_data = []


def on_message(client, userdata, msg):
    try:
        # 1. Parse raw byte-string to JSON dict
        raw_payload = json.loads(msg.payload.decode())

        # 2. Validate and Load into LinkML Class
        # This will raise an error if the JSON doesn't match your schema
        data_obj = json_loader.loads(raw_payload, target_class=SensorPayload)

        # 3. Extract specific fields for plotting
        # LinkML objects allow dot-notation access
        reading = {
            "timestamp": datetime.fromtimestamp(data_obj.time / 1e9),  # Convert nanos to datetime
            "activepower": data_obj.fields.activepower,
            "soc": data_obj.fields.soc,
            "BESS_id": data_obj.tags.BESS_id
        }

        received_data.append(reading)
        print(f"Validated Data from BESS {reading['BESS_id']}: Power={reading['activepower']}, SoC={reading['soc']}%")

    except Exception as e:
        print(f"Invalid Payload: {e}")


def plot_data():
    if not received_data:
        print("No data collected.")
        return

    df = pd.DataFrame(received_data)

    # Create two subplots: one for Power, one for SoC
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot Active Power
    ax1.plot(df['timestamp'], df['activepower'], color='blue', label='Active Power (W)')
    ax1.set_ylabel('Power (W)')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Plot State of Charge (SoC)
    ax2.plot(df['timestamp'], df['soc'], color='green', label='SoC (%)')
    ax2.set_ylabel('SoC (%)')
    ax2.set_ylim(0, 105)  # SoC is always 0-100
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.xlabel('Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def serialise_data():
    if not received_data:
        print("No data received.")
        return

    df = pd.DataFrame(received_data)

    # 1. Your Metadata
    metadata = {
        "project": "MQTT Plotter",
        "topic": MQTT_TOPIC.replace("/", "_"),
        "duration": COLLECTION_DURATION,
        "version": "v11",
        "status": "raw"
    }
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    filename = f"{metadata['project']}_{timestamp}_{metadata['duration']:04}_sec_{metadata['topic']}_{metadata['version']}_{metadata['status']}.csv"
    filepath = SCRIPT_DIR / Path(ACQUISITION_PATH) / filename
    print(f"Saving data to {filepath}...")

    df.to_csv(filepath, index=False)

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

    # Serialising
    serialise_data()

    # Plotting
    plot_data()


if __name__ == "__main__":
    main()