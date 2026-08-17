from scapy.all import IP, TCP, UDP, DNS, DNSQR
from scapy.contrib.mqtt import MQTT, MQTTPublish
import random

def generate_port_scan(count=20, target_ip="192.168.1.250"):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)
        destination_port = random.randint(1, 1024)

        packet = IP(dst=target_ip) / TCP(
            sport=source_port,
            dport=destination_port,
            flags="S"
        )

        packets.append(packet)

    return packets

def generate_mqtt_flood(count=100, broker_ip="192.168.1.200"):
    packets = []

    available_ports = range(49152, 65536)

    if count > len(available_ports):
        raise ValueError(
            "MQTT flood count exceeds the available source port range."
        )

    source_ports = random.sample(
        available_ports,
        count
    )

    for source_port in source_ports:
        value = str(
            random.randint(0, 100)
        ).encode()

        packet = IP(dst=broker_ip) / TCP(
            sport=source_port,
            dport=1883,
            flags="PA"
        ) / MQTT(type=3) / MQTTPublish(
            topic=b"home/temperature",
            value=value
        )

        packets.append(packet)

    return packets

def generate_dns_exfiltration(count=50, dns_server="8.8.8.8"):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)

        encoded_data = "".join(
            random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
            for _ in range(20)
        )

        domain = f"{encoded_data}.exfil.local"

        packet = IP(dst=dns_server) / UDP(
            sport=source_port,
            dport=53
        ) / DNS(
            rd=1,
            qd=DNSQR(qname=domain)
        )

        packets.append(packet)

    return packets

def generate_mirai_like(count=100):
    packets = []

    common_ports = [23, 2323, 80, 8080]

    for _ in range(count):
        target_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        source_port = random.randint(49152, 65535)
        destination_port = random.choice(common_ports)

        packet = IP(dst=target_ip) / TCP(
            sport=source_port,
            dport=destination_port,
            flags="S"
        )

        packets.append(packet)

    return packets