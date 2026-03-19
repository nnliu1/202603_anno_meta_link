import json
import os

import panel as pn
import paho.mqtt.client as mqtt
import pandas as pd
import holoviews as hv
from holoviews import streams
import threading

from datetime import datetime

from linkml_runtime.utils.schemaview import SchemaView
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
MQTT_TOPIC = "testing/fenecon/mea/132"
PROJECT_DIR = Path(__file__).resolve().parents[2]
ACQUISITION_PATH = "acquisitions"
SCHEMA_PATH = "schemas"
LINKML_NAME = "fenecon_mea.yaml"

pn.extension(design='material')

# --- DATA STORAGE ---
data = {'time': [], 'value': []}
df = pd.DataFrame(data)
view = SchemaView(PROJECT_DIR / SCHEMA_PATH / LINKML_NAME)
cls_desc = view.get_class("SensorPayload").description
print(f"Class Description: {cls_desc}")

# --- PANEL COMPONENTS ---
title = pn.pane.Markdown("# Live MQTT Monitor")
gauge = pn.indicators.Gauge(name='Current Value', value=0, bounds=(-2000, 2000), format='{value}')
plot_pane = pn.pane.HoloViews(hv.Curve(df).opts(width=600, color='teal', responsive=True))


# --- MQTT SETUP ---
def on_message(client, userdata, message):
    global df
    try:
        # 1. Parse raw byte-string to JSON dict
        raw_payload = json.loads(message.payload.decode())

        # 2. Validate and Load into LinkML Class
        # target_class=SensorPayload ensures schema compliance
        data_obj = json_loader.loads(raw_payload, target_class=SensorPayload)

        # 3. Extract specific fields (using dot-notation from LinkML)
        # Assuming you want to plot 'activepower' for this example
        val = data_obj.fields.activepower
        ts = datetime.fromtimestamp(data_obj.time / 1e9)
        bess_id = data_obj.tags.BESS_id
        soc = data_obj.fields.soc
        print(f"Validated Data from BESS {bess_id}: Power={val}, SoC={soc}%")


        # 4. Update Gauge UI
        gauge.value = val
        title.object = f"# Monitor BESS_ID: {bess_id}"  # Dynamic title

        # 5. Update Pandas DataFrame for the Plot
        new_entry = {'time': ts, 'value': soc}
        df = pd.concat([df, pd.DataFrame([new_entry])]).tail(200)

        # 6. Refresh Plot Pane
        plot_pane.object = hv.Curve(df, 'time', 'value').opts(
            title=f"Real-time SoC - {bess_id}",
            shared_axes=False,
            responsive=True
        )

    except Exception as e:
        print(f"Data Validation Error: {e}")

client = mqtt.Client()
client.on_message = on_message


def start_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT)  # Public test broker
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()


# Run MQTT in a background thread so it doesn't block the UI
thread = threading.Thread(target=start_mqtt, daemon=True)
thread.start()

# --- LAYOUT ---
dashboard = pn.Column(
    title,
    pn.Row(gauge, plot_pane),
)

dashboard.servable()

dashboard.show()  # This opens the dashboard in your browser