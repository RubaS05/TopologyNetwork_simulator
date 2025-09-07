class Device:
    def __init__(self, hostname, dev_type, mgmt_ip=None, interfaces=None):
        self.hostname = hostname
        self.dev_type = dev_type
        self.mgmt_ip = mgmt_ip
        self.interfaces = interfaces or []
        self.links = []

class Interface:
    def __init__(self, name, ip=None):
        self.name = name
        self.ip = ip
