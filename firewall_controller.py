from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp

log = core.getLogger()

class FirewallController (object):
    def __init__ (self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.mac_to_port = {}

    def _handle_PacketIn (self, event):
        packet = event.parsed

        # Only inspect IPv4 packets for our firewall rules
        if packet.type == packet.IP_TYPE:
            ip_packet = packet.payload

            # ---------------------------------------------------------
            # FIREWALL RULE 1: IP Filtering
            # Block ALL traffic from h1 (10.0.0.1) to h3 (10.0.0.3)
            # ---------------------------------------------------------
            if ip_packet.srcip == "10.0.0.1" and ip_packet.dstip == "10.0.0.3":
                log.warning(f"[FIREWALL LOG] BLOCKED IP Traffic: {ip_packet.srcip} attempted to reach {ip_packet.dstip}")
                self.drop_packet(event, packet)
                return # Stop processing, do not forward

            # ---------------------------------------------------------
            # FIREWALL RULE 2: Port Filtering
            # Block Web Traffic (TCP Port 8000) going to h2 (10.0.0.2)
            # ---------------------------------------------------------
            if ip_packet.protocol == ipv4.TCP_PROTOCOL:
                tcp_packet = ip_packet.payload
                if ip_packet.dstip == "10.0.0.2" and tcp_packet.dstport == 8000:
                    log.warning(f"[FIREWALL LOG] BLOCKED Port Traffic: TCP Port 8000 access denied to {ip_packet.dstip}")
                    self.drop_packet(event, packet)
                    return

        # ---------------------------------------------------------
        # ALLOWED TRAFFIC: Standard L2 Forwarding
        # If the packet didn't break any rules, forward it normally
        # ---------------------------------------------------------
        self.forward_packet(event, packet)

    def drop_packet(self, event, packet):
        # Install a DROP rule in the switch hardware
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
        # NOTE: Appending NO actions means the switch will DROP the packet
        self.connection.send(msg)

    def forward_packet(self, event, packet):
        # Learn the MAC address and forward safely
        self.mac_to_port[packet.src] = event.port
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            msg = of.ofp_flow_mod()
            msg.match.dl_dst = packet.dst
            msg.actions.append(of.ofp_action_output(port = out_port))
            self.connection.send(msg)
            
            out_msg = of.ofp_packet_out()
            out_msg.data = event.ofp
            out_msg.actions.append(of.ofp_action_output(port = out_port))
            self.connection.send(out_msg)
        else:
            out_msg = of.ofp_packet_out()
            out_msg.data = event.ofp
            out_msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            self.connection.send(out_msg)

def launch ():
    def start_switch (event):
        log.info("SDN Firewall activated and securing the network.")
        FirewallController(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)