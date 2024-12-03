import json
from pathlib import Path
from flask import Flask, request

PASSWORD = "hi"
DEVICES_STORAGE_LOCATION = "devices.txt"


def load(devices_storage_location):
    if Path(devices_storage_location).exists():
        with open(devices_storage_location, "r") as file:
            namelist = json.load(file)
            return dict(zip(namelist, map(lambda x: False, namelist)))
    else:
        return {}


app = Flask(__name__)
devices = load(DEVICES_STORAGE_LOCATION)


def save(devices):
    with open(DEVICES_STORAGE_LOCATION, "w") as file:
        json.dump(list(devices.keys()), file)


@app.post("/register")
def register():
    hostname = request.headers.get("Device")
    devices[hostname] = False
    save(devices)
    return "Okay"


@app.post("/delete")
def delete():
    if request.headers.get("Password") == PASSWORD:
        hostname = request.headers.get("Device")
        del devices[hostname]
        save(devices)
        return "Okay"
    return "Forbidden", 403


@app.get("/requested")
def requested():
    device = request.headers.get("Device")
    return str(devices.get(device))


@app.post("/request")
def set_requested():
    if request.headers.get("Password") == PASSWORD:
        if (device := request.headers.get("Device")) in devices:
            devices[device] = True
            print(devices)
            return "Okay"
    return "Forbidden", 403


@app.post("/deactivate")
def deactivate():
    if request.headers.get("Password") == PASSWORD:
        if (device := request.headers.get("Device")) in devices:
            devices[device] = False
            return "Okay"
    return "Forbidden", 403


if __name__ == '__main__':
    print(f"Admin-Passwort: {PASSWORD}")
    app.run(debug=True)
