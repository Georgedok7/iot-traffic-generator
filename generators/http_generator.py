from scapy.all import IP, TCP, Raw
import random


endpoints = [
    "/sensor",
    "/temperature",
    "/device/status"
]


def generate_http_traffic(count=10, server_ip="192.168.1.100"):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)
        temperature = random.randint(18, 30)
        endpoint = random.choice(endpoints)

        payload = (
            f"POST {endpoint} HTTP/1.1\r\n"
            "Host: iot-server.local\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "\r\n"
            f"temperature={temperature}"
        )

        packet = IP(dst=server_ip) / TCP(
            sport=source_port,
            dport=80,
            flags="PA"
        ) / Raw(load=payload)

        packets.append(packet)

    return packets