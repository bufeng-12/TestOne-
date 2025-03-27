class Device:
    def __init__(self, ip, protocol, username, password):
        self.ip = ip
        self.protocol = protocol
        self.username = username
        self.password = password

    def connect(self):
        print(f"Connecting to {self.ip} using {self.protocol}")


class Server(Device):
    def __init__(self, ip, protocol, username, password):
        super().__init__(ip, protocol, username, password)

    def run_command(self, command):
        print(f"Running command {command} on server {self.ip}")


class Storage(Device):
    def __init__(self, ip, protocol, username, password):
        super().__init__(ip, protocol, username, password)

    def read_data(self):
        print(f"Reading data from storage {self.ip}")
    