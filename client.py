import http.client
import os
import urllib.request
import socket

os.putenv("client", "true")
import management

# URL = "http://linoschopp.ddns.net:9000"
URL = "http://localhost:5000"
HOSTNAME = socket.gethostname()


def active():
    request = urllib.request.Request(f"{URL}/active", headers={"Device": HOSTNAME.encode()}, method="GET")
    with urllib.request.urlopen(request) as response:
        response: http.client.HTTPResponse
        is_active = response.read().decode() == "True"
    return is_active

def register():
    request = urllib.request.Request(f"{URL}/register", data=HOSTNAME.encode(), method="POST")
    with urllib.request.urlopen(request) as response:
        response: http.client.HTTPResponse
        token = response.read().decode()
    return token

def getcmd(token):
    request = urllib.request.Request(f"{URL}/commands/get", headers={"Token": token})
    print("Requesting command...")
    with urllib.request.urlopen(request) as response:
        response: http.client.HTTPResponse
        data = response.read().decode()
        print(data)
        cmd = management.Command.import_from_string(data)
        print(f"{cmd.name}: {', '.join(cmd.args)}")

if __name__ == "__main__":
    print(f"Hostname: {HOSTNAME}")
    token = register()
    while active():
        getcmd(token)
