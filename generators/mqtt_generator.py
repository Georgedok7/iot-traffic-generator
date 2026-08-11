from scapy.all import IP, TCP
from scapy.contrib.mqtt import MQTT, MQTTPublish
import random


topics = [
    b"home/temperature",
    b"home/humidity",
    b"device/status"
]


def generate_mqtt_traffic(count=10, broker_ip="192.168.1.200"):
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

        packet = IP(dst=broker_ip) / TCP(
            sport=source_port,
            dport=1883,
            flags="PA"
        ) / MQTT(
            type=3
        ) / MQTTPublish(
            topic=topic,
            value=value
        )

        packets.append(packet)

    return packets