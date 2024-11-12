from queue import Queue


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
    def __init__(self):
        raise NotImplementedError


class Device:
    def __init__(self, hostname, commands=None):
        if commands is None:
            commands = Queue()
        self.hostname = hostname
        self.commands = commands

    def put(self, command: Command):
        self.commands.put(command)

    def get(self):
        return self.commands.get()

    def task_done(self):
        self.commands.task_done()


def get_registered_devices() -> list[Device]:
    raise NotImplementedError


def get_active_mode() -> Mode:
    raise NotImplementedError


def get_active_devices() -> list[Device]:
    raise NotImplementedError

def get_device(device_hostname):
    for device in get_registered_devices():
        if device.hostname == device_hostname:
            return device

def put_host(device_hostname, command: Command):
    get_device(device_hostname).put(command)