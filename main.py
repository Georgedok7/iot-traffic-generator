import random
import pandas as pd

from scapy.all import wrpcap

from config import (
    RANDOM_SEED,
    TOTAL_FLOWS,
    ATTACK_RATIO,
    DNS_RATIO,
    HTTP_RATIO,
    MQTT_RATIO,
    PORT_SCAN_RATIO,
    MQTT_FLOOD_RATIO,
    DNS_EXFILTRATION_RATIO,
    MIRAI_RATIO
)

from processing.traffic_pipeline import (
    calculate_traffic_counts,
    generate_normal_traffic,
    generate_attack_traffic,
    build_traffic_blocks,
    process_traffic_blocks
)

from processing.dataset_pipeline import (
    process_flow_dataset
)

from processing.statistics import (
    print_dataset_statistics
)

from processing.plots import (
    create_dataset_plots
)

from processing.validation import (
    validate_config,
    validate_dataset
)


PCAP_PATH = "output/pcap/final_mixed_traffic.pcap"
FLOW_CSV_PATH = "output/csv/final_flow_dataset.csv"
BURST_CSV_PATH = "output/csv/attack_burst_statistics.csv"
ZEEK_OUTPUT_DIR = "output/logs/zeek_final"


def main():
    random.seed(RANDOM_SEED)

    validate_config(
        TOTAL_FLOWS,
        ATTACK_RATIO,
        DNS_RATIO,
        HTTP_RATIO,
        MQTT_RATIO,
        PORT_SCAN_RATIO,
        MQTT_FLOOD_RATIO,
        DNS_EXFILTRATION_RATIO,
        MIRAI_RATIO
    )

    counts = calculate_traffic_counts()

    (
        dns_packets,
        http_packets,
        mqtt_packets
    ) = generate_normal_traffic(counts)

    (
        port_scan_packets,
        mqtt_flood_packets,
        dns_exfiltration_packets,
        mirai_packets
    ) = generate_attack_traffic(counts)

    print()
    print("Requested flows:", TOTAL_FLOWS)

    print()
    print("Normal:")
    print("DNS:", counts["dns"])
    print("HTTP:", counts["http"])
    print("MQTT:", counts["mqtt"])

    print()
    print("Attacks:")
    print("Port Scan:", counts["port_scan"])
    print("MQTT Flood:", counts["mqtt_flood"])
    print(
        "DNS Exfiltration:",
        counts["dns_exfiltration"]
    )
    print("Mirai-like:", counts["mirai_like"])

    print()
    print("Generated raw packets:")
    print("DNS packets:", len(dns_packets))
    print("HTTP packets:", len(http_packets))
    print("MQTT packets:", len(mqtt_packets))
    print(
        "Port Scan packets:",
        len(port_scan_packets)
    )
    print(
        "MQTT Flood packets:",
        len(mqtt_flood_packets)
    )
    print(
        "DNS Exfiltration packets:",
        len(dns_exfiltration_packets)
    )
    print(
        "Mirai-like packets:",
        len(mirai_packets)
    )

    traffic_blocks, attack_bursts = (
        build_traffic_blocks(
            dns_packets,
            http_packets,
            mqtt_packets,
            port_scan_packets,
            mqtt_flood_packets,
            dns_exfiltration_packets,
            mirai_packets
        )
    )

    (
        all_packets,
        event_metadata,
        burst_metadata
    ) = process_traffic_blocks(
        traffic_blocks
    )

    print()
    print("Traffic events:", TOTAL_FLOWS)
    print("Attack bursts:", len(attack_bursts))
    print("Total raw packets:", len(all_packets))
    print(
        "Metadata entries:",
        len(event_metadata)
    )

    wrpcap(
        PCAP_PATH,
        all_packets
    )

    print("Mixed PCAP saved successfully.")

    burst_df = pd.DataFrame(
        burst_metadata
    )

    print()
    print("Attack burst statistics:")
    print(
        burst_df.groupby("attack_type")[
            [
                "packet_count",
                "duration",
                "avg_inter_arrival"
            ]
        ].mean()
    )

    burst_df.to_csv(
        BURST_CSV_PATH,
        index=False
    )

    labeled_flow_df = process_flow_dataset(
        PCAP_PATH,
        event_metadata,
        ZEEK_OUTPUT_DIR,
        FLOW_CSV_PATH
    )

    print()
    print(
        "Labeled dataset shape:",
        labeled_flow_df.shape
    )

    print()
    print("Label distribution:")
    print(
        labeled_flow_df[
            "label"
        ].value_counts(
            dropna=False
        )
    )

    print()
    print(
        "Final labeled flow dataset "
        "saved successfully."
    )

    print_dataset_statistics(
        labeled_flow_df
    )

    create_dataset_plots(
        labeled_flow_df,
        burst_df
    )

    print()
    print("Dataset plots saved successfully.")

    validate_dataset(
        labeled_flow_df,
        TOTAL_FLOWS
    )


if __name__ == "__main__":
    main()