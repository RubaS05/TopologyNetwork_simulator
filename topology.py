from .models import Device

class Topology:
    def __init__(self):
        self.devices = {}

    def add_device(self, dev: Device):
        self.devices[dev.hostname] = dev

    def add_link(self, dev1: str, dev2: str):
        if dev1 in self.devices and dev2 in self.devices:
            if dev2 not in self.devices[dev1].links:
                self.devices[dev1].links.append(dev2)
            if dev1 not in self.devices[dev2].links:
                self.devices[dev2].links.append(dev1)

    def neighbors(self, hostname):
        nbs = []
        if hostname not in self.devices:
            return nbs
        for link in self.devices[hostname].links:
            nbs.append(link)
        return nbs

    def to_dict(self):
        return {k: {"dev_type": v.dev_type, "mgmt_ip": v.mgmt_ip, "interfaces": [i.name for i in v.interfaces], "links": v.links} 
                for k, v in self.devices.items()}
