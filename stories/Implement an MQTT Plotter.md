## Working with LinkML and uv
To use LinkML to validate your MQTT data or generate Python classes, add the generator to your uv environment:

Bash
```
uv add linkml
```

### 1. Generate Python Data Classes
You can automatically turn that YAML into a Python script with built-in validation:

Bash
```
uv run gen-python schema.yaml > datamodel.py
```

### 2. Validate a JSON file
If you save your payload to a file named data.json, you can check it against the schema:

Bash
```
uv run linkml-validate -s schema.yaml data.json
```

To integrate LinkML validation into your MQTT listener, we will use the linkml-runtime to parse and validate the incoming JSON against your schema. This ensures that if a sensor sends a malformed payload (e.g., missing the BESS_id), the script catches it before it breaks your plot.
