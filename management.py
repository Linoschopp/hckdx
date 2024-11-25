import os
from queue import Queue
from operator import attrgetter

if os.getenv("client") == "true":
    import time
    import pyautogui
    import pynput
    keyboard = pynput.keyboard.Controller()
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
            case "BLANK":
                return
            case "TYPE":
                keyboard.type(*self.args)
            case "HOTKEY":
                *hold, tap = self.args
                for key in hold:
                    if key.startswith("COD:"):
                        keyboard.press(key[4:])
                    elif key.startswith("KEY:"):
                        keyboard.press(getattr(pynput.keyboard, key[4:]))
                if tap.startswith("COD:"):
                    keyboard.press(tap[4:])
                elif key.startswith("KEY:"):
                    keyboard.press(getattr(pynput.keyboard, tap[4:]))
                for key in hold:
                    if key.startswith("COD:"):
                        keyboard.release(key[4:])
                    elif key.startswith("KEY:"):
                        keyboard.release(getattr(pynput.keyboard, key[4:]))
                
                        
                        
                    

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
        self.state = "INACTIVE"

    def put(self, command: Command):
        self.commands.put(command)

    def get(self):
        cmd = self.commands.get()
        self.commands.task_done()
        return cmd

    def task_done(self):
        self.commands.task_done()

class DeviceStorage:
    def __init__(self, devices=None):
        if devices is None:
            devices = []
        self.devices: list[Device] = devices

    def __iter__(self):
        return iter(self.devices)

    def get_device(self, device_hostname):
        for device in self:
            if device.hostname == device_hostname:
                return device

    def __getitem__(self, item):
        return self.get_device(item)

    def requested(self):
        requested = []
        for dev in self.devices:
            if dev.active == "REQUESTED":
                requested.append(dev)
        return requested

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
