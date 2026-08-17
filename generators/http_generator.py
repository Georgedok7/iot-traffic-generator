from scapy.all import IP, TCP, Raw
import random


endpoints = [
    "/sensor",
    "/temperature",
    "/device/status"
]


def generate_http_traffic(
    count=10,
    server_ip="192.168.1.100",
    source_ip="192.168.1.10"
):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)
        temperature = random.randint(18, 30)
        endpoint = random.choice(endpoints)

        client_seq = random.randint(1000, 100000)
        server_seq = random.randint(1000, 100000)

        syn = IP(
            src=source_ip,
            dst=server_ip
        ) / TCP(
            sport=source_port,
            dport=80,
            flags="S",
            seq=client_seq
        )

        syn_ack = IP(
            src=server_ip,
            dst=source_ip
        ) / TCP(
            sport=80,
            dport=source_port,
            flags="SA",
            seq=server_seq,
            ack=client_seq + 1
        )

        ack = IP(
            src=source_ip,
            dst=server_ip
        ) / TCP(
            sport=source_port,
            dport=80,
            flags="A",
            seq=client_seq + 1,
            ack=server_seq + 1
        )

        payload = (
            f"POST {endpoint} HTTP/1.1\r\n"
            "Host: iot-server.local\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            "\r\n"
            f"temperature={temperature}"
        )

        data = IP(
            src=source_ip,
            dst=server_ip
        ) / TCP(
            sport=source_port,
            dport=80,
            flags="PA",
            seq=client_seq + 1,
            ack=server_seq + 1
        ) / Raw(load=payload)

        packets.extend([
            syn,
            syn_ack,
            ack,
            data
        ])

    return packets