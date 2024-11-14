import os
import re
from queue import Queue
from operator import attrgetter

if os.getenv("client") == "true":
    import time
    import pyautogui
    client = True
else:
    client = False


class Command:
    def __init__(self, name: str, args: list[str]):
        self.name = name
        self.args = args
    def execute(self):
        if not client:
            print("This method should only be used by clients.")
            return
        match self.name:
            case "SLEEP":
                d, = self.args
                time.sleep(int(d))
    def export_to_string(self):
        return self.name+":"+"\0".join(self.args)

    @classmethod
    def import_from_string(cls, string: str):
        return cls(string.split(":", 1)[0], string.split(":", 1)[1].split("\0"))


class Device:
    def __init__(self, hostname, commands=None):
        if commands is None:
            commands = Queue()
        self.hostname = hostname
        self.commands: Queue[Command] = commands
        self.active = False

    def put(self, command: Command):
        self.commands.put(command)

    def get(self):
        return self.commands.get()

    def task_done(self):
        self.commands.task_done()

class DeviceStorage:
    def __init__(self, devices=None):
        if devices is None:
            devices = []
        self.devices: list[Device] = devices

    def __iter__(self):
        return self.devices

    def get_device(self, device_hostname):
        for device in self:
            if device.hostname == device_hostname:
                return device

    def __getitem__(self, item):
        return self.get_device(item)

    def active(self):
        return list(map(attrgetter("active"), self.devices))

    @classmethod
    def load_devices(cls, floc):
        if not os.path.isfile(floc):
            return cls()
        with open(floc, "r") as f:
            device_names = filter(bool, f.read().split("\n"))
        devices = []
        for device_name in device_names:
            devices.append(Device(device_name))
        return DeviceStorage(devices)

    def save(self, floc):
        file_content = "\n".join(map(attrgetter("hostname"), self.devices))
        with open(floc, "w") as f:
            f.write(file_content)
