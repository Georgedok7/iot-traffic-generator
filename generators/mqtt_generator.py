from scapy.all import IP, TCP
from scapy.contrib.mqtt import MQTT, MQTTPublish
import random


topics = [
    b"home/temperature",
    b"home/humidity",
    b"device/status"
]


def generate_mqtt_traffic(
    count=10,
    broker_ip="192.168.1.200",
    source_ip="192.168.1.10"
):
    packets = []

    for _ in range(count):
        source_port = random.randint(49152, 65535)
        topic = random.choice(topics)

        if topic == b"home/temperature":
            value = str(random.randint(18, 30)).encode()
        elif topic == b"home/humidity":
            value = str(random.randint(30, 80)).encode()
        else:
            value = random.choice([b"online", b"idle", b"active"])

        client_seq = random.randint(1000, 100000)
        server_seq = random.randint(1000, 100000)

        syn = IP(
            src=source_ip,
            dst=broker_ip
        ) / TCP(
            sport=source_port,
            dport=1883,
            flags="S",
            seq=client_seq
        )

        syn_ack = IP(
            src=broker_ip,
            dst=source_ip
        ) / TCP(
            sport=1883,
            dport=source_port,
            flags="SA",
            seq=server_seq,
            ack=client_seq + 1
        )

        ack = IP(
            src=source_ip,
            dst=broker_ip
        ) / TCP(
            sport=source_port,
            dport=1883,
            flags="A",
            seq=client_seq + 1,
            ack=server_seq + 1
        )

        publish = IP(
            src=source_ip,
            dst=broker_ip
        ) / TCP(
            sport=source_port,
            dport=1883,
            flags="PA",
            seq=client_seq + 1,
            ack=server_seq + 1
        ) / MQTT(type=3) / MQTTPublish(
            topic=topic,
            value=value
        )

        packets.extend([
            syn,
            syn_ack,
            ack,
            publish
        ])

    return packets