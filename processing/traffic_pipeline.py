import random

from config import (
    TOTAL_FLOWS,
    ATTACK_RATIO,
    DNS_RATIO,
    HTTP_RATIO,
    PORT_SCAN_RATIO,
    MQTT_FLOOD_RATIO,
    DNS_EXFILTRATION_RATIO,
    ATTACK_BURST_MIN,
    ATTACK_BURST_MAX,
    NORMAL_DELAY_MIN,
    NORMAL_DELAY_MAX,
    PORT_SCAN_DELAY_MIN,
    PORT_SCAN_DELAY_MAX,
    MQTT_FLOOD_DELAY_MIN,
    MQTT_FLOOD_DELAY_MAX,
    DNS_EXFIL_DELAY_MIN,
    DNS_EXFIL_DELAY_MAX,
    MIRAI_DELAY_MIN,
    MIRAI_DELAY_MAX,
    DEVICE_PROFILES
)

from generators.dns_generator import generate_dns_traffic
from generators.http_generator import generate_http_traffic
from generators.mqtt_generator import generate_mqtt_traffic

from generators.attack_generator import (
    generate_port_scan,
    generate_mqtt_flood,
    generate_dns_exfiltration,
    generate_mirai_like
)


def calculate_traffic_counts():
    attack_count = int(TOTAL_FLOWS * ATTACK_RATIO)
    normal_count = TOTAL_FLOWS - attack_count

    dns_count = int(normal_count * DNS_RATIO)
    http_count = int(normal_count * HTTP_RATIO)
    mqtt_count = normal_count - dns_count - http_count

    port_scan_count = int(attack_count * PORT_SCAN_RATIO)
    mqtt_flood_count = int(attack_count * MQTT_FLOOD_RATIO)
    dns_exfiltration_count = int(
        attack_count * DNS_EXFILTRATION_RATIO
    )

    mirai_count = (
        attack_count
        - port_scan_count
        - mqtt_flood_count
        - dns_exfiltration_count
    )

    return {
        "dns": dns_count,
        "http": http_count,
        "mqtt": mqtt_count,
        "port_scan": port_scan_count,
        "mqtt_flood": mqtt_flood_count,
        "dns_exfiltration": dns_exfiltration_count,
        "mirai_like": mirai_count
    }


def choose_device_for_protocol(protocol):
    devices = list(DEVICE_PROFILES.values())

    valid_devices = []
    weights = []

    for device in devices:
        protocol_weights = device["protocol_weights"]

        if protocol in protocol_weights:
            valid_devices.append(device)
            weights.append(protocol_weights[protocol])

    return random.choices(
        valid_devices,
        weights=weights,
        k=1
    )[0]


def generate_normal_traffic(counts):
    dns_packets = []
    http_packets = []
    mqtt_packets = []

    for _ in range(counts["dns"]):
        device = choose_device_for_protocol("dns")

        packets = generate_dns_traffic(
            count=1,
            source_ip=device["ip"]
        )

        dns_packets.extend(packets)

    for _ in range(counts["http"]):
        device = choose_device_for_protocol("http")

        packets = generate_http_traffic(
            count=1,
            source_ip=device["ip"]
        )

        http_packets.extend(packets)

    for _ in range(counts["mqtt"]):
        device = choose_device_for_protocol("mqtt")

        packets = generate_mqtt_traffic(
            count=1,
            source_ip=device["ip"]
        )

        mqtt_packets.extend(packets)

    return dns_packets, http_packets, mqtt_packets


def generate_attack_traffic(counts):
    return (
        generate_port_scan(counts["port_scan"]),
        generate_mqtt_flood(counts["mqtt_flood"]),
        generate_dns_exfiltration(
            counts["dns_exfiltration"]
        ),
        generate_mirai_like(counts["mirai_like"])
    )


def create_bursts(packets):
    bursts = []
    index = 0

    while index < len(packets):
        burst_size = random.randint(
            ATTACK_BURST_MIN,
            ATTACK_BURST_MAX
        )

        bursts.append(
            packets[index:index + burst_size]
        )

        index += burst_size

    return bursts


def build_traffic_blocks(
    dns_packets,
    http_packets,
    mqtt_packets,
    port_scan_packets,
    mqtt_flood_packets,
    dns_exfiltration_packets,
    mirai_packets
):
    normal_events = []

    for i in range(0, len(dns_packets), 2):
        normal_events.append(
            ("normal", dns_packets[i:i + 2])
        )

    for i in range(0, len(http_packets), 4):
        normal_events.append(
            ("normal", http_packets[i:i + 4])
        )

    for i in range(0, len(mqtt_packets), 4):
        normal_events.append(
            ("normal", mqtt_packets[i:i + 4])
        )

    random.shuffle(normal_events)

    attack_bursts = []

    attack_groups = [
        ("port_scan", port_scan_packets),
        ("mqtt_flood", mqtt_flood_packets),
        (
            "dns_exfiltration",
            dns_exfiltration_packets
        ),
        ("mirai_like", mirai_packets)
    ]

    for attack_type, packets in attack_groups:
        for burst in create_bursts(packets):
            attack_bursts.append(
                (attack_type, burst)
            )

    random.shuffle(attack_bursts)

    traffic_blocks = normal_events.copy()

    for attack_type, burst in attack_bursts:
        position = random.randint(
            0,
            len(traffic_blocks)
        )

        traffic_blocks.insert(
            position,
            (attack_type, burst)
        )

    return traffic_blocks, attack_bursts


def apply_timing(
    block_type,
    packets,
    current_time
):
    if block_type == "normal":
        current_time += random.uniform(
            NORMAL_DELAY_MIN,
            NORMAL_DELAY_MAX
        )

        for packet in packets:
            packet.time = current_time
            current_time += random.uniform(
                0.001,
                0.01
            )

    elif block_type == "port_scan":
        delay_min = PORT_SCAN_DELAY_MIN
        delay_max = PORT_SCAN_DELAY_MAX

        for packet in packets:
            current_time += random.uniform(
                delay_min,
                delay_max
            )
            packet.time = current_time

    elif block_type == "mqtt_flood":
        delay_min = MQTT_FLOOD_DELAY_MIN
        delay_max = MQTT_FLOOD_DELAY_MAX

        for packet in packets:
            current_time += random.uniform(
                delay_min,
                delay_max
            )
            packet.time = current_time

    elif block_type == "dns_exfiltration":
        delay_min = DNS_EXFIL_DELAY_MIN
        delay_max = DNS_EXFIL_DELAY_MAX

        for packet in packets:
            current_time += random.uniform(
                delay_min,
                delay_max
            )
            packet.time = current_time

    elif block_type == "mirai_like":
        delay_min = MIRAI_DELAY_MIN
        delay_max = MIRAI_DELAY_MAX

        for packet in packets:
            current_time += random.uniform(
                delay_min,
                delay_max
            )
            packet.time = current_time

    return current_time


def create_event_metadata(
    block_type,
    packets
):
    metadata = []

    if block_type == "normal":
        metadata_packets = [packets[0]]
    else:
        metadata_packets = packets

    for packet in metadata_packets:
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst

        if packet.haslayer("TCP"):
            src_port = packet["TCP"].sport
            dst_port = packet["TCP"].dport
            protocol = "tcp"

        elif packet.haslayer("UDP"):
            src_port = packet["UDP"].sport
            dst_port = packet["UDP"].dport
            protocol = "udp"

        else:
            src_port = None
            dst_port = None
            protocol = None

        metadata.append({
            "src_ip": src_ip,
            "src_port": src_port,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "protocol": protocol,
            "label": block_type
        })

    return metadata


def create_burst_metadata(
    block_type,
    packets
):
    if block_type == "normal":
        return None

    start_time = float(packets[0].time)
    end_time = float(packets[-1].time)

    duration = end_time - start_time

    if len(packets) > 1:
        inter_arrival_times = [
            float(packets[i].time)
            - float(packets[i - 1].time)
            for i in range(1, len(packets))
        ]

        average_inter_arrival = (
            sum(inter_arrival_times)
            / len(inter_arrival_times)
        )

    else:
        average_inter_arrival = 0.0

    return {
        "attack_type": block_type,
        "packet_count": len(packets),
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "avg_inter_arrival":
            average_inter_arrival
    }


def process_traffic_blocks(
    traffic_blocks
):
    all_packets = []
    event_metadata = []
    burst_metadata = []

    current_time = 0.0

    for block_type, packets in traffic_blocks:
        current_time = apply_timing(
            block_type,
            packets,
            current_time
        )

        event_metadata.extend(
            create_event_metadata(
                block_type,
                packets
            )
        )

        burst_info = create_burst_metadata(
            block_type,
            packets
        )

        if burst_info is not None:
            burst_metadata.append(
                burst_info
            )

        all_packets.extend(packets)

    return (
        all_packets,
        event_metadata,
        burst_metadata
    )