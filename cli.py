import json
import networkx as nx
import matplotlib.pyplot as plt

from .models import Device
from .topology import Topology
from .validator import Analyser
from .simulator import Simulator

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def generate_graph_image(topo, filename="topology_graph.png"):
    G = nx.Graph()
    for hostname, dev in topo.devices.items():
        G.add_node(hostname, dev_type=dev.dev_type)
    for hostname, dev in topo.devices.items():
        for linked in dev.links:
            G.add_edge(hostname, linked)

    color_map = {
        "PC": "lightblue",
        "Server": "orange",
        "Switch": "green",
        "Router": "red"
    }
    node_colors = [color_map.get(topo.devices[n].dev_type, "gray") for n in G.nodes]

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=10)
    plt.title("Network Topology Graph")
    plt.savefig(filename)
    plt.close()

def main():
    print("Welcome to Ring Topology Network Simulator")

    try:
        pc_count = int(input("Enter number of PCs: "))
        server_count = int(input("Enter number of Servers: "))
        switch_count = int(input("Enter number of Switches: "))
        router_count = int(input("Enter number of Routers: "))
    except ValueError:
        print("Please enter valid integer numbers.")
        return

    topo = Topology()

    # Add PCs and Servers first
    for i in range(1, pc_count + 1):
        dev = Device(f"PC{i}", "PC")
        topo.add_device(dev)

    for i in range(1, server_count + 1):
        dev = Device(f"Server{i}", "Server")
        topo.add_device(dev)

    # Add routers and switches (ring devices)
    ring_devices = []

    for i in range(1, router_count + 1):
        dev = Device(f"Router{i}", "Router")
        topo.add_device(dev)
        ring_devices.append(dev.hostname)

    for i in range(1, switch_count + 1):
        dev = Device(f"Switch{i}", "Switch")
        topo.add_device(dev)
        ring_devices.append(dev.hostname)

    # Create ring among routers and switches
    n = len(ring_devices)
    if n < 3:
        print("Warning: Ring topology requires at least 3 devices in the ring (routers + switches).")
    else:
        for i in range(n):
            current_dev = ring_devices[i]
            next_dev = ring_devices[(i + 1) % n]
            topo.add_link(current_dev, next_dev)

    # Connect servers and PCs to switches in round-robin
    switch_names = [f"Switch{i}" for i in range(1, switch_count + 1)]
    if not switch_names and (server_count > 0 or pc_count > 0):
        print("No switches to connect servers or PCs to. They will be isolated.")

    for i in range(1, server_count + 1):
        dev_name = f"Server{i}"
        if switch_names:
            switch_to_connect = switch_names[(i - 1) % len(switch_names)]
            topo.add_link(dev_name, switch_to_connect)

    for i in range(1, pc_count + 1):
        dev_name = f"PC{i}"
        if switch_names:
            switch_to_connect = switch_names[(i - 1) % len(switch_names)]
            topo.add_link(dev_name, switch_to_connect)

    # Show topology
    print("\nTopology Created:")
    for hostname, dev in topo.devices.items():
        print(f"{hostname} ({dev.dev_type}) linked to: {dev.links}")

    # Validate topology
    analyser = Analyser(topo)
    results = analyser.run()

    print("\nValidation Results:")
    if results["issues"]:
        for issue in results["issues"]:
            print(f" - {issue}")
    else:
        print("No issues found.")
    print(f"Total devices: {results['device_count']}")

    # Run simulation
    simulator = Simulator(topo)
    logs = simulator.run()

    print("\nSimulation Logs:")
    for log in logs:
        print(log)

    # Save JSON outputs
    save_json("report.json", results)
    save_json("sim_log.json", logs)

    # Generate and save graph image
    generate_graph_image(topo)
    print("\nOutputs saved:")
    print(" - report.json (validation results)")
    print(" - sim_log.json (simulation logs)")
    print(" - topology_graph.png (topology graph image)")

if __name__ == "__main__":
    main()
