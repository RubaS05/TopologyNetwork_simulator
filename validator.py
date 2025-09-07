class Analyser:
    def __init__(self, topo):
        self.topo = topo

    def run(self):
        issues = []
        for hostname, dev in self.topo.devices.items():
            if dev.dev_type.lower() == "router" and not dev.links:
                issues.append(f"{hostname} is isolated!")
            if dev.dev_type.lower() == "switch" and not dev.links:
                issues.append(f"{hostname} is isolated!")
        return {"issues": issues, "device_count": len(self.topo.devices)}
