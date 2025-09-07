import random

class Simulator:
    def __init__(self, topo):
        self.topo = topo

    def run(self):
        logs = []
        for dev in self.topo.devices.values():
            for linked_hostname in dev.links:
                if random.random() > 0.1:
                    logs.append(f"Ping from {dev.hostname} to {linked_hostname} SUCCESS")
                else:
                    logs.append(f"Ping from {dev.hostname} to {linked_hostname} FAILED")
        return logs
