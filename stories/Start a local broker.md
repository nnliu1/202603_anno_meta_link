# Start a local broker

To start a broker, `mosquitto`must be already installed.

## Option A: Run as a background service (Recommended)
This ensures Mosquitto starts automatically when you log in and stays running in the background.
```bash
brew services start mosquitto
```

## Option B: Run manually in the foreground
Useful if you want to see the logs in real-time for debugging.
```bash
/opt/homebrew/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

## Configuration for Local Access
By default, newer versions of Mosquitto (2.0+) only allow local connections and require no authentication. However, if you run into connection issues with your Python script, you may need to edit the configuration file located at:
`/opt/homebrew/etc/mosquitto/mosquitto.conf`

To allow "anonymous" connections (no username/password) for local testing, ensure these lines exist in the config:

```Plaintext
listener 1883
allow_anonymous true
```

## Verify the Installation
Open a new Terminal window and "subscribe" to a test topic:

```Bash
mosquitto_sub -h localhost -t "test/topic"
```
Open a second Terminal window and "publish" a message:

```Bash
mosquitto_pub -h localhost -t "test/topic" -m "Hello from Mac"
```
If you see "Hello from Mac" appear in the first window, your broker is working perfectly.