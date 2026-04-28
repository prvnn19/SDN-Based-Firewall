
---

# SDN-Based Stateful Firewall using POX and Mininet

## 📌 Project Overview
This project demonstrates the implementation of a **Software-Defined Networking (SDN) Firewall**. By utilizing the **POX Controller**, we decouple the control plane from the data plane, allowing for centralized management of network security policies. The firewall dynamically pushes flow rules to an **Open vSwitch (OVS)** to block or allow traffic based on IP addresses and TCP ports.

---

## 🖼️ Execution Proof

### 1. Controller Logs & Rule Enforcement
This screenshot shows the POX controller actively intercepting traffic and logging blocked attempts from h1 to h3 and TCP port violations.

![Controller Execution](logs_screenshot_1.jpg)

### 2. Mininet Topology & Testing
This screenshot shows the network topology initialization and the `pingall` results verifying the firewall's impact on network connectivity.

![Mininet Testing](logs_screenshot_2.jpg)

---

### Key Features
- **Dynamic Policy Enforcement**: Real-time packet inspection and rule installation.
- **Efficient Flow Management**: Uses `ofp_flow_mod` with idle timeouts to minimize controller-switch communication.
- **Layer 2 Learning**: Integrated MAC-to-port learning logic for standard traffic forwarding.
- **Custom Topology**: A specialized 3-host, 1-switch network environment.

---

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **SDN Controller:** POX (Eel)
* **Network Emulator:** Mininet
* **Southbound Protocol:** OpenFlow 1.0

---

## 🏗️ Architecture & Security Rules
The network consists of one switch (`s1`) and three hosts (`h1`, `h2`, `h3`).

| Rule Type | Source | Destination | Protocol/Port | Action |
| :--- | :--- | :--- | :--- | :--- |
| **IP Filter** | 10.0.0.1 (h1) | 10.0.0.3 (h3) | Any | **DROP** |
| **Port Filter** | Any | 10.0.0.2 (h2) | TCP Port 8000 | **DROP** |
| **Default** | Any | Any | Any | **ALLOW** (L2 Learning) |

---

## 📂 File Description
1.  **`firewall_controller.py`**: The core controller logic. It listens for `PacketIn` events, checks them against the security table, and sends `ofp_flow_mod` commands to the switch.
2.  **`topo.py`**: A Mininet script that automates the creation of the hosts, switch, and links, while connecting them to the remote POX controller.

---

## 🚀 Step-by-Step Tutorial

### 1. Environment Preparation
Ensure you have Mininet and POX installed. Place `firewall_controller.py` in the POX extension directory:
```bash
cp firewall_controller.py ~/pox/ext/
```

### 2. Start the Control Plane
Launch the POX controller with the firewall component:
```bash
cd ~/pox
./pox.py log.level --DEBUG openflow.of_01 ext.firewall_controller
```

### 3. Start the Data Plane
In a separate terminal, execute the topology script:
```bash
sudo python3 topo.py
```

### 4. Verification Testing
Once the `mininet>` CLI appears, run these tests:

* **Verify IP Block:**
    ```bash
    mininet> h1 ping h3
    ```
    *(Expected: Destination Host Unreachable / 100% Packet Loss)*

* **Verify Port Block:**
    On h2: `mininet> h2 iperf -s -p 8000 &`
    On h1: `mininet> h1 telnet 10.0.0.2 8000`
    *(Expected: Connection timed out/refused)*

* **Check Switch Flows:**
    ```bash
    mininet> dpctl dump-flows
    ```
    *(Expected: You will see "drop" actions for the blocked IP/Port pairs)*

---

## 📊 Performance Logic
To prevent the controller from being overwhelmed by a flood of blocked packets, the script installs a **hard-drop rule** on the switch hardware:
$$\text{Timeout} = 30s$$
This ensures that once a violation is detected, the switch handles the drop locally for the next 30 seconds without querying the controller.

---

## 📝 Author & Identity
* **Name:** Praveen Naik
* **Directory ID:** PES2UG24AM123
* **Academic Project:** SDN Security Systems

---

