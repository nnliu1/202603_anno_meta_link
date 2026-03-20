import json
import os

import panel as pn
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
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

# --- 1. Setup Paths correctly ---
# Assuming PROJECT_DIR is already a Path object from our previous step
# If SCHEMA_PATH is "schema" and LINKML_NAME is "sensor.yaml"
full_schema_path = PROJECT_DIR / SCHEMA_PATH / LINKML_NAME

# --- 2. Get Description from linkML ---
view = SchemaView(full_schema_path)
cls_desc = view.get_class("SensorPayload").description
print(f"Class Description: {cls_desc}")

# --- 3. Initialize empty DataFrame ---
df = pd.DataFrame(columns=['time', 'power', 'soc', 'ctrl_mode'])

# --- 4. Define the UI Components ---
title = pn.pane.Markdown(f"# BESS Monitor\n**Schema Info:** {cls_desc}")

gauge = pn.indicators.Gauge(
    name='Active Power',
    value=0,
    bounds=(-2400, 2400),
    format='{value} W',
    sizing_mode='stretch_both'
)

# Set heights here once to keep things uniform
PLOT_HEIGHT = 300

# Initialize Power Plot (to go next to the Gauge)
power_plot_pane = pn.pane.HoloViews(
    hv.Curve(df, kdims='time', vdims='power').opts(
        title="Active Power (W)",
        color="blue",
        responsive=True,
        height=PLOT_HEIGHT # Matches Gauge visual height better
    ),
    sizing_mode='stretch_both'
)

soc_plot_pane = pn.pane.HoloViews(
    hv.Curve(df, kdims='time', vdims='soc').opts(
        title="SoC %",
        color="green",
        responsive=True,
        height=PLOT_HEIGHT
    ),
    sizing_mode='stretch_width'
)

ctrl_plot_pane = pn.pane.HoloViews(
    hv.Curve(df, kdims='time', vdims='ctrl_mode').opts(
        title="Control Mode",
        color="purple",
        responsive=True,
        height=PLOT_HEIGHT
    ),
    sizing_mode='stretch_width'
)

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
        power = data_obj.fields.activepower
        soc = data_obj.fields.soc
        ctrl_mode = data_obj.fields.ctrlmode
        ts = datetime.fromtimestamp(data_obj.time / 1e9)
        bess_id = data_obj.tags.BESS_id

        print(f"Validated Data from BESS {bess_id}: Power={power}, SoC={soc}%, Ctrl Mode={ctrl_mode}")


        # 4. Update Gauge UI
        gauge.value = power
        title.object = f"# Monitor BESS_ID: {bess_id}"  # Dynamic title

        # 5. Update Pandas DataFrame for the Plot
        new_entry = pd.DataFrame([{
            'time': ts,
            'power': power,
            'soc': soc,
            'ctrl_mode': ctrl_mode
        }])
        df = pd.concat([df, new_entry]).tail(1200)

        # 6. Refresh SoC Plot (Line)
        soc_plot_pane.object = hv.Curve(df, 'time', 'soc').opts(
            title=f"Real-time SoC - {bess_id}",
            color="green",
            ylabel="SoC %",
            responsive=True
        )

        # Only apply interpolation if we have at least 2 points to "step" between
        if len(df) > 1:
            # Safe to use interpolation now
            ctrl_plot_pane.object = hv.Curve(df, 'time', 'ctrl_mode').opts(
                title="Control Mode State",
                color="purple",
                interpolation='steps-post',
                responsive=True,
                height=PLOT_HEIGHT
            )
        else:
            # Just a simple update for the first point
            ctrl_plot_pane.object = hv.Curve(df, 'time', 'ctrl_mode').opts(
                responsive=True, height=PLOT_HEIGHT
            )
        # 8. Refresh Power Plot (Line)
        power_plot_pane.object = hv.Curve(df, 'time', 'power').opts(
            title=f"Power Trend - {bess_id}",
            color="blue",
            ylabel="Watts",
            responsive=True
        )

    except Exception as e:
        print(f"Data Validation Error: {e}")

client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message


def start_mqtt():
    client.connect(MQTT_BROKER, MQTT_PORT)  # Public test broker
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()


# Run MQTT in a background thread so it doesn't block the UI
thread = threading.Thread(target=start_mqtt, daemon=True)
thread.start()

# --- LAYOUT ---

# Top Row: Gauge on the left, Power Plot on the right
top_row = pn.Row(
    gauge,
    power_plot_pane,
    height=PLOT_HEIGHT + 50,
    sizing_mode='stretch_width'
)

# Main Dashboard: Vertical stack
dashboard = pn.Column(
    title,
    top_row,                       # Gauge + Power Plot
    pn.Spacer(height=20),
    soc_plot_pane,                 # SoC below
    pn.Spacer(height=10),
    ctrl_plot_pane,                # Ctrl Mode at the bottom
    width=1000,                    # Increased width for the side-by-side layout
    sizing_mode='stretch_width'
)

# Optional: Set fixed heights for consistency
soc_plot_pane.height = 300
ctrl_plot_pane.height = 300

dashboard.servable()
dashboard.show()  # This opens the dashboard in your browser