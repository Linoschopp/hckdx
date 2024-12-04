import json
from pathlib import Path
from flask import Flask, request

PASSWORD = "hi"
DEVICES_STORAGE_LOCATION = "devices.txt"


def load(devices_storage_location):
    if Path(devices_storage_location).exists():
        with open(devices_storage_location, "r") as file:
            return set(json.load(file))
    else:
        return set()


app = Flask(__name__)
devices = load(DEVICES_STORAGE_LOCATION)


def save(devices):
    with open(DEVICES_STORAGE_LOCATION, "w") as file:
        json.dump(list(devices), file)


@app.get("/requested")
def requested():
    device = request.headers.get("Device")
    return str(device in devices)


@app.post("/request")
def set_requested():
    if not request.headers.get("Password") == PASSWORD:
        return "Forbidden", 403
    device = request.headers.get("Device")
    devices.add(device)
    return "Okay"


@app.post("/deactivate")
def deactivate():
    if not request.headers.get("Password") == PASSWORD:
        return "Forbidden", 403
    device = request.headers.get("Device")
    try:
    	devices.remove(device)
    except KeyError:
        pass
    return "Okay"
    


if __name__ == '__main__':
    print(f"Admin-Passwort: {PASSWORD}")
    app.run(debug=True)
