import os
from operator import attrgetter
from queue import Queue

if os.getenv("client") == "true":
    import time
    import pyautogui
    client = True
else:
    client = False


class Mode:
    def __init__(self, *, single: bool = None, multi: bool = None, string_repr: str = None):
        self.string_repr: str
        if single == True or multi == False:
            self.string_repr = "single"
        elif single == False or multi == True:
            self.string_repr = "multi"
        elif string_repr in ("single", "multi"):
            self.string_repr = string_repr
        else:
            raise TypeError("Mode() must have one argument.")

    def __str__(self):
        return self.string_repr


class Command:
    def __init__(self, name: str, args: list):
        self.name = name
        self.args = args
    def execute(self):
        if not client:
            print("This method should only be used by clients.")
            return
        match self.name:
            case "SLEEP":
                d, = self.args
                time.sleep(d)




class Device:
    def __init__(self, hostname, commands=None):
        if commands is None:
            commands = Queue()
        self.hostname = hostname
        self.commands = commands
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
