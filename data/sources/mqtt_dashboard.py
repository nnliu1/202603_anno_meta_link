import panel as pn
import paho.mqtt.client as mqtt
import pandas as pd
import holoviews as hv
from holoviews import streams
import threading

pn.extension(design='material')

# --- DATA STORAGE ---
data = {'time': [], 'value': []}
df = pd.DataFrame(data)

# --- PANEL COMPONENTS ---
title = pn.pane.Markdown("# EDO Framework Live MQTT Monitor")
gauge = pn.indicators.Gauge(name='Current Value', value=0, bounds=(0, 100), format='{value}')
plot_pane = pn.pane.HoloViews(hv.Curve(df).opts(width=600, color='teal', responsive=True))


# --- MQTT SETUP ---
def on_message(client, userdata, message):
    global df
    val = float(message.payload.decode("utf-8"))

    # Update Gauge
    gauge.value = val

    # Update Plot Data
    new_entry = {'time': pd.Timestamp.now(), 'value': val}
    df = pd.concat([df, pd.DataFrame([new_entry])]).tail(20)  # Keep last 20 points

    # Refresh Plot
    plot_pane.object = hv.Curve(df, 'time', 'value').opts(title="Real-time Stream", shared_axes=False)


client = mqtt.Client()
client.on_message = on_message


def start_mqtt():
    client.connect("broker.hivemq.com", 1883)  # Public test broker
    client.subscribe("edo/framework/sensors")
    client.loop_forever()


# Run MQTT in a background thread so it doesn't block the UI
thread = threading.Thread(target=start_mqtt, daemon=True)
thread.start()

# --- LAYOUT ---
dashboard = pn.Column(
    title,
    pn.Row(gauge, plot_pane),
    servable=True
)

dashboard.show()  # This opens the dashboard in your browser