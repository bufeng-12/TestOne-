import unittest
from unittest.mock import patch
from device import Device, Server, Storage


class TestDevice(unittest.TestCase):
    def setUp(self):
        self.ip = '192.168.1.100'
        self.protocol = 'ssh'
        self.username = 'admin'
        self.password = 'password'

    def test_device_connect(self):
        device = Device(self.ip, self.protocol, self.username, self.password)
        with patch('builtins.print') as mock_print:
            device.connect()
            mock_print.assert_called_once_with(f"Connecting to {self.ip} using {self.protocol}")


class TestServer(unittest.TestCase):
    def setUp(self):
        self.ip = '192.168.1.101'
        self.protocol = 'ssh'
        self.username = 'admin'
        self.password = 'password'

    def test_server_run_command(self):
        server = Server(self.ip, self.protocol, self.username, self.password)
        command = 'ls -l'
        with patch('builtins.print') as mock_print:
            server.run_command(command)
            mock_print.assert_called_once_with(f"Running command {command} on server {self.ip}")


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.ip = '192.168.1.102'
        self.protocol = 'ssh'
        self.username = 'admin'
        self.password = 'password'

    def test_storage_read_data(self):
        storage = Storage(self.ip, self.protocol, self.username, self.password)
        with patch('builtins.print') as mock_print:
            storage.read_data()
            mock_print.assert_called_once_with(f"Reading data from storage {self.ip}")


if __name__ == '__main__':
    unittest.main()
    