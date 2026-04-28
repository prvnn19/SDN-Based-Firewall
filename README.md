# SDN-Based-Firewall
A controller-based firewall using POX and Mininet to implement rule-based IP and Port filtering.
# SDN-Based Firewall (POX & Mininet)

Developed a controller-based firewall to dynamically manage network traffic by blocking or allowing packets based on security rules.

## 🚀 Project Features
- **IP Filtering**: Specifically blocks all traffic from `h1` (10.0.0.1) to `h3` (10.0.0.3).
- **Port Security**: Blocks incoming TCP traffic on **Port 8000** for host `h2`.
- **Dynamic Flow Entry**: Installs "Drop" rules directly into the switch with a 30s timeout to optimize performance.
- **Layer 2 Learning**: Includes basic MAC-learning logic for standard traffic forwarding.

## 🛠️ Tech Stack
- **Language**: Python 3
- **SDN Controller**: POX
- **Network Emulator**: Mininet
- **Protocol**: OpenFlow 1.0

## 📂 File Structure
- `firewall_controller.py`: The core firewall logic (place in `pox/ext/`).
- `topo.py`: Defines the 3-host, 1-switch topology.

## 🚦 How to Run
1. Move the controller script:
   `cp firewall_controller.py ~/pox/ext/`
2. Start the POX Controller:
   `./pox.py log.level --DEBUG openflow.of_01 ext.firewall_controller`
3. Launch the Network:
   `sudo python3 topo.py`

## 📊 Results
Successfully verified traffic blocking via Mininet CLI. Approximately **16-20% packet loss** observed during `pingall`, confirming that specific prohibited paths were successfully severed by the firewall.

---
**Author:** Praveen Naik (PES2UG24AM123)
